var isLogin = false;
var showBoo = false;

$(document).ready(function(){

	$("#header-zhcx-mb").click(function(){
		$.getJSON('/logout/',function(ret){
			var res = confirm("确定退出的登录页面吗？");
			if(res){
				window.location.href = '../';
			}
		});
	});

	$.getJSON('/loginOrNot/',function(ret){
		if(ret.loginOrNot == '1'){
			isLogin = true;
		}else{
			window.location.href = '../';
		}
		if(isLogin){
			$("#loginOk span").text(ret.username);
			$("#loginOk").css("display", "block");
			$("#header-1-login").css("display", "none");
		}else{
			$("#loginOk").css("display", "none");
			$("#header-1-login").css("display", "block");
		}
		$("#loginOk a").click(function(){
			// 退出
			$.getJSON('/logout/',function(ret){
				window.location.href = '../';
			});
			$("#loginOk").css("display", "none");
			$("#header-1-login").css("display", "block");
		});
	});

	$("#header-zhcx").click(function(){
		// 点击账户查询
		$.getJSON('/loginOrNot/',function(ret){
			if(ret.loginOrNot == '1'){
				window.location.href = ret.url;
			}else{
				alert('请登陆后查看！');
				window.location.href = ret.url;
			}
		})
	});

	$("#header-logo").click(function(){
		window.location.href="../account_personal";
	});

	$("#showNavBtn").click(function (){
		if(!showBoo){
			showNav();
		}else{
			hideNav();
		}
	});

	$("#chinese-versions").click(function(){
		$.getJSON('/changeToChinese',function(ret){
			window.location.href = window.location.href;
		});
	});
	$("#english-versions").click(function(){
		$.getJSON('/changeToEnglish',function(ret){
			window.location.href = window.location.href;
		});
	});

	$("#chinese-versions-mb").click(function(){
		$.getJSON('/changeToChinese',function(ret){
			window.location.href = window.location.href;
		});
	});
	$("#english-versions-mb").click(function(){
		$.getJSON('/changeToEnglish',function(ret){
			window.location.href = window.location.href;
		});
	});

	$("#versions-mb").click(function(){
		$.getJSON('/changeVersions',function(ret){
			window.location.href = window.location.href;
		});
	});

});


function showNav(){
	showBoo = true;
	// document.addEventListener('touchmove', documentTouchmove, false);
	$("#showNavBtn-show").animate({"opacity":'0'});
	$("#showNavBtn-hide").animate({"opacity":'1'});
	$("#header-nav-mb").animate({"height":'100%'});
	$("#header-nav-mb-box").animate({"margin-top":'90px'});
}
function hideNav(){
	showBoo = false;
	// document.removeEventListener('touchmove', documentTouchmove, false);
	$("#showNavBtn-show").animate({"opacity":'1'});
	$("#showNavBtn-hide").animate({"opacity":'0'});
	$("#header-nav-mb").animate({"height":'60px'});
	$("#header-nav-mb-box").animate({"margin-top":'0'});
}

function documentTouchmove(e){
	e.preventDefault();
}
