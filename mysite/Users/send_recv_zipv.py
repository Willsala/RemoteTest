import os
import hashlib
import time
import zipfile

def sendFile(conn,file):	
	s_time = time.time()
	md5 = 0
	md5_recv = 1
	while md5 != md5_recv:
		ptnfile = "fake"
		if file.endswith('.ptn'):
			ptnfile = file
			file = zip(file)
		size = os.stat(file).st_size  #获取文件大小
		conn.send((file + "+-+-+" + ptnfile + "+-+-+" + str(size)).encode("utf-8"))  # 发送数据长度
		print("发送的大小：", size)

		# 2.发送文件内容
		conn.recv(1024)  # 接收确认

		m = hashlib.md5()

		f = open(file,'rb')
		for chunk in readInChunks(f):
			conn.send(chunk)
			m.update(chunk)
		f.close()

		# 3.发送md5值进行校验
		md5 = m.hexdigest()
		conn.send(md5.encode("utf-8"))  # 发送md5值
		md5_recv = conn.recv(1024).decode("utf-8")
		print("md5: ", md5)
		print("md5_recv: ",md5_recv)
	
	e_time = time.time()
	print("send time: "+str(e_time-s_time))
	with open("log_zipv.txt","a") as fp:
		fp.write(file + " - " + str(e_time - s_time)+"\n")
		fp.close()

	
def recvFile(conn):	
	s_time = time.time()
	md5_origin = 0
	md5_recvfile = 1
	while md5_origin != md5_recvfile:
		received_size = 0
		m = hashlib.md5()
		recvFile, ptnfile, size_str = conn.recv(1024).decode('utf-8').split("+-+-+")
		conn.send(("recv").encode("utf-8"))
		file_size = int(size_str)
		recvFile = recvFile.replace("\\",os.sep)
		recvFile = recvFile.replace("/",os.sep)
		if recvFile.endswith(".ptn"):
			basename= os.path.split(recvFile)[0]
			if not os.path.exists(basename):
				os.makedirs(basename)
		print("recvFile: " + recvFile)
		print("Size of file to recv: " + size_str)
		f = open(recvFile, "wb")
		while received_size < file_size:
			size = 0  # 准确接收数据大小，解决粘包
			preset_size = 1024*1024*2
			if file_size - received_size > preset_size: # 多次接收
				size = preset_size
			else:  # 最后一次接收完毕
				size = file_size - received_size

			data = conn.recv(size)  # 多次接收内容，接收大数据
			data_len = len(data)
			received_size += data_len
			m.update(data)
			f.write(data)
		f.close()
		
		
		if recvFile.endswith(".zip"):
			upzip(recvFile)
			
		md5_origin = conn.recv(1024).decode("utf-8")
		md5_recvfile = m.hexdigest()
		print(md5_origin+"\n"+md5_recvfile)
		conn.send(md5_recvfile.encode("utf-8"))
	
	e_time = time.time()
	print("recv time: "+str(e_time-s_time))
	return ptnfile.replace("\\",os.sep).replace("/",os.sep)
	
def readInChunks(fileObj, chunkSize=1024*1024*2):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.
    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data

def zip(file):
	zipFileName = "whatever"
	zf = zipfile.ZipFile(zipFileName+'.zip', "w", zipfile.ZIP_DEFLATED)
	zf.write(file,file)
	zf.close()
	return zipFileName+'.zip'

def upzip(zipFileName):
	zf = zipfile.ZipFile(zipFileName)
	zf.extractall("./")
