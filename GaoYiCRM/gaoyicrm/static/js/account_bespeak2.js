var jiaoyiType = ""; // 记录交易类型
var phoneType = ""; // 联系电话类型
var phone = ""; // 联系电话

$(document).ready(function(){

    $.getJSON('/get_bespeak/',function(ret){
        $("#bespeak-content-fundname span").html(ret.fundName);
        $("#user-phone1 em").text(ret.mobile);
    })

    $("#confirmBtn").click(function(){
        //if(!$("#agree input").is(':checked')){
        //    alert("请勾选愿意接受高毅最新的产品和活动的最新通知！");
        //    return;
        //}
        phoneType = getTransactionType("transactionType1"); //联系电话类型
        if(phoneType == "预留手机号"){
            phone = $("#user-phone1 em").text();
        }else{
            if($("#user-phone input").val() == ""){
                alert("请输入您的联系电话！");
                return;
            }else{
                phone = $("#user-phone input").val();
            }
        }

        //当符合条件后执行以下代码
        jiaoyiType = getTransactionType("transactionType"); //获取交易类型

        if(!checkTxt.regMobile.test(phone)){ alert("您输入的手机号码有误！"); return; }

        var sendDate = {
            'mobile':phone,
            'inquirytype':jiaoyiType,
            'message':$("#user-message textarea").val(),
            "date":$("#user-date select").val(),
            "time":$("#user-time select").val()}
        alert(sendDate);
        $.getJSON('/store_inquery/',sendDate,function(ret){
            alert("预约成功！");
            window.location= '../account_inquiry/';
        })

    });

    $("#reBtn").click(function(){
        window.location.reload();
    });

    $("#filter-mb-btn1").click(function(){
        $("#filter-mb-cp").slideToggle();
    });
    $("#filter-mb-btn2").click(function(){
        $("#filter-mb-px").slideToggle();
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });
});

function checkLength(gm) {
    var maxChars = 140;
    if (gm.value.length > maxChars){
        gm.value = gm.value.substring(0,maxChars);
    }
    var curr = maxChars - gm.value.length;
    document.getElementById("leftnum").innerHTML = "还可输入"+curr.toString()+"字";
}

// 获取交易类型
function getTransactionType(type){
    var value="";
    var radio=document.getElementsByName(type);
    for(var i=0;i<radio.length;i++){
        if(radio[i].checked==true){
            value=radio[i].value;
            break;
        }
    }
    return value;
}

