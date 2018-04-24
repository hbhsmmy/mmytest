var message_id="";
var client_id="";
$(document).ready(function(){
	message_id = window.location.href.split("=")[1];
	var sendData = {'message_id':message_id};
	$.getJSON('/get_detail_message/',sendData,function(ret){

		$("#client_name").text(ret.message_username);
		var message_time = ret.message_time.substr(0,10) + ' ' +ret.message_time.substr(11,5);
		$("#message_time").text(message_time);
		var client_mobile = ret.message_mobile;
		if(client_mobile == '' || client_mobile == null){
			client_mobile = '暂无纪录'
		}
		var client_email = ret.message_email;
		if(client_email == '' || client_email == null){
			client_email = '暂无纪录'
		}
		$("#client_mobile").text(client_mobile);
		$("#client_email").text(client_email);
		$("#date").text(ret.contact_date);
		$("#description").text(ret.message)

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
			var sendData = {'message_id':message_id,'revert_record':details};
			$.getJSON('/save_revert_record/',sendData,function(ret) {
				if(ret.success == 200){
					window.location.href='../account_inquiry';
				}
			});
		})
	});
});
