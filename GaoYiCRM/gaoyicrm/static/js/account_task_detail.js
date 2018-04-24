var contact_id="";
var client_id="";
$(document).ready(function(){
	contact_id = window.location.href.split("=")[1];
	var sendData = {'contact_id':contact_id};
	$.getJSON('/get_task_detail/',sendData,function(ret){

		$("#client_name").text(ret.customer_name);
		var contact_type = ret.contact_type
		if(contact_type == '' || contact_type == null){
			contact_type = '暂无纪录'
		}else if(contact_type == 1){
			contact_type = '自建待办'
		}else if(contact_type == 2){
			contact_type = '静默回访'
		}else if(contact_type == 10){
			contact_type = '适应性确认'
		}
		$("#contact_type").text(contact_type);
		var client_mobile = ret.customer_mobile;
		if(client_mobile == '' || client_mobile == null){
			client_mobile = '暂无纪录'
		}
		var client_email = ret.customer_email;
		if(client_email == '' || client_email == null){
			client_email = '暂无纪录'
		}
		$("#client_mobile").text(client_mobile);
		$("#client_email").text(client_email);
		$("#date").text(ret.contact_date);
		$("#description").text(ret.contact_detail)

		client_id = ret.client_id;
		$("#quitBtn").click(function () {
			history.go(-1);
		})

		$("#saveBtn").click(function(){
			var details = $('#focuse-message textarea').val();
			if(details == ""){
				alert('请填写纪录');
				return;
			}
			//var time = $('#task-time option:selected').text();
			var sendData = {'contact_id':contact_id,'client_id':client_id,'contact_record':details};
			$.getJSON('/save_contact_record/',sendData,function(ret) {
				if(ret.success == 200){
					window.location.href='../account_personal';
				}
			});
		})
	});
});
