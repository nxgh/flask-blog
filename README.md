## 项目描述

Flask和MongoDB搭建的Web RESTful api，用于搭建个人博客。

## 目标功能

 - [x] 用户注册

 - [x] 用户登录

 - [x] 文章创建

 - [x] 更新文章
 
 - [x] 删除文章
 
 - [x] 文章评论
 
 - [x] 文章分类查询 

 - [] 邮件验证

 - [] 生成头像

 - [] 登录验证码

 - [] 删除评论


# 项目依赖

 - MongoDB

```
flask 
pymongo 
pythodotenv 
flaspymongo 
flasmail 
flasrestful 
webargs 
pyjwt 
flascors 
flassocketio 
eventlet 
```

## 项目运行

```bash
安装虚拟环境
$ cd flask-blog

$ python -m venv venv

$ source venv venv

$ pip install -r requirements.txt

$ flask run
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
[GPL](https://github.com/bailicangdu/vueelm/blob/master/COPYING)



