var data = new Array();
var contact  = '';
var type = 9;
var status = 9;
var fundID = 9;
var clicking = false;
var productList = '';
$(document).ready(function(){
    //while(!finishOrNot){}
    //waitGlobal();
    //setTimeout('waitGlobal()',1000);
    applyListNot = true;
    $.getJSON('/getFuzzyProduct/',function(ret){
        productList = ret.productList;
        for(var i=0;i<productList.length;i++){
            var item = productList[i];
            if(item['saleschannel']=="直销" || item['saleschannel']=="员工"){
                data.push({title:item['name'],'nextopenday':item['nextopenday'],'fundid':item['fundid']});
            }
        }
        $("#user-search").bigAutocomplete({
            width:355,
            data:data,
            callback:function(data){
                fundID = data.fundid;
                getApply(fundID,type,status)
            }
        });
    });

    $("#filter-lx p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        type = getTypeNum($(this).text());
        getApply(fundID,type,status)
        //getProduct(jjjlName,$("#filter-px .filter-curr").text(),px,searchContent,1,true,false);
        //$("#filter-mb-cp").slideToggle();
    });
    $("#filter-zt p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        status = getStatusNum($(this).text());
        getApply(fundID,type,status)
        //getProduct(jjjlName,$("#filter-px .filter-curr").text(),px,searchContent,1,true,false);
        //$("#filter-mb-cp").slideToggle();
    });

    $("#searchBtn").click(function(){

        if(status == 1 || status == 2 || status == 9){
            alert('只能导出已完成状态的预约数据');
        }
        $.getJSON('/exportMsg/',{"fundID":fundID,"type":type,"status":status},function(ret){
            for(var i=0;i<ret.newUrl.length;i++){
                window.open(ret.newUrl[i]);
            }
        });
    });

    getApply(fundID,type,status);
});

function selectImage(file){
    var xlsName = file.files[0].name;
    var xlsContent = '';
    if(!file.files || !file.files[0]){
        return;
    }
    $("#tips").attr('placeholder',xlsName+'正在上传请稍后！');
    var reader = new FileReader();
    reader.onload = function(evt){
        xlsContent = evt.target.result;
        var sendDate = {'xlsName':xlsName,'xlsContent':xlsContent}
        $.post('/xlsHandle/',sendDate,function(ret){
            if(ret.success == '200'){
                $("#tips").attr('placeholder',xlsName+'上传成功！');
            }else{
                $("#tips").attr('placeholder',xlsName+'上传失败！');
            }
        });
    }
    reader.readAsDataURL(file.files[0]);
}

function getTypeNum(type){
    switch (type){
        case '全部':
            return 9
        case '申购追加':
            return 1
        case '赎回':
            return 3
    }
}
function getStatusNum(status){
    switch (status){
        case '全部':
            return 9;
        case '在途':
            return 1;
        case '完成':
            return 4;
        case '失效':
            return 5;
    }
}

function getApply(fundID,type,status){
    $("#listBox").empty();
    var sendData = {"fundID":fundID,"type":type,"status":status}
    $.getJSON('/getTotalApplyList/',sendData,function(ret){
        var applyList = ret.sendApplyList;
        for(var i=0;i<applyList.length;i++){
            var item = applyList[i];
            replaceContent(i,item)
        }
    });
}

