## 开发数据库
username: herba_dev
password: password

## 测试数据库
username: herba_test
password: password


## 数据模型
```py
User = {
        "username" : "",
        "password_hash" : "", 
        "email" : "",
        "avatar" : "", # 头像 URL
        "uid": "", 
        "desc": "",   # 简介
        "posts": [Post.ObjectId]
        "topics" : [Topic.ObjectId], # 帖子
        "photos" : [Photo.ObjectId], # 分享图片
        "collect_posts": [Post.ObjectId]
        "collect_topics" : [Topic.ObjectId],
        "collect_photos" : [Photo.ObjectId], # 收藏图片
        "permission" : ["USER", "ADMIN", "Moderator"],
        "follower" : [User.ObjectId],
        "followed" : [User.ObjectId],
        "comments" : [], 
        "location" : "",  # 上次登录位置
        "login_time" : "", # 上次登录时间
        "locket" : bool, # 账号锁定状态
}

Posts = {
    "title": "",
    "body":"",
    "comments": [
        {
            "username": User.name,
            "body": "",
            "replay": []
        }
    ],
    "category": "",
    "can_comment": bool
    "Tags": []
}

Topics = {
    "title": "",
    "desc": "",
    "comments": [
        {
            "floor": int,
            "user": ["username", "avatar", "desc"],
            "body": "",
            "timestamp": "",
            "like": int,
        }
    ]
}

Photos = {
    "desc": "",
    "filename":"",
    "author": "",
    "stars": "",
    "comment": [],
    "tags": []
}

```

用户相关

注册
'/singup'
post /user
{
    username:"",
    email:"",
    password:"",
    location:"",
}

登录
'login'
post /token
{
    email: "",
    password:"",
    location:"",
}
return {
    user_info
}


更改资料
patch /user?type=email # 更改邮箱
patch /user?type=pwd # 忘记/更改密码

注销
delete /user


用户主页
get /user/<string:user_id>
return {
    user_info
}