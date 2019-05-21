from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from Users.models import Users,Invitation,Group

import django.db 
import time
import os
import shutil
import zipfile
#def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.


def sign_up(request):
	return render(request, 'Users/sign_up.html')


def login(request):
	return render(request,"Users/login.html")

def identify(request):

	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		user = Users.objects.filter(username=username).first()		

		if user and user.password == password:
			#
			request.session['username']=user.username
			
			# authority
			# dirs = show_file(user.username)
			# context = {'username': username,'dirs':dirs}
			# return render(request, 'mysite/homepage.html', context)

			return redirect("/maintest/index/")
			# return redirect("/index")
		else:
			return HttpResponse("<script>alert(\"You entered an incorrect user name or password\");window.location.href=\"/Users/login/\";</script>")
	
	else:
		return HttpResponse("<script>window.location.href=\"/Users/login/\";</script>")
		


def add_user(request):
	if request.method == 'POST':

		username = request.POST.get("username",None)
		password = request.POST.get("password",None)
		try:
			user=Users(username=username,password=password)           #<<<<<<<<<<<<--------------------bug----------------
			user.save()
		except django.db.utils.IntegrityError:
			html_add_user_str="<p>"+ username + ''' 
			has been signed up already! Please try another one to <a href="/Users/sign_up/">sign up</a> !</p>

			'''
		else:
			request.session['username']=user.username
			path = "Users/all_users/"+username
			os.mkdir(path)

			html_add_user_str='''
				<p>Successfully sign up! Click <a href="/maintest/index/">here</a> to login</p>

			'''
	else:
		html_add_user_str='''
			<p>failed</p>
		'''
	return HttpResponse(html_add_user_str)





def upload(request):

	username = request.session.get('username',None)
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))	
		file_loc = request.POST.get('file_loc',"/").split("/")
		for iter in file_loc:
			path=os.path.join(path,iter)
		files = request.FILES.getlist("myfile")
		for file in files:
			with open(os.path.join(path,file.name),'wb') as fp:
				for chunk in file.chunks():
					fp.write(chunk)
				fp.close()
				#create_history(username,"upload file",file.name)
		if len(files):
			return JsonResponse({"msg":"Upload successfully! If file is too big, please wait some time and then refresh the page!","type":"s"})
		return JsonResponse({"msg":"Please select files to upload!","type":"w"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})


# def show_file(username):
# 	dirs={}
# 	sec_dir={}
# 	dirs['content']=[]
# 	dirs['dirname']=username
# 	path = "Users/all_users/"+username
# 	dir_list=os.listdir(path)
	
# 	for iter_dir in dir_list:
# 		path_iter = path + "/" +iter_dir
# 		if(os.path.isdir(path_iter)):
# 			#content=os.listdir(path)
# 			# sec_dir['dirname']=iter_dir
# 			# sec_dir['content']=os.listdir(path_iter)
# 			dirs['content'].append({'dirname':iter_dir,'content':os.listdir(path_iter)})
# 		else:
# 			dirs['content'].append(iter_dir)
# 	print(dirs)
# 	return dirs

