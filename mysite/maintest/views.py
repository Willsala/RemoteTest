from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os, json, re
from .mytools.patternGen import PatternGen
from .mytools.mytools import VcdFile, vcd_merge
from .vcd2pic_views import vcd2picjson

from Users.task_handle import tfo_parser
import time
from Users.models import user_in_queue,user4serving,Users

# patternGen.prepare()

# define
DONE = 2
LOADING = 1
UNDONE = 0
# end define

# Create your views here.

DIRECTORY = os.path.join(site.storage.location, "Users","all_users")  # /path/to/mysite/uploads/
#DIRECTORY = os.path.join("Users","all_users")
"""
Arithmetic app functions
"""


def _file_process(file, regex):
	dict = {}
	with open(file, "r") as fp:
		for line in fp.readlines():
			# print(line)
			m = regex.match(line)
			if m:
				dict[m.group(1)] = m.group(2)
	return dict


def data_parser(file):
	regex = re.compile(r'(data\d): (\d+)')
	return _file_process(file, regex)


def operator_parser(file):
	regex = re.compile(r'(operator): (0x80{6}\d)')
	return _file_process(file, regex)


def app_execution(data1, data2, operator):
	return_value = os.popen('sudo /BR0101/arith_math/arithmetic_intr_mmap_test_app' + data1 + data2 + operator).read()
	return return_value


def arithmetic_app(request):
	# TODO: ugly code.
	dataFile = os.path.join(DIRECTORY, "myTest/data")
	operatorFile = os.path.join(DIRECTORY, "myTest/operator")
	dataDict = data_parser(dataFile)
	operator = operator_parser(operatorFile)['operator']
	result = app_execution(dataDict['data1'], dataDict['data2'], operator)
	# result = app_execution(dataDict["data1"], dataDict["data2"], operator)
	return HttpResponse(result)


"""
Main test template
"""


def treeview_parser(root='', abspath='', relpath='', flag='C'):
	"""
	According to the given root, traverse its file tree and return a json object.
	:param root:
	:param abspath:
	:param flag: 'C'-> Complete file tree, 'O'-> file tree used in open project
	:return:
	"""
	dataList = []
	path = os.path.join(DIRECTORY, root)
	filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
	for item in filelisting.listing():
		fileobject = FileObject(os.path.join(path, item))
		newabspath = os.path.join(abspath, item)
		# print(newabspath)
		if flag == 'O':
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-folder-close",
				# "selectedIcon": "glyphicon glyphicon-folder-open",
				"nodes": treeview_parser(fileobject.path_relative_directory, newabspath, flag=flag),
				"href": reverse('maintest:index') + "?path=" + newabspath
			})
		elif fileobject.is_folder:  # and not fileobject.is_empty:
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-folder-close",
				# "selectedIcon": "glyphicon glyphicon-folder-open",
				"nodes": treeview_parser(fileobject.path_relative_directory, newabspath, flag=flag)
			})
		elif flag == 'C':
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-file",
				"href": reverse('maintest:index') + "?file=" + newabspath + "&path=" + relpath
				# "href": "#edit-text"
			})
	return dataList


def clr_status(request):
	for item in request.session['stream_status']:
		item[1] = UNDONE


def file_check(request):
	pass


def syntax_check(request):
	pass


def check(request):
	query = request.GET
	# self.tfo_path = os.path.join(DIRECTORY, query.get('path', ''))
	request.session['tfo_path'] = request.session['directory']
	request.session['tfo_name'] = query.get('tfo', '')
	print('tfo_path =', request.session['tfo_path'])
	print('tfo_name =', request.session['tfo_name'])
	# tfo_file = 'tfo_demo.tfo'
	# TODO: Check file integrity and syntax.
	if(not request.session['tfo_name'].endswith(".tfo")):
		return JsonResponse({"msg":"please choose a tfo file!","type":"w"})
	file_list_list = tfo_parser(request.session['tfo_path'],request.session['tfo_name'])
	for iter in file_list_list:
		project_loc = iter[0]
		ptn_name = iter[1][0]
		if os.path.isdir(project_loc):
			dir_list = os.listdir(project_loc)
			input_ptn = ptn_name + ".ptn"
			if input_ptn not in dir_list:
				msg = "no ptn file called " + input_ptn + " in " + project_loc +". Please check tfo file!"
				type = "w"
				request.session['stream_status'][0][1] = UNDONE
				return JsonResponse({"msg":msg,"type":type})
		else:
			msg = "There is no directory called "+ project_loc.split(os.path.join("all_users",request.session.get("username","None")))[1]+"!!!"
			type = "d"
			request.session['stream_status'][0][1] = UNDONE
			return JsonResponse({"msg":msg,"type":type})
			
	request.session['stream_status'][0][1] = DONE  # Check status
	
	return JsonResponse({"msg":"check pass","type":"s"})


def build(request):
	from maintest.mytools.batch import batch_build
	query = request.GET
	path = query.get('path', '')
	print('initialization success!')
	tfo_path = request.session['tfo_path']
	tfo_name = request.session['tfo_name']
	print('path = {}\ntfo = {}'.format(tfo_path, tfo_name))
	batch_build(tfo_path, tfo_name)
	print('write success!')
	request.session['stream_status'][1][1] = DONE  # Build status
	return HttpResponse("Build Success!")


