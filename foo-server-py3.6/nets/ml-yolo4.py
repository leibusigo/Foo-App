from collections import OrderedDict

import torch
import torch.nn as nn

from nets.mobilenet_v1 import mobilenet_v1
from nets.mobilenet_v2 import mobilenet_v2
from nets.mobilenet_v3 import mobilenet_v3


class MobileNetV1(nn.Module):
    def __init__(self, pretrained = False):
        super(MobileNetV1, self).__init__()
        self.model = mobilenet_v1(pretrained=pretrained)

    def forward(self, x):
        out3 = self.model.stage1(x)
        out4 = self.model.stage2(out3)
        out5 = self.model.stage3(out4)
        return out3, out4, out5

class MobileNetV2(nn.Module):
    def __init__(self, pretrained = False):
        super(MobileNetV2, self).__init__()
        self.model = mobilenet_v2(pretrained=pretrained)

    def forward(self, x):
        out3 = self.model.features[:7](x)
        out4 = self.model.features[7:14](out3)
        out5 = self.model.features[14:18](out4)
        return out3, out4, out5

class MobileNetV3(nn.Module):
    def __init__(self, pretrained = False):
        super(MobileNetV3, self).__init__()
        self.model = mobilenet_v3(pretrained=pretrained)

    def forward(self, x):
        out3 = self.model.features[:7](x)
        out4 = self.model.features[7:13](out3)
        out5 = self.model.features[13:16](out4)
        return out3, out4, out5

def conv2d(filter_in, filter_out, kernel_size, groups=1, stride=1):
    pad = (kernel_size - 1) // 2 if kernel_size else 0
    return nn.Sequential(OrderedDict([
        ("conv", nn.Conv2d(filter_in, filter_out, kernel_size=kernel_size, stride=stride, padding=pad, groups=groups, bias=False)),
        ("bn", nn.BatchNorm2d(filter_out)),
        ("relu", nn.ReLU6(inplace=True)),
    ]))

def conv_dw(filter_in, filter_out, stride = 1):
    return nn.Sequential(
        nn.Conv2d(filter_in, filter_in, 3, stride, 1, groups=filter_in, bias=False),
        nn.BatchNorm2d(filter_in),
        nn.ReLU6(inplace=True),

        nn.Conv2d(filter_in, filter_out, 1, 1, 0, bias=False),
        nn.BatchNorm2d(filter_out),
        nn.ReLU6(inplace=True),
    )

