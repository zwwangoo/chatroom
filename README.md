# chatroom

> 基于python的tornado框架下的即时聊天室
> tornado + redis + mysql

![广场](https://i.loli.net/2017/07/22/597346b254be0.png)
![加入聊天室](https://i.loli.net/2017/07/22/597346b25f4de.png)
![聊天](https://i.loli.net/2017/07/22/597346b27c87f.png)

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

- [官方给的chat示例](https://github.com/tornadoweb/tornado/tree/stable/demos/chat)
- [tornado官方文档(中文)](https://tornado-zh.readthedocs.io/zh/latest/guide.html)
- [ruboob.com(菜鸟教程)redis教程](http://www.runoob.com/redis/redis-tutorial.html)
- [ruboob.com(菜鸟教程)python教程](http://www.runoob.com/python/python-tutorial.html)


---

目前还差当前在线用户的判断没有完成

---
# 完成情况和实现功能说明

- 基于tornado web AJAX的长轮询模式实现的及时在线聊天室
- 实现了基本的异步即时通信的功能、多人在线群聊功能、聊天室创建功能
- 简单练习了tornado的异步非阻塞的概念实现
- 深入学习了tornado web应用的结构和实现

# 不足和可拓展的地方

## 不足
- 长轮询链接断开后无法自动重新连接
- 聊天室人员在线未使用在线状态判断

## 可拓展
- 好友的添加和一对一聊天
- 关注聊天室后，聊天室内容及时推送

---
# 说明：

就做到这了，其他的问题，等以后有兴趣了再来研究吧。加油！