var applyID = ''
$(document).ready(function() {
    applyID = window.location.href.split("=")[1];
    var sendData = {'applyID':applyID}
    $.getJSON('/applyDetails/', sendData, function (ret){
        var applyStatus = ret.apply_status;
        switch (applyStatus){
            case "1":
                $("#applyStatus").text('当前状态：已录入')
                break;
            case "2":
                $("#applyStatus").text('当前状态：已到账')
                break;
            case "3":
                $("#applyStatus").text('当前状态：已回访')
                break;
            case "4":
                $("#applyStatus").text('当前状态：已完成')
                break;
        }
        var applyType = ret.applyType;
        var account = 0;
        if(applyType == '1'){
            applyType = '认购';
            account = ret.applyAmount;
            $("#apply_amount_type").text('认购金额（元）：')
            $("#apply_amount").val(getFloat(account,2));
        }else if(applyType == '2'){
            applyType = '追加';
            account = ret.applyAmount;
            $("#apply_amount_type").text('追加金额（元）：')
            $("#apply_amount").val(getFloat(account,2));
        }else{
            applyType = '赎回';
            account = ret.applyAmount;
            $("#apply_amount_type").text('赎回份额（份）：')
            $("#apply_amount").val(getFloat(account,2));
        }
        $("#apply_type").text('意向类型：'+applyType);
        $("#apply_fund").text('意向产品：'+ret.applyFundName);
        $("#fund_details").click(function(){
            window.open('../account_details/fund='+ret.applyFundID)
        });
        $("#next_open_day").text('下一开放日：'+ret.applyDate);
        var failedTypeList = ret.failedType.split('|');
        for(var i=0; i<failedTypeList.length; i++){
            if(failedTypeList[i] == '0'){
                $("#client_type").children().eq(1).attr('src','../static/img/crm_intention/icons_s_r_72.png')
                $("#client_type").children().eq(2).attr('class','red')
            }
            if(failedTypeList[i] == '1'){
                $("#client_type").children().eq(3).attr('src','../static/img/crm_intention/icons_s_r_72.png')
                $("#client_type").children().eq(4).attr('class','red')
            }
            if(failedTypeList[i] == '2'){
                $("#client_type").children().eq(5).attr('src','../static/img/crm_intention/icons_s_r_72.png')
                $("#client_type").children().eq(6).attr('class','red')
            }
            if(failedTypeList[i] == '3'){
                $("#client_type").children().eq(7).attr('src','../static/img/crm_intention/icons_s_r_72.png')
                $("#client_type").children().eq(8).attr('class','red')
            }
        }
        $("#user-bankname").val(ret.bankName);
        $("#user-backno").val(ret.bankNo);

        $("#chulirenyuan").text(ret.username);
        $("#user-time-1").val(ret.signContractDate);

        if(ret.baseCheck == '1'){
            $("#base-check").attr("checked", true);
        }
        if(ret.cardCheck == '1'){
            $("#card-check").attr("checked", true);
        }
        if(ret.testCheck == '1'){
            $("#test-check").attr("checked", true);
        }
        if(ret.assetCheck == '1'){
            $("#asset-check").attr("checked", true);
        }
        if(ret.contractCheck == '1'){
            $("#contract-check").attr("checked", true);
        }
        if(ret.applyCheck == '1'){
            $("#apply-check").attr("checked", true);
        }
        if(ret.account_date == null || ret.account_date == ""){
            $("#zijin_com").text('-');
            $("#jingmo_com").text('-');
        }else{
            $("#zijin_com").text(ret.account_date);
            $("#jingmo_com").text(ret.silence_date);
        }
        if(applyStatus == 4){
            $("#apply_amount").attr("disabled",'disabled');
            $("#user-bankname").attr("disabled",'disabled');
            $("#user-backno").attr("disabled",'disabled');
            $("#apply-check").attr("disabled",'disabled');
            $("#deleteBtn").css('display','none');
        }
        if(ret.HF_date == null || ret.HF_date == ""){
            $("#huifang").text('否');
            $("#huifang_sty").text('无');
            $("#contart_per").text('无');
            $("#huifang_per").text('无');
            $("#huifang_com").text('-');
        }else{
            $("#huifang").text('是');
            $("#huifang_sty").text('电话');
            $("#contart_per").text(ret.username);
            $("#huifang_com").text(ret.HF_date);
            if(ret.complete_per == null || ret.complete_per == ""){
                $("#huifang_per").text('-');
            }else{
                $("#huifang_per").text(ret.complete_per);
            }
        }
        //if(ret.complete_date == null || ret.complete_date == ""){
        //    $("#huifang_com").text('-');
        //}else{
        //    $("#huifang_com").text(ret.complete_date);
        //}
    });

    var myDate = new Date();
    var yy = myDate.getYear();
    if(yy<1900) yy = yy+1900;
    var MM = myDate.getMonth()+1;
    if(MM<10) MM = '0' + MM;
    var dd = myDate.getDate();
    if(dd<10) dd = '0' + dd;
    $("#user-time-1").val(yy+'-'+MM+'-'+dd);
    $("#user-time-1").datepicker().on('changeDate', function(ev){
        $('#user-time-1').datepicker('hide');
    });
    $("#user-time-2").datepicker().on('changeDate', function(ev){
        $('#user-time-2').datepicker('hide');
    });


    $("#deleteBtn").click(function(){
        var delOrNot = confirm('确认删除该意向及其相关信息吗？');
        if(delOrNot){
            var sendData = {'applyID':applyID}
            $.getJSON('/deleteApply/', sendData, function (ret){
                alert('删除成功！');
                window.location.href = '../account_home/client='+ret.clientID;
            });
        }
    });

    $("#saveBtn").click(function(){
        var applyAmount = $("#apply_amount").val();
        var userBankName = $("#user-bankname").val();
        var userBankNo   = $("#user-backno").val();
        var userTime = "";
        var moneyTime = "";
        var baseCheck = "";
        var cardCheck = "";
        var testCheck = "";
        var assetCheck = "";
        var contractCheck = "";
        var applyCheck = $("#apply-check").is(':checked');
        var sendData = {'applyAmount':applyAmount,'userBankName':userBankName,'userBankNo':userBankNo,'userTime':userTime,'baseCheck':baseCheck,'cardCheck':cardCheck,
            'testCheck':testCheck,'assetCheck':assetCheck,'contractCheck':contractCheck,'applyCheck':applyCheck,'applyID':applyID,'moneyTime':moneyTime}
        $.getJSON('/updateClientAccount/', sendData, function (ret){
            window.location.href = '../account_home/client='+ret.clientID;
        });
    });
});