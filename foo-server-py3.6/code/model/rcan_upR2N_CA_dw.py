from model import common
import torch
import torch.nn as nn
import math


def make_model(args, parent=False):
    return RCAN(args)


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=dilation, groups=groups, bias=False, dilation=dilation)


def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


# mulscale block 经过一次卷积后通过多尺度结构，然后输入与输出残差连接
class MulScaleBlock(nn.Module):
    __constants__ = ['downsample']

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(MulScaleBlock, self).__init__()
        # norm_layer = nn.BatchNorm2d
        scale_width = int(planes / 4)

        self.scale_width = scale_width

        self.conv1 = conv3x3(inplanes, planes, stride)
        # self.bn1 = norm_layer(planes)
        self.relu = nn.ReLU(inplace=False)

        self.conv1_2_1 = conv3x3(scale_width, scale_width)
        # self.bn1_2_1 = norm_layer(scale_width)
        self.conv1_2_2 = conv3x3(scale_width, scale_width)
        # self.bn1_2_2 = norm_layer(scale_width)
        self.conv1_2_3 = conv3x3(scale_width, scale_width)
        # self.bn1_2_3 = norm_layer(scale_width)
        self.conv1_2_4 = conv3x3(scale_width, scale_width)
        # self.bn1_2_4 = norm_layer(scale_width)

        # self.conv2_2_1 = conv3x3(scale_width, scale_width)
        # # self.bn2_2_1 = norm_layer(scale_width)
        # self.conv2_2_2 = conv3x3(scale_width, scale_width)
        # # self.bn2_2_2 = norm_layer(scale_width)
        # self.conv2_2_3 = conv3x3(scale_width, scale_width)
        # # self.bn2_2_3 = norm_layer(scale_width)
        # self.conv2_2_4 = conv3x3(scale_width, scale_width)
        # # self.bn2_2_4 = norm_layer(scale_width)

        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        # out = self.bn1(out)
        out = self.relu(out)

        sp_x = torch.split(out, self.scale_width, 1)

        ##########################################################
        out_1_1 = self.conv1_2_1(sp_x[0])
        # out_1_1 = self.bn1_2_1(out_1_1)
        out_1_1_relu = self.relu(out_1_1)
        out_1_2 = self.conv1_2_2(out_1_1_relu + sp_x[1])
        # out_1_2 = self.bn1_2_2(out_1_2)
        out_1_2_relu = self.relu(out_1_2)
        out_1_3 = self.conv1_2_3(out_1_2_relu + sp_x[2])
        # out_1_3 = self.bn1_2_3(out_1_3)
        out_1_3_relu = self.relu(out_1_3)
        out_1_4 = self.conv1_2_4(out_1_3_relu + sp_x[3])
        # out_1_4 = self.bn1_2_4(out_1_4)
        output_1 = torch.cat([out_1_1, out_1_2, out_1_3, out_1_4], dim=1)

        # out_2_1 = self.conv2_2_1(sp_x[3])
        # # out_2_1 = self.bn2_2_1(out_2_1)
        # out_2_1_relu = self.relu(out_2_1)
        # out_2_2 = self.conv2_2_2(out_2_1_relu + sp_x[2])
        # # out_2_2 = self.bn2_2_2(out_2_2)
        # out_2_2_relu = self.relu(out_2_2)
        # out_2_3 = self.conv2_2_3(out_2_2_relu + sp_x[1])
        # # out_2_3 = self.bn2_2_3(out_2_3)
        # out_2_3_relu = self.relu(out_2_3)
        # out_2_4 = self.conv2_2_4(out_2_3_relu + sp_x[0])
        # # out_2_4 = self.bn2_2_4(out_2_4)
        # output_2 = torch.cat([out_2_1, out_2_2, out_2_3, out_2_4], dim=1)

        # out = output_1 + output_2
        out = output_1

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class h_swish(nn.Module):
    def __init__(self, inplace=True):
        super(h_swish, self).__init__()
        self.sigmoid = h_sigmoid(inplace=inplace)

    def forward(self, x):
        return x * self.sigmoid(x)


class h_sigmoid(nn.Module):
    def __init__(self, inplace=True):
        super(h_sigmoid, self).__init__()
        self.relu = nn.ReLU6(inplace=inplace)

    def forward(self, x):
        return self.relu(x + 3) / 6


