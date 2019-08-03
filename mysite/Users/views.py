from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from Users.models import Users,Invitation,Group
from django.views.decorators.csrf import csrf_exempt
import django.db 
import time
import os
import shutil
import zipfile
from datetime import datetime
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


@csrf_exempt
def before_upload(request):
	username = request.session.get('username',None)
	if username:
		file_loc = request.POST.get("file_loc")
		request.session['file_loc'] = file_loc
		return HttpResponse("whatever")
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})

@csrf_exempt
def upload(request):

	username = request.session.get('username',None)
	data = {}
	flag = ""
	
	GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 '
	if username:
		path = request.session.get('directory',os.path.join("Users","all_users",username))	
		file_loc = request.POST.get('file_loc',"/")
		file_loc_splited= file_loc.split("/")
		index = request.POST.get('index',"0")
		total = request.POST.get('total',"unknown")
		upload_time = request.POST.get('upload_time').split('(')[0]
		print(upload_time)
		print(type(upload_time))
		dat = datetime.strptime(upload_time,GMT_FORMAT)
		a = datetime.now()
		#print(file_loc)
		for iter in file_loc_splited:
			path=os.path.join(path,iter)
		files = request.FILES.getlist("file")
		file_paths = request.POST.getlist("paths")
		# if len(file_paths):
			# i = 0
			# for file in files:
				# abs_path = os.path.join(path,os.sep.join(file_paths[i].split("/")))
				# basename= os.path.split(abs_path)[0]
				# if not os.path.exists(basename):
					# os.makedirs(basename)
				# with open(abs_path,'wb') as fp:
					# for chunk in file.chunks():
						# fp.write(chunk)
					# fp.close()
				# i = i + 1
		# else:
			# for file in files:
				# abs_path = os.path.join(path,file.name)
				# with open(abs_path,'wb') as fp:
					# for chunk in file.chunks():
						# fp.write(chunk)
					# fp.close()
		
		print((datetime.now()-dat).seconds)
		with open("uploadlog.txt","a") as fp:
			fp.write(str(index)+ "/" + str(total)+ "  " +str((datetime.now()-dat).seconds)+" write time:" + str((datetime.now()-a).seconds) +"\n")
		print("write time:" + str((datetime.now()-a).seconds))
		if len(files): 
			data["msg"] = str(index)+ "/" + str(total)+ " upload successfully!"
			data["total"] = total
			data["index"] = index
			data["file_loc"] = file_loc
			if index == total:
				data["type"] = "s"
			else:
				data["type"] = "i"
				data["flag"] = "ing"
				data["msg"] = data["msg"] + "  Please wait!  " +"It took "+ str((datetime.now()-dat).seconds) + " seconds."
			return JsonResponse(data)
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
	
def zip_dir(dir,flag="default"):
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
