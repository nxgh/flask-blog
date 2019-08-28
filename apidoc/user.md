## 用户注册

**请求URL:**

 - GET `http://xx.com/user/<string:user_id>`

**简要描述：**

 - 根据用户id返回用户信息


**返回示例**
```json
{
  "username" : "",
  "desc": "",
  "avatar" : "",
  "uid": 0, 
  "topics" : [],
  "photos" : [],
  "follower" : [],
  "followed" : [],
  "comments" : [],
  "collect" : [],
}
```
**返回参数说明**
参考`post /token`


## 用户注册

**请求URL:**

 - POST `http://xx.com/user`

**简要描述：**

 - 用户注册接口

**data/json参数：**

|参数名|	必选|	类型|	说明|
|:---|:---|:---|:---|
|username|	是|	string|	用户名|
|email|	是|	string|	邮箱地址|
|password|	是|	string|	密码|
|location|	否|	string|用户地址位置，由前端发送，用户不需填写|


**返回示例**
 - 状态码: `201`

`"", 201`

**返回参数说明**


## 用户信息操作

**请求URL:**

 - PATCH `http://xx.com/user/<string:user_id>`

**简要描述：**

 - 忘记密码、更改用户信息（邮箱，密码）

**Headers**

|参数名|	必选|	类型|	值|说明|
|:---|:---|:---|:---|:---|
|Authorization|是|str|"JWT token_string"|发送验证token|


**data/json参数：**


|参数名|	必选|	类型|	说明|
|:---|:---|:---|:---|
|username|否|	string|	用户名|
|desc|否|string|	个人简介|
|email|否|string|	邮箱地址|
|password|否|	string|	密码|
|setting|否|array|用户设置|


**返回示例**
 - 描述：json形式返回更新后的用户信息
 - 状态码: `200`

```
user_info
{

}
```