#---------------------------------------------------#
#   SPP结构，利用不同大小的池化核进行池化
#   池化后堆叠
#---------------------------------------------------#
class SpatialPyramidPooling(nn.Module):
    def __init__(self, pool_sizes=[5, 9, 13]):
        super(SpatialPyramidPooling, self).__init__()

        self.maxpools = nn.ModuleList([nn.MaxPool2d(pool_size, 1, pool_size//2) for pool_size in pool_sizes])

    def forward(self, x):
        features = [maxpool(x) for maxpool in self.maxpools[::-1]]
        features = torch.cat(features + [x], dim=1)

        return features

#---------------------------------------------------#
#   卷积 + 上采样
#---------------------------------------------------#
class Upsample(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(Upsample, self).__init__()

        self.upsample = nn.Sequential(
            conv2d(in_channels, out_channels, 1),
            nn.Upsample(scale_factor=2, mode='nearest')
        )

    def forward(self, x,):
        x = self.upsample(x)
        return x

#---------------------------------------------------#
#   三次卷积块
#---------------------------------------------------#
def make_three_conv(filters_list, in_filters):
    m = nn.Sequential(
        conv2d(in_filters, filters_list[0], 1),
        conv_dw(filters_list[0], filters_list[1]),
        conv2d(filters_list[1], filters_list[0], 1),
    )
    return m

#---------------------------------------------------#
#   五次卷积块
#---------------------------------------------------#
def make_five_conv(filters_list, in_filters):
    m = nn.Sequential(
        conv2d(in_filters, filters_list[0], 1),
        conv_dw(filters_list[0], filters_list[1]),
        conv2d(filters_list[1], filters_list[0], 1),
        conv_dw(filters_list[0], filters_list[1]),
        conv2d(filters_list[1], filters_list[0], 1),
    )
    return m

#---------------------------------------------------#
#   最后获得yolov4的输出
#---------------------------------------------------#
def yolo_head(filters_list, in_filters):
    m = nn.Sequential(
        conv_dw(in_filters, filters_list[0]),
        
        nn.Conv2d(filters_list[0], filters_list[1], 1),
    )
    return m


class Swish(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)


class SwishImplementation(torch.autograd.Function):
    @staticmethod
    def forward(ctx, i):
        result = i * torch.sigmoid(i)
        ctx.save_for_backward(i)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        i = ctx.saved_variables[0]
        sigmoid_i = torch.sigmoid(i)
        return grad_output * (sigmoid_i * (1 + i * (1 - sigmoid_i)))


class MemoryEfficientSwish(nn.Module):
    def forward(self, x):
        return SwishImplementation.apply(x)

#---------------------------------------------------#
#   yolo_body
#---------------------------------------------------#
class YoloBody(nn.Module):
    def __init__(self, num_anchors, num_classes, backbone="mobilenetv3", pretrained=False):
        super(YoloBody, self).__init__()
        #---------------------------------------------------#   
        #   生成mobilnet的主干模型，获得三个有效特征层。
        #---------------------------------------------------#
        if backbone == "mobilenetv1":
            #---------------------------------------------------#   
            #   52,52,256；26,26,512；13,13,1024
            #---------------------------------------------------#
            self.backbone = MobileNetV1(pretrained=pretrained)
            in_filters = [256,512,1024]
        elif backbone == "mobilenetv2":
            #---------------------------------------------------#   
            #   52,52,32；26,26,92；13,13,320
            #---------------------------------------------------#
            self.backbone = MobileNetV2(pretrained=pretrained)
            in_filters = [32,96,320]
        elif backbone == "mobilenetv3":
            #---------------------------------------------------#   
            #   52,52,40；26,26,112；13,13,160
            #---------------------------------------------------#
            self.backbone = MobileNetV3(pretrained=pretrained)
            in_filters = [40,112,160]
        else:
            raise ValueError('Unsupported backbone - `{}`, Use mobilenetv1, mobilenetv2, mobilenetv3.'.format(backbone))

        self.Swish = Swish()

        # 分母常数
        self.epsilon = 1e-4

        # 简易注意力机制的weights
        self.p5_w1 = nn.Parameter(torch.ones(2, dtype=torch.float32), requires_grad=True)
        self.p5_w1_relu = nn.ReLU()
        self.p4_w1 = nn.Parameter(torch.ones(2, dtype=torch.float32), requires_grad=True)
        self.p4_w1_relu = nn.ReLU()
        self.p3_w1 = nn.Parameter(torch.ones(2, dtype=torch.float32), requires_grad=True)
        self.p3_w1_relu = nn.ReLU()

        self.p4_w2 = nn.Parameter(torch.ones(3, dtype=torch.float32), requires_grad=True)
        self.p4_w2_relu = nn.ReLU()

        self.conv4_td        = make_three_conv([256,512],256)
        self.conv3_out       = make_three_conv([128,256],128)
        self.conv4_out       = make_three_conv([256,512],256)
        self.conv5_out       = make_three_conv([512,1024],512)

        self.conv1           = make_three_conv([512, 1024], in_filters[2])
        self.SPP             = SpatialPyramidPooling()
        self.conv2           = make_three_conv([512, 1024], 2048)

        self.upsample1       = Upsample(512, 256)
        self.conv_for_P4     = conv2d(in_filters[1], 256,1)
        self.make_five_conv1 = make_five_conv([256, 512], 256)

        self.upsample2       = Upsample(256, 128)
        self.conv_for_P3     = conv2d(in_filters[0], 128,1)
        self.make_five_conv2 = make_five_conv([128, 256], 128)

        # 3*(5+num_classes) = 3*(5+20) = 3*(4+1+20)=75
        final_out_filter2    = num_anchors * (5 + num_classes)
        self.yolo_head3      = yolo_head([256, final_out_filter2],128)

        self.down_sample1    = conv_dw(128, 256,stride=2)
        self.make_five_conv3 = make_five_conv([256, 512],256)

        # 3*(5+num_classes) = 3*(5+20) = 3*(4+1+20)=75
        final_out_filter1    = num_anchors * (5 + num_classes)
        self.yolo_head2      = yolo_head([512, final_out_filter1], 256)

        self.down_sample2    = conv_dw(256, 512,stride=2)
        self.make_five_conv4 = make_five_conv([512, 1024], 512)

        # 3*(5+num_classes) = 3*(5+20) = 3*(4+1+20)=75
        final_out_filter0    = num_anchors * (5 + num_classes)
        self.yolo_head1      = yolo_head([1024, final_out_filter0], 512)


    def forward(self, x):
        """ 改进bifpn模块结构示意图
                        P5_0 ---------> P5_1 ---------> P5_2 -------->
                          |-------------|                ↑
                                        ↓                |
                       P4_0 ---------> P4_1 ---------> P4_2 -------->
                          |-------------|--------------↑ ↑
                                        |--------------↓ |
                       P3_0 -------------------------> P3_2 -------->
        """
        #  backbone
        x2, x1, x0 = self.backbone(x)

        P5 = self.conv1(x0)
        P5 = self.SPP(P5)
        P5 = self.conv2(P5)

        P5_upsample = self.upsample1(P5)
        P4 = self.conv_for_P4(x1)
        # 简单的注意力机制，用于确定更关注p5_upsample还是p4_1
        p4_w1 = self.p4_w1_relu(self.p4_w1)
        weight = p4_w1 / (torch.sum(p4_w1, dim=0) + self.epsilon)
        p4_td = self.conv4_td(weight[0] * P4 + weight[1] * P5_upsample)

        # P4_1 = torch.cat([P4, P5_upsample], axis=1)
        p4_td = self.make_five_conv1(p4_td)

        P4_upsample = self.upsample2(p4_td)
        P3 = self.conv_for_P3(x2)
        p3_w1 = self.p3_w1_relu(self.p3_w1)
        weight = p3_w1 / (torch.sum(p3_w1, dim=0) + self.epsilon)
        p3_out = self.conv3_out(weight[0] * P3 + weight[1] * P4_upsample)

        # P3 = torch.cat([P3,P4_upsample],axis=1)
        p3_out = self.make_five_conv2(p3_out)

        P3_downsample = self.down_sample1(p3_out)
        p4_w2 = self.p4_w2_relu(self.p4_w2)
        weight = p4_w2 / (torch.sum(p4_w2, dim=0) + self.epsilon)
        p4_out = self.conv4_out(weight[0] * P4 + weight[1] * p4_td+ weight[2] * P3_downsample)

        # P4 = torch.cat([P3_downsample,P4_1,P4],axis=1)
        p4_out = self.make_five_conv3(p4_out)

        P4_downsample = self.down_sample2(p4_out)
        p5_w1 = self.p5_w1_relu(self.p5_w1)
        weight = p5_w1 / (torch.sum(p5_w1, dim=0) + self.epsilon)
        p5_out = self.conv5_out(weight[0] * P5 + weight[1] * P4_downsample)

        # P5 = torch.cat([P4_downsample,P5],axis=1)
        p5_out = self.make_five_conv4(p5_out)

        out2 = self.yolo_head3(p3_out)
        out1 = self.yolo_head2(p4_out)
        out0 = self.yolo_head1(p5_out)

        return out0, out1, out2

