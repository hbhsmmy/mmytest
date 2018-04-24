
$(document).ready(function(){

	$(".footer-navs div").eq(3).children("a").eq(0).click(function(){
		// 页面底部PC端了解产品点击
		//alert('数据整合中，敬请期待！');
		//$.getJSON('/loginOrNot/',function(ret){
		//	if(ret.loginOrNot == '1'){
		//		window.location.href = '../account_product/manager=managerZero';
		//	}else{
		//		alert('请登陆后查看！');
		//		window.location.href = ret.url;
		//	}
		//})
	});

	$("#footer-3 .content a").eq(3).click(function(){
		// 页面底部手机端了解产品点击
		//alert('数据整合中，敬请期待！');
		//$.getJSON('/loginOrNot/',function(ret){
		//	if(ret.loginOrNot == '1'){
		//		window.location.href = '../account_product/manager=managerZero';
		//	}else{
		//		alert('请登陆后查看！');
		//		window.location.href = ret.url;
		//	}
		//})
	});

});
