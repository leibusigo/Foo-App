# -*- coding: utf-8 -*-
"""
 @Time   : 2020/10/29 9:54
 @Athor   : LinXiao
 @功能   :
"""
# ------------------------------
import datetime
import io
import uuid
import requests
import oss2


# 储存的路径
# filePath="/house/2020-10-29/xxxx.jpg"  # xxxxx 为随机uuid,防止重复
# # 指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
# bucket=oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

# 连接oss
def oss_parser(img, imageName, dirpath):
    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'  # 在哪个城市就选那个城市的oss-cn
    access_key_id = 'LTAI5tEjvgxJVugXp9pYgBrJ'
    access_key_secret = 'FoZaWkS6SW3x1Fgvl4GK880ulXrJWR'
    bucket_name = 'foo-app'
    # 指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    # result = bucket.put_object(f'{dirpath}/{imageName}', img.getvalue())
    # print('图片上传oss success!')
    # return result.status


# 上床成功并返回图片的链接
def oss_deal_pic(url):
    # 测试的阿里云oss储存路径,正式的为house
    dirpath = 'house'
    domain = 'http://oss.fapai*****fang.top****************/'
    now = datetime.datetime.now()
    nonce = str(uuid.uuid4())
    random_name = now.strftime("%Y-%m-%d") + "/" + nonce
    imageName = '{}.jpg'.format(random_name)

    img = io.BytesIO(requests.get(url, timeout=300).content)
    statusCode = oss_parser(img, imageName, dirpath)
    if statusCode == 200:
        new_oss_url = domain + dirpath + '/' + imageName
        # new_oss_url= '/' + imageName
        # print(new_oss_url)
        # print(type(new_oss_url))   # <class 'str'>
        return new_oss_url


if __name__ == '__main__':
    # url='https://img.alicdn.com/bao/uploaded/i3/TB1LMGLiP39YK4jSZPctrBrUFXa_460x460.jpg'
    url = 'https://img.alicdn.com/bao/uploaded/i4/O1CN01CW2jEc1pOLaFef85M_!!0-paimai.jpg_460x460.jpg'

    oss_deal_pic(url)
    print(len("http://oss.fapaifang.top/house-test/2020-10-29/a12e11c9-d965-448b-b323-eb743d7ad327.jpg"))  # 87的长度
    print(len("/2020-10-29/a12e11c9-d965-448b-b323-eb743d7ad327.jpg"))  # 87的长度
    # 所以这里mysql的pic的字段的设置的默认长度应该是90x5 450个长度