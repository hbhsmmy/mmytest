$(document).ready(function(){


	if(localStorage.getItem('user') != ''){
		$("#user-name input").val(localStorage.getItem('user'));
	}
	if(localStorage.getItem('pass') != ''){
		$("#user-password input").val(localStorage.getItem('pass'));
	}

	$("#header-logo").click(function(){
		window.location.href="../";
	});

	$("#showNavBtn").click(function (){
		if(!showBoo){
			showNav();
		}else{
			hideNav();
		}
	});

	$(window).keydown(function (e) {
		if (e.which == 13) {
			getInfo();
		}
	});

	$("#changeBtn").click(function(){
		window.location.href='../retrieve'
	})

	$("#loginBtn").click(function(){
		getInfo();
	});
});

function getInfo(){
	if($("#user-name input").val() == ""){
		alert("请输入用户名");
		return;
	}
	if($("#user-password input").val() == ""){
		alert("请输入登陆密码");
		return;
	}

	var userName = $("#user-name input").val();
	var userPassword = $("#user-password input").val();

	getLogin(userName, userPassword);
}

function getLogin(_name, _password){
	var sendData = {'crmuser':_name,'password':_password}
	$.post('/user_login/',sendData,function(ret){
		if(ret.success == 0){
			var rememberBox = document.getElementById('rememberBox');
			if(rememberBox.checked){
				localStorage.setItem("user",_name);
				localStorage.setItem("pass",_password);
			}else{
				localStorage.removeItem("user");
				localStorage.removeItem("pass");
			}
			//window.location.href = '../account_personal';
			//alert(ret.roleList);
			//var AuthorityList = getAuthorityPool(ret.roleList);
			for(var authority in getAuthorityPool(ret.roleList)){
				switch(authority){
					case '0':
						window.location.href = '../account_personal';
						break
					case '1':
						window.location.href = '../account_product';
						break
					case '2':
						window.location.href = '../account_records';
						break
					case '3':
						window.location.href = '../account_inquiry';
						break
					case '4':
						window.location.href = '../account_function';
						break
				}
				break
			}
		}else{
			showStatus();
			$("#user-password input").val("");
		}
	});
}

// 显示错误状态
function showStatus(){
	$("#login-status").css("display", "block");
}


function showNav(){
	showBoo = true;
	$("#showNavBtn-show").animate({"opacity":'0'});
	$("#showNavBtn-hide").animate({"opacity":'1'});
	$("#header-nav-mb").animate({"height":'100%'});
	$("#header-nav-mb-box").animate({"margin-top":'90px'});
}
function hideNav(){
	showBoo = false;
	$("#showNavBtn-show").animate({"opacity":'1'});
	$("#showNavBtn-hide").animate({"opacity":'0'});
	$("#header-nav-mb").animate({"height":'60px'});
	$("#header-nav-mb-box").animate({"margin-top":'0'});
}

function documentTouchmove(e){
	e.preventDefault();
}





