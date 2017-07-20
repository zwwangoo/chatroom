# chatroom

> 基于python的tornado框架下的即时聊天室
> tornado + redis + mysql

## 安装tornado

    pip install tornado

## 安装redis

### windows环境下

点击[这里](https://github.com/MicrosoftArchive/redis/releases )下载

## 安装 tornado

    pip install tornado-redis
    
## 创建数据库(mysql数据库的安装，这里就不说了)

创建数据库**chatroom**，运行脚本

    python init_mysql.py

添加用户数据在【**user**】表

## 参考

- [tornado官方文档(中文)](https://tornado-zh.readthedocs.io/zh/latest/guide.html)
- [ruboob.com(菜鸟教程)redis教程](http://www.runoob.com/redis/redis-tutorial.html)
- [ruboob.com(菜鸟教程)python教程](http://www.runoob.com/python/python-tutorial.html)