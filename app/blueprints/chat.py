# from flask_restful import Resource
from flask import render_template
from flask_socketio import emit

from app.extension import socketio
from flask import Blueprint

chat_bp = Blueprint('chat_bp', __name__)


# socketio.on 装饰器用来注册用于接收客户端发送来事件的事件处理函数
# 这里创建 new message 事件处理函数， 处理客户端发送的new message 事件
# on() 接受的必须参数是函数要监听的时间名称
# @socketio.on('new message')
# def new_message():
#     print('new message')
#     # emit() 函数发送事件
#     # emit() 第一个参数用来指定事件名称，第二个参数是要发送的数据
#     # broadcast 为True时，将事件发送给所有已连接的客户端
#     emit('new message', 'success')

'''
@socketio.on('connect')
def test_connect():
    emit(
        'server_response',
        {'data': 1919}
    )
    # print('connect')
'''

@socketio.on('connect')
def connect():
    """ 服务端自动发送通信请求 """
    
    emit('server_response', {'data': '试图连接客户端！'})
    返回消息信息


@socketio.on('connect_event')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """

    emit('server_response', {'data': message['data']})
    emit('user_response', {'data': message['data']})