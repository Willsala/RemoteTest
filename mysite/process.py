import multiprocessing
from Users.task_handle import test_pack,minute_process
import os

if __name__ == '__main__':
	abc = os.popen("sudo /home/linaro/BR0101/z7_v4_com/z7_v4_ip_sysrst").read()
	print(abc)
	pro_1 = multiprocessing.Process(target = minute_process)
	pro_1.start()
	pro_2 = multiprocessing.Process(target = test_pack)
	pro_2.start()
	print("-------------aa-------\n")
