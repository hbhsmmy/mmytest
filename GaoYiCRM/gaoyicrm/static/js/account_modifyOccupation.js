
$(document).ready(function(){


    $("#enterBtn").click(function(){
        if($("#user-occupation input").val() == ""){
            alert("请填写您的职业!");
            return;
        }
        var userEducation = $("#user-education select").val();//用户选择的学历
        var userOccupation = $("#user-occupation input").val();//用户填写的职业

        if(userOccupation.length > 30){
            alert('您输入的职业格式不合法！')
            return;
        }
        var sendData = {
            'education': userEducation,
            'occupation': userOccupation,
        }

        $.getJSON('/modifyOccupation/', sendData, function(ret){
            window.location.href="../account_personal";
        });

    });



    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

});




