import socket
 
client = socket.socket()
 
# 连接服务器
host = socket.gethostname()
print(host)
addr = (host, 9923)
client.connect(addr)
 
data = 'hello,123'
# 发送数据
client.send(data.encode('utf-8'))
 
client.close()

