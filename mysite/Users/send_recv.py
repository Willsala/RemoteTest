import os
import hashlib
import time

def sendFile(conn,file):
	s_time = time.time()
	md5 = 0
	md5_recv = 1
	while md5 != md5_recv:
		size = os.stat(file).st_size  #获取文件大小
		conn.send((file + "+-+-+" +str(size)).encode("utf-8"))  # 发送数据长度
		#print("发送的大小：", size)

		# 2.发送文件内容
		conn.recv(1024)  # 接收确认

		m = hashlib.md5()
		# with open(file, "rb") as f:
			# for line in f:
				# conn.send(line)  # 发送数据
				# m.update(line)
			# f.close()
		f = open(file,'rb')
		for chunk in readInChunks(f):
			conn.send(chunk)
			m.update(chunk)
		f.close()

		# 3.发送md5值进行校验
		md5 = m.hexdigest()
		conn.send(md5.encode("utf-8"))  # 发送md5值
		md5_recv = conn.recv(1024).decode("utf-8")
		#print("md5: ", md5)
		#print("md5_recv: ",md5_recv)
	
	e_time = time.time()
	#print("send time: "+str(e_time-s_time))
	with open("log.txt","a") as fp:
		fp.write(file + " - " + str(e_time - s_time)+"\n")
		fp.close()

	
def recvFile(conn):
	md5_origin = 0
	md5_recvfile = 1
	while md5_origin != md5_recvfile:
		s_time = time.time()
		received_size = 0
		m = hashlib.md5()
		recvFile, size_str = conn.recv(1024).decode('utf-8').split("+-+-+")
		conn.send(("recv").encode("utf-8"))
		file_size = int(size_str)
		recvFile = recvFile.replace("\\",os.sep)
		recvFile = recvFile.replace("/",os.sep)
		basename= os.path.split(recvFile)[0]
		if not os.path.exists(basename):
			os.makedirs(basename)
		#print("recvFile: " + recvFile)
		#print("Size of file to recv: " + size_str)
		f = open(recvFile, "wb")
		while received_size < file_size:
			size = 0  # 准确接收数据大小，解决粘包
			preset_size = 1024*1024*25
			if file_size - received_size > preset_size: # 多次接收
				size = preset_size
			else:  # 最后一次接收完毕
				size = file_size - received_size

			data = conn.recv(size)  # 多次接收内容，接收大数据
			data_len = len(data)
			received_size += data_len
			#print("已接收：", int(received_size/file_size*100), "%")
			m.update(data)
			f.write(data)
		md5_origin = conn.recv(1024).decode("utf-8")
		md5_recvfile = m.hexdigest()
		#print(md5_origin+"\n"+md5_recvfile)
		conn.send(md5_recvfile.encode("utf-8"))
		f.close()
	
	e_time = time.time()
	#print("recv time: "+str(e_time-s_time))
	return recvFile
	
def readInChunks(fileObj, chunkSize=1024*1024*25):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.
    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data

