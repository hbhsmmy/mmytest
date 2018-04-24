$(document).ready(function(){

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

    $("#enterBtn").click(function(){
        if(!checkTxt.emal.test($("#user-email input").val())){
            alert("请填写正确的邮箱地址！");
            return;
        }

        $.getJSON('/emailAuthentication/',{'email':$("#user-email input").val()},function(ret){
                if(ret.type == 'success'){
                    alert('邮箱认证成功！')
                }else{
                    alert('邮箱认证失败，请重新尝试！')
                }
                window.location.href = '../account_personal';
            }
        )
    });

});


