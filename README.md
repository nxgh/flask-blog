## 项目描述

Flask和MongoDB搭建的Web RESTful api，用于搭建个人博客，BBS论坛和基于Socketio的聊天室。

## 目标功能

 - [x] 用户注册
 - [x] 用户登录
 - [x] 邮件验证
 - [x] 文章创建
 - [x] 更新文章
 - [x] 删除文章
 - [x] 文章评论
 - [x] 删除评论
 - [x] 文章分类查询
 - [x] 修改密码
 - [ ] 生成头像
 - [ ] 用户个人中心
 - [ ] 修改个人信息
 - [ ] 用户发帖
 - [ ] 用户回帖
 - [ ] 删除帖子
 - [ ] 创建话题
 
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
