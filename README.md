## 项目描述

Flask和MongoDB搭建的Web RESTful api，用于搭建个人博客，论坛和基于Socketio的聊天室。

DB
- MongoDB - PyMongo
- MySQL - SQLAlchemy
- Redis

## 目标功能



 - [] 用户注册
  - 分为两类，用户评论时允许不注册评论，自动建立账号不验证邮箱，权限为 unchecked-user
  - 通过 /login 注册的用户，需要验证邮箱，权限为 checked-user
  - 用户权限分为管理员、协管员、未验证用户、验证用户、匿名。协管员权限由管理员指定
   - 未验证用户 文章评论，聊天限制五句
   - 验证用户 论坛发布话题/文章，聊天室自由讨论
   - 管理员在程序初始化过程中创建

 - [] 用户登录
  - 第三方登录 QQ Github
 - [] 邮件验证

 - [] 生成头像
 - [] 用户个人中心
  - 用户关注列表
 - [] 修改个人信息
  - 修改密码、头像、邮箱、关注列表
 - [] 登录验证码
 - [] 关注用户

 博客 模仿简书
 - [] 文章创建
 - [] 更新文章
 - [] 删除文章

 - [] 文章评论
 - [] 删除评论
 - [] 文章分类查询 

 论坛 模仿知乎
 - 用户权限
  - 管理员
  - 协管员
  - 用户 
  - 匿名
 - [] 用户发帖、创建话题
 - [] 用户回帖、创建回答、回答评论
 - [] 删除帖子、删除帖子回复、删除回答

 聊天室 (websocket) QQ群
 - [] simple 聊天室

## TODOS
 - webargs 表单验证
 - flask 命令
 - 单元测试
 - api文档
 - sentry 日志

# 项目依赖
```
flask 
pymongo 
python-dotenv 
flask-pymongo 
flask-mail 
flask-restful 
webargs 
pyjwt 
flask-cors 
flask-socketio 
eventlet 
```

## 项目运行

```bash
安装虚拟环境
$ pip install pipenv

$ git clone https://github.com/nxgh/Herba.git

$ cd Herba

$ pipenv install 

$ pipenv shell

```

配置环境变量
```
.env

MAIL_SERVER=
MAIL_USERNAME=
MAIL_PASSWORD=
APP_EMAIL=
APP_AUTHOR=
MONGODB_URI=
SECRET_KEY=
```
运行
```
$ flask run
```


## License
[GPL](https://github.com/bailicangdu/vue2-elm/blob/master/COPYING)




## 测试

[√] 用户注册 - 创建用户
```
测试账户 密码            邮箱                   权限
Test0   Password_123    test0@foxmail.com     Admin
Test1   Password_123    test1@foxmail.com     User
Test2   Password_123    test2@foxmail.com     User
Test3   Password_123    test3@foxmail.com     User
```