def mkdir(request):
	username = request.session.get('username',None)
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))
		dir_loc = request.POST.get("dir_loc","/").split("/")
		dir_name = request.POST.get("dir_name",'')
		for iter in dir_loc:
			path = os.path.join(path,iter)
		path = os.path.join(path,dir_name)
		try:
			os.mkdir(path)				
		except OSError:
			return JsonResponse({"msg":"Failed in create!","type":"d"})
		else:
			return JsonResponse({"msg":"Create successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})



	



def logout(request):
	request.session.flush()
	return redirect("/maintest/index/")



def del_file(request):
	username = request.session.get("username",None)
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))	
		loc4del = request.POST.get("loc4del").split("/")
		for iter in loc4del:
			path = os.path.join(path,iter)
		if os.path.isdir(path):
			ls = os.listdir(path)
			for i in ls:
				c_path = os.path.join(path, i)
				if os.path.isdir(c_path):
					shutil.rmtree(c_path,True)
				else:
					os.remove(c_path)
			shutil.rmtree(path,True)
			return JsonResponse({"msg":"delete the dir successfully!","type":"s"})
		else:
			os.remove(path)
			return JsonResponse({"msg":"delete the file successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"d"})


def create_history(username,behavior,filename,tag="0"):
	if tag == "0":
		with open("Users/all_users/%s/%s" % (username,".log.txt"),'a') as fp:
			fp.write(behavior+" | "+filename+" | "+time.asctime(time.localtime(time.time()))+"\n")
		fp.close()
	else:
		with open("Users/all_groups/%s/%s" % (username,".log.txt"),'a') as fp:
			fp.write(behavior+" | "+filename+" | "+time.asctime(time.localtime(time.time()))+"\n")
		fp.close()
	# print "time.time(): %f " %  time.time()
	# print time.localtime( time.time() )
	# print time.asctime( time.localtime(time.time()) )
	
def log(request):
	username = request.session.get("username")
	if username:
		log=[]
		try:
			fp = open("Users/all_users/"+username+"/.log.txt","r")
		except FileNotFoundError:
			log.append("no log information")
		else:
			log=fp.readlines();
			fp.close()
		return JsonResponse({"log":log})
	#else:
		#return HttpResponse("<script>alert(\"Login first!\");window.location.href=\"/Users/login/\";</script>")
		
def invitations(request):
	username = request.session.get("username")
	context = {}
	if username:
		user = Users.objects.get(username = username)
		invitations = user.invitation_set.all().values("inviter_name","group_id","invitee_au","notes")
		context["invitations"] = invitations
		for inv in invitations:
			group = Group.objects.get(group_id=inv["group_id"])
			inv["group_name"] = group.group_name
		return render(request,"Users/invitations.html",context)
	else:
		return redirect('/Users/login/')

def download(request):
	username = request.session.get('username',None)
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))
		loc4down = request.POST.get('loc4down',"/").split("/")
		filename = request.POST.get('file_name4down')
		for iter in loc4down:
			path = os.path.join(path,iter)
		path = os.path.join(path,filename)
		if filename:
			file = open(path,'rb')
		else:
			(path4zip,filename)=zip_dir(path)
			file = open(path4zip,'rb')
		response = FileResponse(file)	
		response['Content-Disposition']='attachment;filename='+'"'+filename+'"'
		return response
	else:
		return redirect('/Users/login/')
	
def zip_dir(dir,flag):
	if dir[-1]==os.sep:
		temp = os.path.split(dir[:-1])         #maybe buggy
	else:
		temp = os.path.split(dir) 
	zipFileName = temp[1]
	zf = zipfile.ZipFile(os.path.join(temp[0],zipFileName+'.zip'), "w", zipfile.ZIP_DEFLATED)
	zip_in(zf,dir,dir,zipFileName,flag)
	zf.close()
	return (os.path.join(temp[0],zipFileName+'.zip'),zipFileName+'.zip')

def zip_in(zf,dir,replace_str,zipFileName,flag="default"):
	dir_list = os.listdir(dir)
	for iter in dir_list:
		path = os.path.join(dir,iter)
		if flag == "default":
			if os.path.isdir(path):
				zf.write(path,os.path.join(zipFileName,path.replace(replace_str,''))+os.sep)
				zip_in(zf,path,replace_str,zipFileName,flag)
			else:
				zf.write(path,os.path.join(zipFileName,path.replace(replace_str,'')))
		elif flag == "trf":
			if os.path.isdir(path):
				#zf.write(path,os.path.join(zipFileName,path.replace(replace_str,''))+os.sep)
				zip_in(zf,path,replace_str,zipFileName,flag)
			else:
				if iter.endswith(".trf"):
					zf.write(path,os.path.join(zipFileName,path.replace(replace_str,'')))
		else:
			if os.path.isdir(path):
				#zf.write(path,os.path.join(zipFileName,path.replace(replace_str,''))+os.sep)
				zip_in(zf,path,replace_str,zipFileName,flag)
			else:
				if iter.endswith("_trf.vcd") or iter.endswith("_merge.vcd") or iter.endswith("_merge.rpt"):
					zf.write(path,os.path.join(zipFileName,path.replace(replace_str,'')))
			

def download_spec(request,flag):
	username = request.session.get('username',None)
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))
		(path4zip,filename)=zip_dir(path,flag)
		file = open(path4zip,'rb')
		response = FileResponse(file)	
		response['Content-Disposition']='attachment;filename='+'"'+filename+'"'
		return response
	else:
		return redirect('/Users/login/')