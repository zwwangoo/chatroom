# chatroom

> 基于python的tornado框架下的即时聊天室
> tornado + redis + mysql

## 安装tornado

    pip install tornado

## 安装redis

### windows环境下

点击[这里](https://github.com/MicrosoftArchive/redis/releases )下载

### ubuntu server环境下

    sudo apt-get install redis-server

## 安装 tornado

    pip install tornado-redis
    
## 创建数据库(mysql数据库的安装，这里就不说了)

创建数据库**chatroom**，运行脚本

    python init_mysql.py

添加用户数据在【**user**】表

## demo

访问[这里](http://123.207.146.54:8000/index)查看demo，用户名密码自己注册就行

## 参考

- [tornado官方文档(中文)](https://tornado-zh.readthedocs.io/zh/latest/guide.html)
- [ruboob.com(菜鸟教程)redis教程](http://www.runoob.com/redis/redis-tutorial.html)
- [ruboob.com(菜鸟教程)python教程](http://www.runoob.com/python/python-tutorial.html)


---

目前还差当前在线用户的判断没有完成
