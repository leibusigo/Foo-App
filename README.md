# Foo-App

## 概述

基于 Nao 机器人自动跟踪系统的前后端分离项目

[![vLOSot.png](https://s1.ax1x.com/2022/09/10/vLOSot.png)](https://imgse.com/i/vLOSot)

## 技术栈

前端：语言：ts + scss；框架： react + antd-mobile；端口：3000

后端：语言：python 2.7 + python3.6 ；框架：pytorch + flask + mongodb；端口4018（2.7），4014（3.6）

数据库：mongodb

## 运行

> 注意:运行前先连接choregraphe,将nao机器人活动状态关闭,以免影响程序的正常运行

[![vLHV58.png](https://s1.ax1x.com/2022/09/10/vLHV58.png)](https://imgse.com/i/vLHV58)

前端，在前端根目录`/foo-front`打开

```
cmd终端

npm i

npm run start
```

后端

```
py 2.7
下载依赖库，下载naoqi sdk
在main.py运行

py 3.6
将yolo权重放入 ./modal_data文件夹中
下载依赖库
在main.py运行
```

数据库

```
下载mongodb，配置环境变量即可
```

