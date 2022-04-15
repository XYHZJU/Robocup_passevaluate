import socket

host = socket.gethostname()
address = (host, 9923)
# 创建socket对象，同时设置通信模式，AF_INET代表IPv4，SOCK_STREAM代表流式socket，使用的是tcp协议
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定到我们刚刚设置的ip和端口元组，代表我们的服务运行在本机的9999端口上
server.bind(address)
 
# 开始监听，5位最大挂起的连接数
server.listen(5)
 
 
# 输入问题，得到答案
# input_Q = '23届冬奥会短道速滑1500冠军是谁？'
print("服务启动")
while True:
    print("server waiting")
    # accept()方法被动接受客户端连接，阻塞，等待连接.
    # client是客户端的socket对象，可以实现消息的接收和发送，addr表示客户端的地址
    client, addr = server.accept()
    data = client.recv(1024)  # 代表从发过来的数据中读取1024byte的数据
    input_Q = str(data, encoding='utf-8')
    print(input_Q)