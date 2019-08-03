import hashlib
import time
from datetime import datetime
import sys
import shutil
import os
import re

def trf_compare(originFile,newFile):
	#s_time = time.time()
	msg = "same"
	md5_ori = md5_calc(originFile)
	md5_new = md5_calc(newFile)
	print(originFile)
	print(newFile)
	print("md5_ori:" + md5_ori)
	print("md5_new:" + md5_new)
	if md5_ori != md5_new:
		msg = "diff"
		shutil.copy(newFile,os.path.join('trf_diffs',re.sub(r'[.:\s-]','_',str(datetime.now())) + "_" + newFile.split(os.sep)[-1]))
	with open("robust_test_log.txt","a") as fp:
		fp.write(newFile + " " + msg +"\n")
		fp.close()
	#e_time = time.time()
	#print("time :" + str(e_time-s_time) + " seconds.")
				
	
def md5_calc(file):
	md5_result = hashlib.md5()
	with open(file,'rb') as fp:	
		data = fp.read()
		md5_result.update(data)
		fp.close()
	return md5_result.hexdigest()
	
	
#if __name__ == "__main__":
#	if len(sys.argv) == 3:
#		trf_compare(sys.argv[1],sys.argv[2])
#	else:
#		print("Please input two files(with their path)!")
		