class CoordAtt(nn.Module):
    def __init__(self, inp, oup, groups=32):
        super(CoordAtt, self).__init__()
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))

        mip = max(8, inp // groups)

        self.conv1 = nn.Conv2d(inp, mip, kernel_size=1, stride=1, padding=0)
        # self.bn1 = nn.BatchNorm2d(mip)
        self.conv2 = nn.Conv2d(mip, oup, kernel_size=1, stride=1, padding=0)
        self.conv3 = nn.Conv2d(mip, oup, kernel_size=1, stride=1, padding=0)
        self.relu = h_swish()

    def forward(self, x):
        identity = x
        n, c, h, w = x.size()
        x_h = self.pool_h(x)
        x_w = self.pool_w(x).permute(0, 1, 3, 2)

        y = torch.cat([x_h, x_w], dim=2)
        y = self.conv1(y)
        # y = self.bn1(y)
        y = self.relu(y)
        x_h, x_w = torch.split(y, [h, w], dim=2)
        x_w = x_w.permute(0, 1, 3, 2)

        x_h = self.conv2(x_h).sigmoid()
        x_w = self.conv3(x_w).sigmoid()
        x_h = x_h.expand(-1, -1, h, w)
        x_w = x_w.expand(-1, -1, h, w)

        y = identity * x_w * x_h

        return y


# class GhostModule(nn.Module):
#     def __init__(self, inp, oup, kernel_size=1, ratio=2, dw_size=3, stride=1, relu=True):
#         super(GhostModule, self).__init__()
#
#         self.oup = oup
#         init_channels = math.ceil(oup / ratio)
#         new_channels = init_channels * (ratio - 1)
#         self.primary_conv = nn.Sequential(
#             nn.Conv2d(inp, init_channels, kernel_size, stride, padding=kernel_size // 2, bias=False),
#             nn.ReLU(inplace=True) if relu else nn.Sequential(),
#         )
#         self.cheap_operation = nn.Sequential(
#             nn.Conv2d(init_channels, new_channels, dw_size, stride=1,
#                       padding=dw_size // 2, groups=init_channels, bias=False),
#             nn.ReLU(inplace=True) if relu else nn.Sequential(),
#         )
#
#     def forward(self, x):
#         x1 = self.primary_conv(x)
#         x2 = self.cheap_operation(x1)
#         out = torch.cat([x1, x2], dim=1)
#         return out[:, :self.oup, :, :]

class DepthwiseMoudle(nn.Module):
    def __init__(self, inp, oup, kernel_size=1, dw_size=3, stride=1, relu=True):
        super(DepthwiseMoudle, self).__init__()

        self.oup = oup
        self.dw_conv = nn.Sequential(
            nn.Conv2d(inp, inp, dw_size, stride, padding=dw_size // 2,groups=inp, bias=False),
            nn.ReLU6(inplace=True) if relu else nn.Sequential(),
        )
        self.normal_conv = nn.Sequential(
            nn.Conv2d(inp, oup, kernel_size, stride=1,
                      padding=kernel_size // 2, bias=False),
            nn.ReLU6(inplace=True) if relu else nn.Sequential(),
        )

    def forward(self, x):
        x = self.dw_conv(x)
        x = self.normal_conv(x)
        return x

## Channel Attention (CA) Layer
class CALayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(CALayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.conv_du = nn.Sequential(
            nn.Conv2d(channel, channel // reduction, 1, padding=0, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(channel // reduction, channel, 1, padding=0, bias=True),
            nn.Sigmoid()
        )

    def forward(self, x):
        y = self.avg_pool(x)
        y = self.conv_du(y)
        return x * y


## Residual Channel Attention Block (RCAB)
class RCAB(nn.Module):
    def __init__(
            self, conv, n_feat, kernel_size, reduction,
            bias=True, bn=False, act=nn.ReLU(True), res_scale=1):
        super(RCAB, self).__init__()
        modules_body = []
        # for i in range(2):
        #     modules_body.append(conv(n_feat, n_feat, kernel_size, bias=bias))
        #     if bn: modules_body.append(nn.BatchNorm2d(n_feat))
        #     if i == 0: modules_body.append(act)
        modules_body.append(DepthwiseMoudle(n_feat, n_feat, kernel_size=1, dw_size=3, stride=1, relu=True))
        modules_body.append(CALayer(n_feat, reduction))
        # modules_body.append(MulScaleBlock(n_feat, n_feat))
        # modules_body.append(CoordAtt(n_feat, n_feat))

        self.body = nn.Sequential(*modules_body)
        self.res_scale = res_scale

    def forward(self, x):
        res = self.body(x)
        # res = self.body(x).mul(self.res_scale)
        res += x
        return res


## Residual Group (RG)
class ResidualGroup(nn.Module):
    def __init__(self, conv, n_feat, kernel_size, reduction, act, res_scale, n_resblocks):
        super(ResidualGroup, self).__init__()
        modules_body = []
        modules_body = [
            RCAB(
                conv, n_feat, kernel_size, reduction, bias=True, bn=False, act=nn.ReLU(True), res_scale=1) \
            for _ in range(n_resblocks)]
        modules_body.append(conv(n_feat, n_feat, kernel_size))
        self.body = nn.Sequential(*modules_body)

    def forward(self, x):
        res = self.body(x)
        res += x
        return res


class RCAN(nn.Module):
    def __init__(self, args, conv=common.default_conv):
        super(RCAN, self).__init__()

        n_resgroups = args.n_resgroups
        n_resblocks = args.n_resblocks
        n_feats = args.n_feats
        kernel_size = 3
        reduction = args.reduction
        scale = args.scale[0]
        act = nn.ReLU(True)

        # RGB mean for DIV2K 1-800
        # rgb_mean = (0.4488, 0.4371, 0.4040)
        # RGB mean for DIVFlickr2K 1-3450
        # rgb_mean = (0.4690, 0.4490, 0.4036)
        if args.data_train == 'DIV2K':
            print('Use DIV2K mean (0.4488, 0.4371, 0.4040)')
            rgb_mean = (0.4488, 0.4371, 0.4040)
        elif args.data_train == 'DIVFlickr2K':
            print('Use DIVFlickr2K mean (0.4690, 0.4490, 0.4036)')
            rgb_mean = (0.4690, 0.4490, 0.4036)
        rgb_std = (1.0, 1.0, 1.0)
        self.sub_mean = common.MeanShift(args.rgb_range, rgb_mean, rgb_std)

        # define head module
        modules_head = [conv(args.n_colors, n_feats, kernel_size)]

        # define body module
        modules_body = [
            ResidualGroup(
                conv, n_feats, kernel_size, reduction, act=act, res_scale=args.res_scale, n_resblocks=n_resblocks) \
            for _ in range(n_resgroups)]

        modules_body.append(conv(n_feats, n_feats, kernel_size))

        # define tail module
        # modules_tail = [
        #     common.Upsampler(conv, scale, n_feats, act=False),
        #     conv(n_feats, args.n_colors, kernel_size)]

        # modules_tail = [
        #     MulScaleBlock(n_feats, n_feats), CoordAtt(n_feats, n_feats),
        #     common.Upsampler(conv, scale, n_feats, act=False),
        #     conv(n_feats, args.n_colors, kernel_size)]

        modules_tail = [
            common.Upsampler(conv, scale, n_feats, act=False),
            MulScaleBlock(n_feats, n_feats), CoordAtt(n_feats, n_feats),
            conv(n_feats, args.n_colors, kernel_size),
        ]

        self.add_mean = common.MeanShift(args.rgb_range, rgb_mean, rgb_std, 1)

        self.head = nn.Sequential(*modules_head)
        self.body = nn.Sequential(*modules_body)
        self.tail = nn.Sequential(*modules_tail)

    def forward(self, x):
        x = self.sub_mean(x)
        x = self.head(x)

        res = self.body(x)
        res += x

        x = self.tail(res)
        x = self.add_mean(x)

        return x

    def load_state_dict(self, state_dict, strict=False):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') >= 0:
                        print('Replace pre-trained upsampler to new one...')
                    else:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

        if strict:
            missing = set(own_state.keys()) - set(state_dict.keys())
            if len(missing) > 0:
                raise KeyError('missing keys in state_dict: "{}"'.format(missing))
