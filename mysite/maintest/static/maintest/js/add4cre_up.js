
function getFilename(){
	files=document.getElementById("file").files;
	var fn="";
	var max = (30 < files.length) ? 30 : files.length;
	for(var i=0;i<max;i++){
		if(upload_dir){
			fn=files[i]['webkitRelativePath'];
		}else{
			fn=files[i].name;
		}
		document.getElementById("filename").innerHTML+=fn+"<br>";	
	}
	if(30 < files.length){
		document.getElementById("filename").innerHTML+="...<br>";
	}
}


function form_submit4reply(obj) { 
	var form_id = "#" + obj.id;

	$(form_id).ajaxSubmit(function(message) { 
		//location.reload();
		msg_show(message);
	}); 
	
	return false; 
}

function msg_show(message,seconds=3){
	var inner = "<div style=\"margin:0px\" class=\"alert ";
	var c_button = " alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\"> &times; </button>";
	if(message.type == "s"){
		inner += "alert-success";
	}else if(message.type == "i"){
		inner += "alert-info";
	}else if(message.type == "w"){
		inner += "alert-warning";
	}else{
		inner += "alert-danger";
	}
	document.getElementById("message").innerHTML = inner + c_button + message.msg + "</div>";
	window.setTimeout(function(){
		$('[data-dismiss="alert"]').alert('close');
	},seconds*1000);
	$("html,body").animate({"scrollTop":top});
	loadTreeview(currentTVPath);
}

function user_submit_pack(obj){
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	return false;
}

function user_submit_pack4up(obj){
	/* var files = obj.files;
	var fd = new FormData; */
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	document.getElementById("filename").innerHTML = "";
	
	return false;
}

function clear_files(){
	document.getElementById("filename").innerHTML="";
}

function del_file4user_pack(obj){
	form_submit4reply(obj);
	$("#myModal_del").modal('hide');
	//window.setTimeout(function(){
	//	getTree();
	//},100);
	
	document.getElementById("loc4del").value = "";
	document.getElementById("file_loc").value = document.getElementById("project4open").value;
	document.getElementById("dir_loc").value = document.getElementById("project4open").value;
	document.getElementById("file_name4down").value = "";
	return false;	
}

function down_file_pack(){
	$("#myModal_down").modal('hide');
}

function input_property4dirs(){
	var str = '<input type="file" name="myfile" webkitdirectory="webkitdirectory" multiple id="file" onchange="getFilename()" style="display:none" />';
	document.getElementById("insert_input").innerHTML = str;
	upload_dir = true;
}

function input_property4files(){
	var str = '<input type="file" name="myfile" multiple id="file" onchange="getFilename()" style="display:none" />';
	document.getElementById("insert_input").innerHTML = str;
	
	upload_dir = false;
}


function upload_ajax(fd){
	var $progressBar = $("#progress-bar");
	$.ajax({
		xhr: function() {
			var xhrobj = $.ajaxSettings.xhr();
			if (xhrobj.upload) {
				xhrobj.upload.addEventListener("progress",
				function(event) {
					var percent = 0;
					var position = event.loaded || event.position;
					var total = event.total;
					if (event.lengthComputable) {
						percent = Math.ceil(position / total * 100);
					}

					// Set the progress bar.
					$progressBar.css({
						"width": percent + "%"
					});
					$progressBar.text(percent + "%");
				},
				false)
			}
			return xhrobj;
		},

		url: "/Users/upload/",
		async: true,
		method: "POST",
		data:fd,
		contentType: false,
		processData: false,
		cache: false,
		success: function(data) {
			fd = new FormData();
			msg_show(data);
			if(data.flag == "ing"){
				var step = 100;
				var total = parseInt(data.total);
				var index = parseInt(data.index);
				var max = (index+step < total) ? step+index : total;
				console.log(max+"--");
				fd.append("total",total);
				fd.append("index",max);
				fd.append("file_loc",data.file_loc);
				for (var i = index; i < max; i++) {
					fd.append("file", files[i]);
					if(upload_dir)
						fd.append("paths", files[i]['webkitRelativePath']);			
				}
				fd.append("upload_time",new Date());
				upload_ajax(fd);
				document.getElementById("file_progress").innerHTML = Math.ceil(max/step)+"/"+Math.ceil(total/step);
			}else{
				loadTreeview(currentTVPath);
				$("#progress").css('display','none');
			}
		}
	});
}

function sleep(ms, callback) {
	setTimeout(callback, ms);
}

function before_upload(){
	var file_loc = $("#file_loc").val();
	clear_files();
	$.ajax({
		url:"/Users/before_upload/",
		async: true,
		method: "POST",
		data:{
			file_loc:file_loc
		},
		success: function(data) {
			if(data.type == 'w'){
				alert(data.msg);
			}
		}
	});
}

