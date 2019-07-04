import multiprocessing
from Users.task_handle import test_pack,minute_process

if __name__ == '__main__':
	pro_1 = multiprocessing.Process(target = minute_process)
	pro_1.start()
	pro_2 = multiprocessing.Process(target = test_pack)
	pro_2.start()
	print("-------------aa-------\n")