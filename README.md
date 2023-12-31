# jiesysadmin-centos-package

## 介绍
Jiesysadmin centos 是用 Python 开发的，用于部署在centOS中远程管理系统的工具系统
本仓库为主代码仓库

## 截图
![首页截图](https://gitee.com/cosyjie/jiesysadmin-centos-code/raw/main/screenshot/index.jpg "首页")
![防火墙管理截图](https://gitee.com/cosyjie/jiesysadmin-centos-code/raw/main/screenshot/firewall.jpg "防火墙")

## 地址：
个人主页Github: https://github.com/cosyjie
个人主页Gitee:  https://gitee.com/cosyjie

发布包仓库：
github:https://github.com/cosyjie/jiesysadmin-centos-package
Gitee:https://gitee.com/cosyjie/jiesysadmin-centos-package

## 注意

本代码不具备生产环境部署条件，请勿用于生产环境和商业环境

## 可用服务器

测试运行于 CentOS 7.9.2009-x86_64 最小安装，且未安装其他软件的情况下进行安装。
安装需要连接外网

## 安装教程

当前为部署包库。安装方法如下：
1.  登录 root 权限的帐号
2.  将所有的文件包和文件都上传到 /opt 目录中
3.  运行 sh /opt/install01.sh 等待自动安装完成
4.  运行 sh /opt/install02.sh 等待自动安装完成

安装完成将自动生成随机用户名和密码，请注意记录。

## 卸载方法

需要远程ssh到 uninstall.sh 文件目录下 运行：
sh uninstall.sh
即可完成卸载。
注意：卸载中由于需要处理之前的文件，全新安装不会有之前旧版的文件，所以提示未找到文件可以忽略提示。

## 使用说明

1.  安装完成后将自动安装成服务，并自动设置为开机启动
2.  浏览器启动 http://ip地址:8000 顺利的话将看到登录界面。
3.  输入安装末尾提示的用户名和密码即可登录

## 调试相关

### 重置密码
1. cd /cosyjieserver/jiesysadmin 进入项目目录
2. python manage.py resetadmin 重置密码，注意会给出原用户名和新用户名，不要复制错误了

### 使用manage.py 调试
1. systemctl stop jiesysadmin.service 关闭服务
2. 进入项目目录
3. sh rundebug.sh 将使用manage.py开发服务器运行

### 使用 gunicorn 显式运行
1. systemctl stop jiesysadmin.service 关闭服务
2. 进入项目目录
3. sh rung.sh 将使用gunicorn运行

## IT阿杰媒体帐号
哔哩哔哩：https://space.bilibili.com/379283376
51CTO: https://edu.51cto.com/lecturer/12831258.html
西瓜视频： https://www.ixigua.com/home/2173081594629741
百家号： https://author.baidu.com/home/1754716766171856
抖音号：itjie

## 授权
 GPL-3.0

