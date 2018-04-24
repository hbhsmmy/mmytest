$(document).ready(function(){
    $.getJSON('/chooseUser/',function(ret) {

        for(var i=0;i<ret.investors.length;i++){
            item = ret.investors[i]
            if(i%2==0){
                var con = 'pull-left'
            }else{
                var con = 'pull-right'
            }
            $("#accountAll").append('<li class="'+con+'"><input type="radio" name="account" value="'+item.id+'"><p>姓名：'+item.realname+'</p><p>证件号：'+item.idno+'</p></li>');
        }

        $("#enterBtn").click(function(){
            var value = ''
            var radio=document.getElementsByName("account");
            for(var i=0;i<radio.length;i++){
                if(radio[i].checked==true){
                    value=radio[i].value;
                    break;
                }
            }
            if(value == ''){
                alert('请选择你要查看的账户！');
            }else{
                $.getJSON('/loginPart/',{'id':value},function(ret) {
                    if(ret.success == 1){
                        window.location.href = '../account_home'
                    }else{
                        alert('登录失败，请稍后尝试！')
                    }
                });
            }
        })
    })
});