def test(request):
	from maintest.mytools.batch import batch_test
	try:
		tfo_path = request.session['tfo_path']
		tfo_name = request.session['tfo_name']
		print('path = {}\ntfo = {}'.format(tfo_path, tfo_name))
		batch_test(tfo_path, tfo_name)
		request.session['stream_status'][2][1] = DONE
		return HttpResponse('Test Success!')
	except Exception as err:
		return HttpResponse(err)


def report(request):
	from maintest.mytools.batch import batch_trf2vcd, batch_merge
	try:
		tfo_path = request.session['tfo_path']
		tfo_name = request.session['tfo_name']
		print(tfo_path, tfo_name)
		batch_trf2vcd(tfo_path, tfo_name)
		batch_merge(tfo_path, tfo_name)
		request.session['stream_status'][3][1] = DONE
		return HttpResponse('Report ready!')
	except Exception as err:
		return HttpResponse(err)


def treeview_ajax(request):
	username = request.session.get("username",None)
	if username:
		query = request.GET
		query_dir = query.get('dir', '')
		query_flag = query.get('flag', '')
		path = os.path.join(DIRECTORY, username ,query_dir)
		request.session['directory'] = path  # change root directory of the page
		# print('ajax_path', request.session['directory'])
		request.session['project_name'] = query_dir
		#request.session['wave_path'] = os.path.join(site.storage.location, "maintest/static/maintest/img", username ,query_dir)
		#request.session['wave_path'] = os.path.join("maintest/static/maintest/img", username ,query_dir)
		clr_status(request)
		# if not os.path.exists(request.session['wave_path']):
			# os.mkdir(request.session['wave_path'])
		result = treeview_parser(path, flag=query_flag)
	else:
		result = [{"text":"login first!"}]
	return HttpResponse(json.dumps(result), content_type='application/json')
	


def edit_file(file_path):
	import binascii
	if os.path.isfile(file_path):
		with open(file_path, 'rb+') as f:
			content = f.read()
			if os.path.splitext(file_path)[1] == '.ptn':
				pattern = re.compile('.{32}')
				content = str(binascii.hexlify(content)).lstrip("b'").upper()
				content = '\t'.join(re.findall(r'.{4}', content))
				content = '\n'.join(re.findall(r'.{40}', content))
		# print(type(content))
		return content
	else:
		return "edit your file here."


@csrf_exempt  # WTF
def save_file(request):
	if request.method == 'POST':
		try:
			# print(request.POST)
			content = request.POST['text']
			path = request.POST['path']
			with open(path, 'w') as f:
				f.write(content)
			return HttpResponse("Success!")
		except Exception as exc:
			return HttpResponse(exc)


def index(request):
	"""
	:param request:
	:return: file path,
	"""
	# initialize session
	status = [
		["Check", UNDONE],
		["Build", UNDONE],
		["Test", UNDONE],
		["Report", UNDONE]
	]
	request.session.setdefault('stream_status', status)
	username = request.session.get("username",None)
	if username:
		
		request.session.setdefault('directory', os.path.join(DIRECTORY,username))
		query = request.GET
		query_file = query.get('file', 'open file')
		# print('query_file(in index)=', query_file)
		directory = request.session.get('directory', username)
		file_path = os.path.join(directory, query_file)
		# print('file_path(in index)=', file_path)
		# print(query_file, file_path)
		query_path = query.get('path', '')
		obj = treeview_parser(directory, relpath=query_path)

		# print(obj)
		tv_dir = treeview_parser(os.path.join(DIRECTORY, username), flag='O')
		# print(self.directory)
		#wave_path = os.path.join('maintest/static/maintest/img', username, '/wave.jpg')
		return render(request, 'maintest/test.html', {
			'DIRECTORY': DIRECTORY,
			'current_path': username,   # directory is Bad URL
			'file_content': edit_file(file_path),  # file to display in <textarea>
			'file_path': file_path,  # path of the above
			'file_name': query_file,
			# 'wave_path': request.session.get("wave_path",wave_path),  # can't deal with it
			'obj': json.dumps(obj),  # default treeview object
			'tv_dir': json.dumps(tv_dir),
			'stream_status': request.session.get('stream_status', []),  # stream status
			'username':username,
		})
	else:
		return render(request, 'maintest/test.html', {
			'stream_status': request.session.get('stream_status', [])  # stream status
		})

def status4user_get(request):
	return render(request, 'maintest/include/stream_status.html',{'stream_status':request.session['stream_status']})

def testProgressQuery(request):
	percent = 0
	sum = 0
	done = 0
	username = request.session.get("username")
	time.sleep(2)
	if username:
		user = Users.objects.get(username = username)
		use_in_queue_item_set = user_in_queue.objects.filter(user=user)
		user4serving_item_set = user4serving.objects.filter(user=user)
		for item in use_in_queue_item_set:
			sum += item.x
		for item in user4serving_item_set:
			sum += item.x
			done += item.x - item.x_current		
		if sum == 0:
			request.session['stream_status'][2][1] = DONE			
			percent = 100
		else:
			percent = int(done/sum*100)
		
	return JsonResponse({"percent":percent})
	
