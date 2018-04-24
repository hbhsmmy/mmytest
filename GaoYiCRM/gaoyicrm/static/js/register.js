var userNameExists = false;
var phoneExists = false;
var idnoExists = false;
$(document).ready(function(){

	$("#user-name input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-name input").blur(function(){ inputStyle(this, "blur"); });
	$("#user-password1 input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-password1 input").blur(function(){ inputStyle(this, "blur"); });
	$("#user-password2 input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-password2 input").blur(function(){ inputStyle(this, "blur"); });

	$("#user-phone input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-phone input").blur(function(){ inputStyle(this, "blur"); });

	$("#user-realName input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-realName input").blur(function(){ inputStyle(this, "blur"); });

	$("#user-cardCode input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-cardCode input").blur(function(){ inputStyle(this, "blur"); });

	// 获取短信验证码
	var timeBoo = false;
	$("#getCodeBtn").click(function (){
		if(timeBoo){ return; }
		if($("#user-phone input").val() == ""){ alert("请先输入您的手机号码！"); return; }
		if(!checkTxt.regMobile.test($("#user-phone input").val())){ alert("您输入的手机号码有误！"); return; }
		if(phoneExists){ alert("该手机号码注册次数过多！"); return; }

		var time = 60;

		var outTime =  setInterval(function(){
			if( time < 1 ){
				timeBoo = false;
				clearInterval(outTime);
				$("#getCodeBtn").text("获取验证码");
				$("#getCodeBtn").css("background", "#dfb578")
				return;
			}
			timeBoo = true;
			time--;
			$("#getCodeBtn").text("再次获取(" + time + ")");
			$("#getCodeBtn").css("background", "#ccc")
		},1000)

		//发送注册验证短信
		var sendData = {'tag':'1','mobile':$("#user-phone input").val()}
		$.getJSON('/send_code/',sendData, function(ret){
			if(ret.status_code == 200){
				alert("验证码已用短信方式发送到您的手机！");
			}
		});
	});

	$("#registerBtn").click(function (){
		if($("#user-name input").val() == ""){ alert("请输入您的用户名"); return; }
		if($("#user-name input").val().length < 2){ alert("用户名不得少于两位字符！"); return; }
		if($("#user-name input").val().length > 20){ alert("用户名不得多于二十位字符！"); return; }

		if(userNameExists){alert("填写的用户名称已被注册！"); return; }


		if($("#user-password1 input").val() == ""){ alert("请输入您的密码"); return; }
		if($("#user-password1 input").val().length < 8){ alert("密码不能少于8个字符！"); return; }
		if($("#user-password1 input").val().length > 16){ alert("密码不能多于16个字符！"); return; }

		if($("#user-password2 input").val() == ""){ alert("请再次输入您的密码！"); return; }
		if($("#user-password2 input").val() != $("#user-password1 input").val()){ alert("密码同上次输入的不一致，请保持一致！"); return; }

		if($("#user-phone input").val() == ""){ alert("请输入您的手机号！"); return; }
		if(!checkTxt.regMobile.test($("#user-phone input").val())){ alert("您输入的手机号码有误！"); return; }
		if(phoneExists){ alert("您输入的手机号码已被多次注册！"); return; }

		if($("#proving input").val() == ""){ alert("请输入您的短信验证码"); return; }

		if(!$("#agree input").is(':checked')){ alert("请阅读并同意《高毅注册协议》"); return; }

		var sendData = {'mobilecode':$("#proving input").val()}
		$.getJSON('/check_code/',sendData, function(ret){
			if(ret.is_coincident == 1){
				alert("请输入正确的短信验证码");
				return;
			}else{
				var sendData = {'uesrname':$("#user-name input").val(),'password':$("#user-password2 input").val(),'mobile':$("#user-phone input").val(),}
				$.post('/store_info/',sendData,function(){});
				step2();
				$("#stepBox1").css("display", "none");
				$("#stepBox2").css("display", "block");
				$("#register-step div").removeClass("step-on");
				$("#register-step div").eq(1).addClass("step-on");
			}
		});
	});

	$("#step2Back").click(function (){

		$("#register-step div").removeClass("step-on");
		$("#register-step div").eq(0).addClass("step-on");
		step1();
		$("#stepBox1").css("display", "block");
		$("#stepBox2").css("display", "none");
	});

	$("#step2Btn").click(function (){
		if($("#user-realName input").val() == ""){
			alert("请输入您的真实姓名！");
			return;
		}
		if($("#user-realName input").val().length < 2){
			alert("您输入的姓名不合法！");
			return;
		}
		if($("#user-cardCode input").val() == ""){
			alert("请输入您的证件号码！");
			return;
		}
		if($("#user-cardType").val()==0){
			if(!checkTxt.cardCode.test($("#user-cardCode input").val())){
				alert("您输入的证件号码不合法！");
				return;
			}
		}else{
			if($("#user-cardCode input").val().length > 20){
				alert("您输入的证件号码不合法！");
				return;
			}
		}

		if(idnoExists){
			alert("您输入的证件号码已被注册");
			return;
		}

		var sendData = {'realname':$("#user-realName input").val(), 'idtype':$("#user-cardType").val(), 'idno':$("#user-cardCode input").val()}
		$.get('/update_identity_card/',sendData,function(ret){
			if(ret.result == "0"){
				alert("认证成功，没有购买产品记录");
			}
			$("#register-step div").removeClass("step-on");
			$("#register-step div").eq(2).addClass("step-on");
			step3();
			$("#stepBox2").css("display", "none");
			$("#stepBox3").css("display", "block");
		});
	});
});

