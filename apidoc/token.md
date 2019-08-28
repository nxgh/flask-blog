## 用户登录

**请求URL:**

 - POST `http://xx.com/token`

**简要描述：**

 - 用户登录接口

**参数：**

|参数名|	必选|	类型|	说明|
|:---|:---|:---|:---|
|email|	是|	string|	邮箱|
|password|	是|	string|	密码|
|remember|	否|	boolean|是否记住登录状态，默认False，有效时间12hours，为True则15天有效|
|location|	否|	string|	用户地址位置，由前端发送，用户不需填写|

**返回示例**
```
{
  "username" : "",
  "email" : "",
  "desc": "",
  "avatar" : "",
  "uid": 0, 
  "topics" : [],
  "photos" : [],
  "follower" : [],
  "followed" : [],
  "comments" : [],
  "collect" : [],
  "login_info": [
      {
      "location" : "",
      "login_time" : datetime.timestamp(datetime.utcnow()),
      }
  ],
}
```
**返回参数说明**

|参数名	|类型	|说明|
|:--|:---|:---|
|desc|str|个人简介|,
|avatar|str|头像地址|,
|uid|int|用户uid|
|topics|[]|发布的帖子|
|photos|[]|发布的图片地址|
|follower|[]|关注我的|
|followed|[]|我关注的|
|comments|[]|用户评论|
|collect |[]|用户收藏|
|login_info|{}|用户登录信息|