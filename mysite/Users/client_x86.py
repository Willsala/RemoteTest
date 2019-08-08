# 客户端

import socket
import os
import hashlib
from .send_recv_zipv import sendFile,recvFile

def client_test(file):
	#ip = 'localhost'
	ip = "192.168.67.3"
	client = socket.socket()  # 生成socket连接对象
	ip_port =(ip, 6969)  # 地址和端口号
	client.connect(ip_port)  # 连接
	print("Connected to server!")
	
	sendFile(client,file)
	recvFile(client)
	client.close()
	
	
	
if __name__ == '__main__':
	client_test("Users/all_users/user_3/adder.ptn")
