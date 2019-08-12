from Users.task_handle import addIndb,tfo_parser

import multiprocessing
from random import randint
import os
from Users.models import user_in_queue,Users
from django.db import transaction
from maintest.mytools.batch import report

import time
def RunUserTestRequest(username,tfo_name,project_name):
	request = "" # nothing because we won't record the test info
	path = os.path.join("Users","all_users",username,project_name)
	
	user = Users.objects.get(username=username)
	user_in_queue_item = user_in_queue(user=user,x=1)	
	file_list_list = tfo_parser(path,tfo_name)
	user_or_group = '0'
	report_file = os.path.splitext(os.path.join(path,tfo_name))[0] + '_report.log'

	user_in_queue_item.x = len(file_list_list)
	user_in_queue_item.report_file=report_file
	with transaction.atomic():
		user_in_queue_item.save()
	report(report_file, 'Batch Test for ' + tfo_name)
	
	for iter in file_list_list:
		project_loc = iter[0]
		ptn_name = iter[1][0]		
		dir_list = os.listdir(project_loc)
		input_ptn = ptn_name + ".ptn"
		if input_ptn not in dir_list:
			print("no ptn file called " + input_ptn + " in " + project_loc +". Please check tfo file!")
		addIndb(request,username,project_loc,user_or_group,ptn_name,report_file)
		print("adding "+ username + " " + ptn_name + " to task list.......(Please don't press Ctrl+C)")
	
	print("\n---------------------------\n")
	print("Now you can press Control + C to stop if you want.")
	print("\n---------------------------\n")

class TestRequest(object):
	
	def __init__(self,username,project_name,tfo_dict):
		self.username = username
		self.project_name = project_name
		self.tfo_dict = tfo_dict	
		
def AutoRunUserTestRequest(TestRequest,chance):
	# test every chance minutes
	N = 10297
	tfo_dict = TestRequest.tfo_dict

	print("I'm " + TestRequest.username)
	while True:
		if randint(20000,10000000) % N % chance == 1:
			tfo_name = tfo_dict[randint(1,len(tfo_dict))]
			RunUserTestRequest(TestRequest.username,tfo_name,TestRequest.project_name)
		time.sleep(60)

if __name__ == '__main__':
	testrequest_1 = TestRequest("user_1","TestProject",{1:"Globals.tfo"})
	
	user_2_tfo_dict = {1:"BRAMs.tfo",2:"DSPs.tfo",3:"CLBs.tfo"}
	testrequest_2 = TestRequest("user_2","TestProject",user_2_tfo_dict)
	
	pro_1 = multiprocessing.Process(target = AutoRunUserTestRequest, args = (testrequest_1, 20))
	pro_1.start()
	pro_2 = multiprocessing.Process(target = AutoRunUserTestRequest, args = (testrequest_2, 6))
	pro_2.start()

