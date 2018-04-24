var i;
$(document).ready(function(){

    $("#user-province select").empty();
    for(i = 0; i < province_arr1.length; i++){
        $("#user-province select").append("<option>" + province_arr1[i] + "</option>");
    }
    $("#user-province select").on("change", cityChange);

    $("#enterBtn").click(function(){
        if($("#user-province select").val() == "请选择"){
            alert("请选择省份/直辖市！");
            return;
        }
        if($("#user-city select").val() == "请选择"){
            alert("请选择县市/区！");
            return;
        }
        if($("#user-address input").val() == ""){
            alert("请输入您的详细地址！");
            return;
        }
        if($("#user-address input").length >30){
            alert("您输入的地址不合法！");
            return;
        }
        if($("#user-zipCode input").val() == ""){
            alert("请输入您的邮编！");
            return;
        }
        if($("#user-zipCode input").length > 10){
            alert("您输入的邮编不合法！");
            return;
        }
        var province = $("#user-province select").val()
        var city = $("#user-city select").val()
        var details = $("#user-address input").val()
        var zipcode = $("#user-zipCode input").val()

        var sendDate = {"province":province,"city":city,"details":details,"zipcode":zipcode}

        $.getJSON('/modifyAddress/',sendDate,function(ret){
            window.location.href="../account_personal";
        })
        //$.getJSON('/modifyAddress/',sendDate,function(ret){
        //    window.location.href="../account_personal";
        //});
        //alert($("#user-province select").val());
        //alert($("#user-city select").val());
        //alert($("#user-address input").val());
        //alert($("#user-zipCode input").val());

        //alert("修改成功！");
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

});


function cityChange(){
    var province = $(this).val();
    var provinceId = province_arr1.indexOf(province);
    $("#user-city select").empty();
    for(i = 0; i < city_arr1[provinceId].length; i++){
        $("#user-city select").append("<option>" + city_arr1[provinceId][i] + "</option>");
    }
}

