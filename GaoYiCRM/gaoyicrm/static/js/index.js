var bannerId = 0;

$(document).ready(function(){

	function keyLogin(){
		//if (event.keyCode==13){
		//	if($("#user-name input").val() == ""){
		//		alert("请输入您的账号！");
		//		return;
		//	}
		//	if($("#user-password input").val() == ""){
		//		alert("请输入您的密码！");
		//		return;
		//	}
        //
		//	var sendData = {'nameOrMobile':$("#user-name input").val(),'password':$("#user-password input").val()}
		//	$.post('/user_login/',sendData,function(ret){
		//		if(ret.success == 0){
		//			$("#loginBox").css("display", "none");
		//			window.location.href = '../account_home';
		//		}else{
		//			alert("您输入的账号或密码错误！");
		//			$("#user-password input").val("");
		//		}
		//	});
		//}
	}

	$.getJSON('/loginOrNot/',function(ret){
		if(ret.loginOrNot == '1'){
			$("#loginBox").css("display", "none");
		}
	});

	$("#shejiao_weixin").click(function(){
		window.location.href = "https://open.weixin.qq.com/connect/qrconnect?appid=wxabbc67847011d287&redirect_uri=http://www.gyasset.com:8080/bespeak&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"
	});

	initPcBanner();
	$("#loginBtn").click(function(){
		if($("#user-name input").val() == ""){
			alert("请输入您的账号！");
			return;
		}
		if($("#user-password input").val() == ""){
			alert("请输入您的密码！");
			return;
		}

		var sendData = {'nameOrMobile':$("#user-name input").val(),'password':$("#user-password input").val()}
		$.post('/user_login/',sendData,function(ret){
			if(ret.success == 0){
				$("#loginBox").css("display", "none");
				window.location.href = '../account_home';
			}else{
				alert("您输入的账号或密码错误！");
				$("#user-password input").val("");
			}
		});
	});


	var swiper = new Swiper('.swiper-container', {
		loop : true,
		pagination : '.swiper-pagination'
	});

});


function initPcBanner(){

	$("#pc-banner-picCon li").css("left", "100%");
	$("#pc-banner-picCon li").eq(0).css("left", "0");

	var dian = "";
	for (var i = 0; i < $("#pc-banner-picCon li").length; i++) {
		dian = dian + '<li class="pull-left"><img src="../static/img/global/dian.png" alt=""></li>';
	};
	$("#pc-banner-dianCon").empty();
	$("#pc-banner-dianCon").append(dian);
	$("#pc-banner-dianCon li").eq(0).children("img").attr("src", "../static/img/global/dian2.png");

	$("#leftJt").click(function(){
		var thisBannerId = bannerId;
		bannerId--;
		if(bannerId < 0){
			bannerId = $("#pc-banner-picCon li").length - 1;
		}
		$("#pc-banner-picCon li").eq(bannerId).css("left", "-100%");
		$("#pc-banner-picCon li").eq(thisBannerId).animate({left:'100%'});
		$("#pc-banner-picCon li").eq(bannerId).animate({left:'0'});
		$("#pc-banner-dianCon li").children("img").attr("src", "../static/img/global/dian.png");
		$("#pc-banner-dianCon li").eq(bannerId).children("img").attr("src", "../static/img/global/dian2.png");
	});
	$("#rightJt").click(function(){
		var thisBannerId = bannerId;
		bannerId++;
		if(bannerId > $("#pc-banner-picCon li").length - 1){
			bannerId = 0;
		}
		$("#pc-banner-picCon li").eq(bannerId).css("left", "100%");
		$("#pc-banner-picCon li").eq(thisBannerId).animate({left:'-100%'});
		$("#pc-banner-picCon li").eq(bannerId).animate({left:'0'});
		$("#pc-banner-dianCon li").children("img").attr("src", "../static/img/global/dian.png");
		$("#pc-banner-dianCon li").eq(bannerId).children("img").attr("src", "../static/img/global/dian2.png");
	});
}