function step1(){
	$("#jindu").text("已完成0%");
	$("#stepTxt").text("设置账户及密码");
	$("#register-step div").removeClass("step-1");
	$("#register-step div").removeClass("step-2");
	$("#register-step div").removeClass("step-3");
	$("#register-step div").removeClass("step-4");
	$("#register-step div").eq(0).addClass("step-1");
	$("#register-step div").eq(1).addClass("step-2");
	$("#register-step div").eq(2).addClass("step-4");
}
function step2(){
	$("#jindu").text("已完成60%");
	$("#stepTxt").text("填写个人信息");
	$("#register-step div").removeClass("step-1");
	$("#register-step div").removeClass("step-2");
	$("#register-step div").removeClass("step-3");
	$("#register-step div").removeClass("step-4");
	$("#register-step div").eq(0).addClass("step-3");
	$("#register-step div").eq(1).addClass("step-1");
	$("#register-step div").eq(2).addClass("step-4");
}
function step3(){
	$("#jindu").text("已完成100%");
	$("#stepTxt").text("完成注册");
	$("#register-step div").removeClass("step-1");
	$("#register-step div").removeClass("step-2");
	$("#register-step div").removeClass("step-3");
	$("#register-step div").removeClass("step-4");
	$("#register-step div").eq(0).addClass("step-2");
	$("#register-step div").eq(1).addClass("step-3");
	$("#register-step div").eq(2).addClass("step-1");
}

