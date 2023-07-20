# jiesysadmin-centos-code

## 介绍
Jiesysadmin centos 是用 Python 开发的，用于部署在centOS中远程管理系统的工具系统

## 注意

本代码不具备生产环境部署条件，请勿用于生产环境和商业环境


## 安装教程

当前为代码仓库。如果要部署请至部署包仓库下载发布包以减少部署时的问题
1.  将所有的文件包和文件都上传到 /opt 目录中
2.  运行 sh /opt/install01.sh，等待自动安装完成
3.  运行 sh /opt/install02.sh 等待自动安装完成

安装完成将自动生成随机用户名和密码，请注意记录。

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


![](readme/network.jpg)

![](readme/process.jpg)
