$(document).ready(function(){
    var splitOne = window.location.href.split("=")
    if(splitOne.length!=0){
        var code = splitOne[1].split("&")[0];
        var weixinUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxabbc67847011d287&secret=9aa8884e19feb24a21da770983e7a761&code="+code+"&grant_type=authorization_code"
        var sendData = {'weixinUrl':weixinUrl}
        $.getJSON("/weixininfo/",sendData,function(ret){
            $("#userName").text(ret.usernickname);
            document.getElementById("userPic").src = ret.headimgurl;
            if(ret.success == 0){
                window.location.href = '../account_home'
            }
        });
    }

    $("#loginConLeft button").click(function(){
        window.location.href = '../register'
    });

    $("#loginConRight button").click(function(){
        var sendData = {'nameOrMobile':$("#user-name input").val(),'password':$("#user-password input").val()}
        $.post('/bind_weixin/',sendData,function(ret){
            if(ret.success == 0){
                window.location.href = '../account_home';
            }else{
                alert('该账户不存在或密码错误！')
            }
        });
    });

    $("#loginConRight form a").click(function(){
        window.location.href = '../retrieve'
    });
});

