var passwordRight = false;
$(document).ready(function(){
    $("#user-oldPassword input").focus(function(){ inputStyle(this, "focus"); });
    $("#user-oldPassword input").blur(function(){ inputStyle(this, "blur"); });
    $("#user-newPassword1 input").focus(function(){ inputStyle(this, "focus"); });
    $("#user-newPassword1 input").blur(function(){ inputStyle(this, "blur"); });
    $("#user-newPassword2 input").focus(function(){ inputStyle(this, "focus"); });
    $("#user-newPassword2 input").blur(function(){ inputStyle(this, "blur"); });

    $("#enterBtn").click(function(){
        if($("#user-oldPassword input").val() == ""){
            alert("请输入您的原始密码！");
            return;
        }
        if(!passwordRight){
            alert("您输入的原始密码不正确！");
            return;
        }
        if($("#user-newPassword1 input").val() == ""){
            alert("请输入您的新密码！");
            return;
        }
        if($("#user-newPassword1 input").val().length < 8){
            alert("新密码不能少于8个字符！");
            return;
        }
        if($("#user-newPassword1 input").val().length > 16){
            alert("新密码不能多于16个字符！");
            return;
        }
        if($("#user-newPassword2 input").val() != $("#user-newPassword1 input").val()){
            alert("您两次输入的密码不一致！");
            return;
        }

        var sendData = {'password':$("#user-newPassword2 input").val()}
        $.post('/change_password/',sendData,function(ret){
            alert("修改成功！");
            window.location.href="../account_personal";
        });
    });



    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

});



function inputStyle(_this, _style){
    if(_style == "focus"){
        showTipsTip(_this);
    }else if(_style == "blur"){

        var _error = $(_this).parent().parent().children(".tip").children(".errorTip");

        if($(_this).parent().attr("id") == "user-oldPassword"){
            // 原始密码判断
            if($(_this).val() == ""){
                showErrorTip(_this);
                _error.children("p").text("请输入您的原始密码！");
            }else{
                var sendData = {'password':$(_this).val()}
                $.post('/checkPassword/',sendData,function(ret) {
                    if(ret.is_exist == 1){
                        passwordRight = true;
                        showOkTip(_this);

                    }else{
                        userNameExists = false;
                        showErrorTip(_this);
                        _error.children("p").text("您输入的原始密码不正确！");
                    }
                });
            }
        }else if($(_this).parent().attr("id") == "user-newPassword1"){
            // 设置密码
            if($(_this).val() == ""){
                showErrorTip(_this);
                _error.children("p").text("请输入您的新密码！");
            }else if($(_this).val().length < 8){
                showErrorTip(_this);
                _error.children("p").text("密码不能少于8个字符！");
            }else if($(_this).val().length > 16){
                showErrorTip(_this);
                _error.children("p").text("密码不能多于16个字符！");
            }else{
                showOkTip(_this);
            }
        }else if($(_this).parent().attr("id") == "user-newPassword2"){
            // 再次输入密码
            if($(_this).val() == ""){
                showErrorTip(_this);
                _error.children("p").text("请再次输入您的新密码！");
            }else if($(_this).val() != $("#user-newPassword1 input").val()){
                showErrorTip(_this);
                _error.children("p").text("密码同上次输入的不一致，请保持一致！");
            }else{
                showOkTip(_this);
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
