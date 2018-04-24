
$(document).ready(function(){

    var swiper = new Swiper('.mb-top-navs', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });


    $("#submitBtn").click(function(){

        if($("#user-name input").val() == ""){
            alert("请输入您的姓名！");
            return;
        }
        if(!checkTxt.regMobile.test($("#user-phone input").val())){
            alert("请输入正确的手机号码！");
            return;
        }
        //if(!checkTxt.emal.test($("#user-email input").val())){
        //    alert("请输入正确的邮箱地址！");
        //    return;
        //}
        //
        if($("#user-message textarea").val()==""){
	      alert("请输入正确的留言！");
              return;
	}

        var sendDate = {"username":$("#user-name input").val(),"mobile":$("#user-phone input").val(),"email":$("#user-email input").val(),"message":$("#user-message textarea").val(),"date":$("#user-date select").val(),"time":$("#user-time select").val()}
        $.getJSON('/leave_message/',sendDate,function(ret){
            alert("留言成功！稍后客服会根据预约时间联系您！");
            $("#user-name input").val("");
    	    $("#user-phone input").val("");
    	    $("#user-email input").val("");
    	    $("#user-message textarea").val("");
        });
    });

    $("#reBtn").click(function(){
    	$("#user-name input").val("");
    	$("#user-phone input").val("");
    	$("#user-email input").val("");
    	$("#user-message textarea").val("");
    });
});




