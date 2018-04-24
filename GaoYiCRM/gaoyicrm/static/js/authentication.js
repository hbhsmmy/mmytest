var userNameThere = false;
var idnoExists = false;

$(document).ready(function(){

	$("#user-realName input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-realName input").blur(function(){ inputStyle(this, "blur"); });

	$("#user-cardCode input").focus(function(){ inputStyle(this, "focus"); });
	$("#user-cardCode input").blur(function(){ inputStyle(this, "blur"); });

	$("#step2Back").click(function (){
		// 取消按钮
	});

	$("#step2Btn").click(function (){
		if($("#user-realName input").val() == ""){
			alert("请输入您的真实姓名！");
			return;
		}
		if($("#user-realName input").val().length < 2 || $("#user-realName input").val().length > 30){
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
			alert("您输入的证件号码已注册！");
			return;
		}
		var sendData = {'realname':$("#user-realName input").val(), 'idtype':$("#user-cardType").val(), 'idno':$("#user-cardCode input").val()}

		$.get('/update_identity_card/',sendData,function(ret){
			if(ret.result == "0"){
				alert("认证成功，没有购买产品记录");
			}else{
				alert("认证成功，欢迎查看产品信息");
			}
			window.location.href = "../account_personal";
		});
	});

});

function inputStyle(_this, _style){
	if(_style == "frunocus"){
		showTipsTip(_this);
	}else if(_style == "blur"){

		var _error = $(_this).parent().parent().children(".tip").children(".errorTip");

		if($(_this).parent().attr("id") == "user-realName"){
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
			}else if($(_this).val().length > 20){
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