function inputStyle(_this, _style){
	if(_style == "focus"){
		showTipsTip(_this);
	}else if(_style == "blur"){

		var _error = $(_this).parent().parent().children(".tip").children(".errorTip");

		if($(_this).parent().attr("id") == "user-name"){
			// 用户名
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("用户名不能为空！");
			}else if($(_this).val().length < 2){
				showErrorTip(_this);
				_error.children("p").text("用户名不得少于两位字符！");
			}else if($(_this).val().length > 20){
				showErrorTip(_this);
				_error.children("p").text("用户名不得多于二十字符！");
			}else{
				var sendData = {'username':$(_this).val()}
				$.getJSON('/check_name/',sendData,function(ret) {
					if(ret.is_exist == 1){
						userNameExists = true;
						showErrorTip(_this);
						_error.children("p").text("该用户名称已被使用！");
					}else{
						userNameExists = false;
						showOkTip(_this);
					}
				});
			}
		}else if($(_this).parent().attr("id") == "user-password1"){
			// 设置密码
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("请输入您的密码");
			}else if($(_this).val().length < 8){
				showErrorTip(_this);
				_error.children("p").text("密码不能少于8个字符！");
			}else if($(_this).val().length > 16){
				showErrorTip(_this);
				_error.children("p").text("密码不能多于16个字符！");
			}else{
				showOkTip(_this);
			}
		}else if($(_this).parent().attr("id") == "user-password2"){
			// 再次输入密码
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("请再次输入您的密码！");
			}else if($(_this).val() != $("#user-password1 input").val()){
				showErrorTip(_this);
				_error.children("p").text("密码同上次输入的不一致，请保持一致！");
			}else{
				showOkTip(_this);
			}
		}else if($(_this).parent().attr("id") == "user-phone"){
			// 手机号码
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("请输入您的真实手机号码！");
			}else if(!checkTxt.regMobile.test($(_this).val())){
				showErrorTip(_this);
				_error.children("p").text("您输入的手机号码有误！");
			}else{
				var sendData = {'mobile':$(_this).val()}
				$.getJSON('/check_mobile/',sendData,function(ret){
					if(ret.is_repeat == 1){
						phoneExists = true;
						showErrorTip(_this);
						_error.children("p").text('该手机号码注册次数过多！');
					}else{
						phoneExists = false;
						showOkTip(_this);
					}
				});
			}
		}else if($(_this).parent().attr("id") == "user-realName"){
			// 真实姓名
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("请输入您的真实姓名！");
			}else if($(_this).val().length < 2 || $(_this).val().length > 30){
				showErrorTip(_this);
				_error.children("p").text("您输入的姓名不合法！");
			}else{
				showOkTip(_this);
			}
		}else if($(_this).parent().attr("id") == "user-cardCode"){
			// 证件号码
			if($(_this).val() == ""){
				showErrorTip(_this);
				_error.children("p").text("请输入您的证件号码！");
			}else if($(_this).val().length > 30){
				showErrorTip(_this);
				_error.children("p").text("您输入的证件号码不合法！");
			}else{
				if($("#user-cardType").val()=="0"){
					if(!checkTxt.cardCode.test($(_this).val())){
						showErrorTip(_this);
						_error.children("p").text("您输入的证件号码不合法！");
					}else{
						var sendData = {'idno':$(_this).val()}
						$.getJSON('/check_identity_card/',sendData, function(ret){
							if(ret.is_exist == 1){
								idnoExists = true;
								showErrorTip(_this);
								_error.children("p").text("您输入的证件号码已被注册！");
							}else{
								idnoExists = false;
								showOkTip(_this);
							}
						});
					}
				}else{
					var sendData = {'idno':$(_this).val()}
					$.getJSON('/check_identity_card/',sendData, function(ret){
						if(ret.is_exist == 1){
							idnoExists = true;
							showErrorTip(_this);
							_error.children("p").text("您输入的证件号码已被注册！");
						}else{
							idnoExists = false;
							showOkTip(_this);
						}
					});
				}
				//var sendData = {'idno':$(_this).val()}
				//$.getJSON('/check_identity_card/',sendData, function(ret){
				//	if(ret.is_exist == 1){
				//		idnoExists = true;
				//		showErrorTip(_this);
				//		_error.children("p").text("您输入的证件号码已被注册！");
				//	}else{
				//		idnoExists = false;
				//		showOkTip(_this);
				//	}
				//});
			}
		}else{
			if($(_this).val() == ""){
				showErrorTip(_this);
			}else{
				showOkTip(_this);
			}
		}

	}
}

// 显示输入提示
function showTipsTip(_this){
	$(_this).parent().parent().children(".tip").children(".tipsTip").addClass("show");
	$(_this).parent().parent().children(".tip").children(".errorTip").removeClass("show");
	$(_this).parent().parent().children(".tip").children(".okTip").removeClass("show");
}
// 显示输入错误提示
function showErrorTip(_this){
	$(_this).parent().parent().children(".tip").children(".tipsTip").removeClass("show");
	$(_this).parent().parent().children(".tip").children(".errorTip").addClass("show");
	$(_this).parent().parent().children(".tip").children(".okTip").removeClass("show");
}
// 显示输入正确提示
function showOkTip(_this){
	$(_this).parent().parent().children(".tip").children(".tipsTip").removeClass("show");
	$(_this).parent().parent().children(".tip").children(".errorTip").removeClass("show");
	$(_this).parent().parent().children(".tip").children(".okTip").addClass("show");
}

