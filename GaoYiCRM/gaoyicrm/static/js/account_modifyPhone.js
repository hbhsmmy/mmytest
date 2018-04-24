var userPhone;
var userPhoneCode;
var step = 1;

$(document).ready(function(){

    $("#enterBtn").click(function(){
        if(step == 1){
            if($("#user-cardCode input").val() == ""){
                alert("请输入您的证件号码！");
                return;
            }
            if($("#user-oldPhone input").val() == ""){
                alert("请输入您的原手机号码！");
                return;
            }
            if($("#user-password input").val() == ""){
                alert("请输入您的登录密码！");
                return;
            }

            var oldPhone = $("#user-oldPhone input").val()
            var password = $("#user-password input").val()
            var cardCode = $("#user-cardCode input").val()
            var sendDate = {"oldPhone":oldPhone,"password":password,"cardCode":cardCode}
            $.post('/modifyPhone1/',sendDate,function(ret){
                if(ret.success == 1){
                    step = 2;
                    $("#inputs1").css("display", "none");
                    $("#inputs2").css("display", "block");
                    $("#enterBtn").text("确认修改");

                }else{
                    alert('信息有误，请重新填写！')
                }

            })
        }else{
            if($("#user-newPhone input").val() == ""){
                alert("请输入您的新手机号码！");
                return;
            }
            if($("#proving-input input").val() == ""){
                alert("请输入验证码！");
                return;
            }

            userPhone = $("#user-newPhone input").val();
            userPhoneCode = $("#proving input").val();

            var sendData = {'mobilecode':userPhoneCode}
            $.getJSON('/check_code/',sendData, function(ret){
                if(ret.is_identical == 1){
                    alert("请输入正确的短信验证码");
                    return;
                }else{
                    alert(userPhone);
                    var sendData = {'phone':userPhone}
                    $.getJSON('/modifyPhone2/',sendData,function(ret){
                        alert("修改成功！");
                        window.location.href="../account_personal";
                    })
                }
            });
        }
    });

    $("#getCodeBtn").click(function(){
        if($("#user-newPhone input").val() == ""){
            alert("请输入您的新手机号码！");
            return;
        }
        if(!checkTxt.regMobile.test($("#user-newPhone input").val())){
            alert("您输入的手机号码有误！");
            return;
        }
        // 这里并不会发送任何信息，需调用接口
        var sendData = {'tag':'2','mobile':$("#user-newPhone input").val()}
        $.getJSON('/send_code/',sendData, function(ret){
            if(ret.status_code == 200){
                alert("验证码已用短信方式发送都您的手机！");
            }
        });
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
    });


    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

});