function replaceContent(num,item){
    var btn = 'hidebtn'+num;
    var div = 'hidediv'+num;

    var hideOrBlock = '<a id="'+btn+'" onclick="blockOrHide('+num+')">展开</a>';
    var applyType = item.applyType;
    var applyStatus = item.applyStatus;
    switch(applyType){
        case '1':
            applyType = '申购';
            break;
        case '2':
            applyType = '追加';
            break;
        case '3':
            applyType = '赎回';
            break;
    }
    switch(applyStatus){
        case '1':
            applyStatus = '已录入';
            break;
        case '2':
            applyStatus = '已到账';
            break;
        case '3':
            applyStatus = '已回访';
            break;
        case '4':
            applyStatus = '已完成';
            break;
        case '5':
            applyStatus = '已失效';
            break;
    }
    var applyAmount = item.applyAmount;
    if(applyAmount == '' || applyAmount == null){
        applyAmount = '-';
    }else{
        applyAmount = fondsFormat(getFloat(applyAmount,2));
    }
    var applyCount = item.applyCount;
    if(applyCount == '' || applyCount == null){
        applyCount = '-';
    }else{
        applyCount = fondsFormat(getFloat(applyCount,2));
    }
    var bankName = item.bankName;
    if(bankName == '' || bankName == null){
        bankName = '-';
    }
    var bankNo = item.bankNo;
    if(bankNo == '' || bankNo == null) {
        bankNo = '-';
    }
    var flag1 = '合同及风险揭示书';
    var infoFlag = item.infoFlag;
    var applytabFlag = item.applytab_flag;
    var questionnaireFlag = item.questionnaireFlag;
    var signContractDate = item.signContractDate;
    if(applyType == '申购'){
        var contractFlag = item.contractFlag;
        if(contractFlag == 0){
            contractFlag = '未签署';
        }else{
            contractFlag = '已签署';
        }
        if(infoFlag == 0){
            infoFlag = '未签署';
        }else{
            infoFlag = '已签署';
        }
        if(applytabFlag == 0){
            applytabFlag = '未签署';
        }else{
            applytabFlag = '已签署';
        }
        if(questionnaireFlag == 0){
            questionnaireFlag = '未签署';
        }else{
            questionnaireFlag = '已签署';
        }
        if(signContractDate == '' || signContractDate == null){
            signContractDate = '未签署';
        }
    }else{
        //var contractFlag = item.applytab_flag
        //if(contractFlag == 0){
        //    contractFlag = '未签署';
        //}else{
        //    contractFlag = '已签署';
        //}
        contractFlag = '-';
        infoFlag = '-';
        if(applytabFlag == 0){
            applytabFlag = '未签署';
        }else{
            applytabFlag = '已签署';
        }
        //applytabFlag = '-';
        questionnaireFlag = '-';
        signContractDate = '-';
    }
    var assetFlag = item.assetFlag;
    if(assetFlag == 0){
        assetFlag = '未签署';
    }else{
        assetFlag = '已签署';
    }
    var accountDate = item.accountDate;
    if(accountDate == '' || accountDate == null){
        accountDate = '未到账';
    }
    var capitalID = item.capitalID;
    if(capitalID == '' || capitalID == null){
        capitalID = '未匹配';
    }
    var silenceDate = item.silenceDate;
    if(silenceDate == '' || silenceDate == null){
        silenceDate = '未匹配';
    }
    var HForNot = '未回访';

    if(applyStatus == '已回访' || applyStatus == '已完成'){
        HForNot = '已回访';
    }
    var HFDate = item.HFDate;
    if(HFDate == '' || HFDate == null){
        HFDate = '未回访';
    }
    //else{
    //    HFDate = HFDate;
    //}
    $("#listBox").append('<li><div class="listBg1 list-left pull-left"><div class="l-i-1 list-info pull-left"><p>客户姓名</p><em>'+item.clientName+'</em></div><div class="l-i-2 list-info pull-left"><p>预约类型</p><em>'+applyType+'</em></div><div class="l-i-3 list-info pull-left"><p>预约状态</p><em>'+applyStatus+'</em></div><div class="l-i-4 list-info pull-left"><p>预约产品</p><em>'+item.fundName+'</em></div><div class="l-i-5 list-info pull-left"><p>开放日</p><em>'+item.fundOpenDay+'</em></div></div><div class="list-right pull-left hidden-xs"><div class="list-right-info">'+hideOrBlock+'</div></div><div id="'+div+'" class="hide-div"><div class="listBg2 list-all pull-left"><div class="l-i-1 list-info pull-left"><p>预约金额（元）</p><em>'+applyAmount+'</em></div><div class="l-i-2 list-info pull-left"><p>预约份额（份）</p><em>'+applyCount+'</em></div><div class="l-i-3 list-info pull-left"><p>客户开户行</p><em>'+bankName+'</em></div><div class="l-i-4 list-info pull-left"><p>客户开户行账号</p><em>'+bankNo+'</em></div><div class="l-i-5 list-info pull-left"><p>'+flag1+'</p><em>'+contractFlag+'</em></div></div><div class="listBg1 list-all pull-left"><div class="l-i-6 list-info pull-left"><p>基本信息表</p><em>'+infoFlag+'</em></div><div class="l-i-6 list-info pull-left"><p>直销申请表</p><em>'+applytabFlag+'</em></div><div class="l-i-6 list-info pull-left"><p>风险问卷确认</p><em>'+questionnaireFlag+'</em></div><div class="l-i-6 list-info pull-left"><p>资产证明确认</p><em>'+assetFlag+'</em></div><div class="l-i-6 list-info pull-left"><p>合同签订日期</p><em>'+signContractDate+'</em></div><div class="l-i-7 list-info pull-left"><p>资金到账日期</p><em>'+accountDate+'</em></div></div><div class="listBg2 last-row list-all pull-left"><div class="l-i-6 list-info pull-left"><p>匹配的资金流水号</p><em>'+capitalID+'</em></div><div class="l-i-6 list-info pull-left"><p>静默期到期时间</p><em>'+silenceDate+'</em></div><div class="l-i-6 list-info pull-left"><p>是否回访完成</p><em>'+HForNot+'</em></div><div class="l-i-6 list-info pull-left"><p>回访处理人</p><em>'+item.updatedBy+'</em></div><div class="l-i-6 list-info pull-left"><p>回访完成时间</p><em>'+HFDate+'</em></div><div class="l-i-7 list-info pull-left"><p>回访形式</p><em>电话</em></div></div></div></li>');
}

function blockOrHide(num){
    var btn = 'hidebtn'+num;
    var div = 'hidediv'+num;
    var obj =  document.getElementById(btn);
    var nextObj =  document.getElementById(div);
    if(nextObj.style.display == "none"){
        nextObj.style.display = "block";
        obj.innerText = '收起';
    }else{
        nextObj.style.display = "none";
        obj.innerText = '展开';
    }
}

function waitGlobal1(){
    document.getElementById("tips").disabled = true;
    if(!judgeAuthority(1002)){
        $("#info2_content2").css("display", "none");
        $("#captailList").css("display", "none");
        $("#applyList").addClass("info-title-more-curr");
    }else{
        $("#info2_content2").css("display", "block");
        $("#info2_content3").css("display", "none");
        $(".info-title-more p").mouseover(function(){
            var ID = $(this).index();
            $(this).addClass("info-title-more-curr");
            $(this).siblings().removeClass("info-title-more-curr");
            if(ID == 0){
                $("#info2_content2").css("display", "block");
                $("#info2_content3").css("display", "none");
            }
            else if(ID == 1){
                $("#info2_content2").css("display", "none");
                $("#info2_content3").css("display", "block");
            }
        });
    }
}