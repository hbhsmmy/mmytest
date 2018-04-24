var userName;
var userPass;
var newPassword;
var step = 1;

$(document).ready(function(){

	$("#header-logo").click(function(){
		window.location.href="../";
	});

	$(window).keydown(function (e) {
		if (e.which == 13) {
			if(step == 1){
				step1();
			}
			if(step == 2){
				step2();
			}
			if(step == 3){
				window.location.href="../";
			}
		}
	});

	// 步骤一提交
	$("#step1Btn").click(function (){
		step1();
	});

	// 步骤二提交
	$("#step2Btn").click(function(){
		step2();
	});

	$("#step3Btn").click(function(){
		window.location.href="../";
	});
});

function step1(){
	if($("#user-name input").val() == ""){
		alert("请输入您的姓名");
		return;
	}
	if($("#user-pass input").val() == ""){
		alert("请输入您的密码");
		return;
	}
	userName = $("#user-name input").val();
	userPass = $("#user-pass input").val();

	var sendData = {'crmuser':userName,'password':userPass}
	$.post('/user_login/',sendData,function(ret){
		if(ret.success == 0){
			$("#retrieve-step1").css("display","none");
			$("#retrieve-step2").css("display","block");
			$("#user-name2 p").text(userName);
			step = 2;
		}else{
			alert('您输入的用户名或密码错误！');
		}
	});
}
function step2(){
	if($("#user-password1 input").val() == ""){
		alert("请输入您的新密码并且不能少于8位大于16位");
		return;
	}
	if($("#user-password1 input").val().length < 8){
		alert("您的新密码不能少于8位");
		return;
	}
	if($("#user-password1 input").val().length > 16){
		alert("您的新密码不能大于16位");
		return;
	}
	if($("#user-password2 input").val() == ""){
		alert("请再次输入您的新密码");
		return;
	}
	if($("#user-password1 input").val() != $("#user-password2 input").val()){
		alert("您输入的密码不一致 请重新输入");
		return;
	}
	newPassword = $("#user-password1 input").val();

	var sendData = {'username':userName,'password':newPassword}
	$.post('/update_password/',sendData,function(ret){
		if(ret.success == 0){
			$("#retrieve-step2").css("display","none");
			$("#retrieve-step3").css("display","block");
			step = 3;
		}else{
			alert('修改失败，请再次尝试或联系IT部门！')
		}
	});
}