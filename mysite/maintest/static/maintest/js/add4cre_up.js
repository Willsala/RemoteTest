function getFilename(){
	files=document.getElementById("file").files;
	var fn="";
	for(var i=0;i<files.length;i++){
		if(upload_dir){
			fn=files[i]['webkitRelativePath'];
		}else{
			fn=files[i].name;
		}
		document.getElementById("filename").innerHTML+=fn+"<br>";	
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

function msg_show(message){
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
	},3000);
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

}

function input_property4files(){
	var str = '<input type="file" name="myfile" multiple id="file" onchange="getFilename()" style="display:none" />';
	document.getElementById("insert_input").innerHTML = str;
	
	upload_dir = false;
}