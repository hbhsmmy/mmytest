var clientID = '';
var clientType = '1';
var contactList = '';
$(document).ready(function() {
    clientID = window.location.href.split("=")[1];
    $("#info2_content1").css("display", "block");
    $("#info2_content2").css("display", "none");
    $("#info2_content3").css("display", "none");
    $("#info2_content4").css("display", "none");
    $("#info2_content5").css("display", "none");

    $(".info-title-more p").mouseover(function(){
        var ID = $(this).index();
        $(this).addClass("info-title-more-curr");
        $(this).siblings().removeClass("info-title-more-curr");
        if(ID == 0){
            $("#info2_content1").css("display", "block");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "none");
            $("#info2_content5").css("display", "none");
        }
        else if(ID == 1){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "block");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "none");
            $("#info2_content5").css("display", "none");
        }
        else if(ID == 2){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "block");
            $("#info2_content4").css("display", "none");
            $("#info2_content5").css("display", "none");
        }
        else if(ID == 3){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "block");
            $("#info2_content5").css("display", "none");
        }
        else if(ID == 4){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "none");
            $("#info2_content5").css("display", "block");
        }
    });

    $("#filter-mb-btn1").click(function(){
        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");
        $("#info2_content1").css("display", "block");
        $("#info2_content2").css("display", "none");
        $("#info2_content3").css("display", "none");
        $("#info2_content4").css("display", "none");
    });
    $("#filter-mb-btn2").click(function(){

        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");
        $("#info2_content1").css("display", "none");
        $("#info2_content2").css("display", "block");
        $("#info2_content3").css("display", "none");
        $("#info2_content4").css("display", "none");
    });
    $("#filter-mb-btn3").click(function(){

        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");
        $("#info2_content1").css("display", "none");
        $("#info2_content2").css("display", "none");
        $("#info2_content3").css("display", "block");
        $("#info2_content4").css("display", "none");
    });
    $("#filter-mb-btn4").click(function(){

        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");
        $("#info2_content1").css("display", "none");
        $("#info2_content2").css("display", "none");
        $("#info2_content3").css("display", "none");
        $("#info2_content4").css("display", "block");
    });

    $("#filter-zt p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        $("#filter-mb-cp").slideToggle();
    });

    $("#taskBtn").click(function(){
        var client_name = $("#userName_pc").text();
        window.location.href = '../account_task/client_id='+clientID+'&client_name='+client_name;
    });

    $("#IntentBtn").click(function(){
        var client_name = $("#userName_pc").text();
        window.location.href = '../account_intention/client_id='+clientID+'&client_name='+client_name;
    });

    $("#editBtn").click(function(){
        if(clientType == '1'){
            window.location.href = '../account_editor/client='+clientID;
        }else{
            window.location.href = '../account_org_editor/client='+clientID;
        }
    });
    $("#deletBtn").click(function(){
        var content = confirm('确认删除该客户及其相关信息吗？');
        if(content){
            var sendData = {'client_id':clientID};
            $.getJSON('/delet_client/',sendData,function(ret) {
                if(ret.success == 402){
                    alert('删除失败！');
                }else{
                    alert('删除成功！');
                    window.location.href = '../account_records';
                }
            });
        }
    });

    $("#taskBtn_mb").click(function(){
        var client_name = $("#userName_pc").text();
        window.location.href = '../account_task/client_id='+clientID+'&client_name='+client_name;
    });
    $("#editBtn_mb").click(function(){
        window.location.href = '../account_editor/client='+clientID;
    });
    $("#deletBtn_mb").click(function(){

    });

    var myDate = new Date();
    var yy = myDate.getYear();
    if(yy<1900) yy = yy+1900;
    var MM = myDate.getMonth()+1;
    if(MM<10) MM = '0' + MM;
    var dd = myDate.getDate();
    if(dd<10) dd = '0' + dd;
    $("#txtEndDate").val(yy+'-'+MM+'-'+dd);
    $("#txtEndDate").datepicker().on('changeDate', function(ev){
        $('#txtEndDate').datepicker('hide');
        var dataArray = $("#txtEndDate").val();
        var sendData = {'client_id':clientID,'time':dataArray}
        $.getJSON('/get_user_fund_time/',sendData,function(ret){
            $("#assets").text(fondsFormat(getFloat(ret.assets,2))+'元');
            $("#totalreturn_money").text(fondsFormat(getFloat(ret.totalreturn_money,2))+'元');
            $("#totalreturn_rate").text(getFloat(ret.totalreturn_rate*100,2)+'%');
            $("#listBox1").empty();
            if(ret.type == 1 && ret.fundlist.length != 0){
                $("#noRecord_2").css("display", "none");
                $("#info-title-funds").css("display", "block");
                for(var i=0; i<ret.fundlist.length; i++){
                    var item = ret.fundlist[i];
                    getHome(item);
                }
            }else{
                $("#info-title-funds").css("display", "none");
                $("#noRecord_2").css("display", "block");
            }
        });
    });

    var sendData = {'clientID':clientID}
    $.getJSON('/getApplyList/',sendData, function (ret){
        if(ret.applyList.length!=0){
            $("#noRecord_4").css("display", "none");
            $("#listBox3").css("display", "block");
            for(var i=0;i<ret.applyList.length;i++){
                var item = ret.applyList[i];
                var applyType = item.applyType;
                var account = 0;
                var herf = "";
                var tpyeContent = "意向金额（元）"
                if(applyType == '1'){
                    applyType = '申购';
                    account = item.applyAmount;
                    herf = '../account_apply/applyID='+item.applyID;
                }else if(applyType == '2'){
                    applyType = '追加';
                    account = item.applyAmount;
                    herf = '../account_add_apply/applyID='+item.applyID;
                }else{
                    applyType = '赎回';
                    account = item.applyAmount;
                    herf = '../account_redemption_apply/applyID='+item.applyID;
                    tpyeContent = "意向份额（份）"
                }
                var inputDate = timeFormat(item.inputDate*1000,'yyyy-MM-dd');
                $("#listBox3").append('<li class="listBg1"><div class="list-left pull-left"><a class="list-title2 clearfix"><p class="pull-left">'+item.applyFundName+'</p><em>'+inputDate+'生成</em></a><a href="" target="_blank" class="list-infoContent2 clearfix"><div class="l-i-2 list-info2 pull-left"><p>意向类型</p><em>'+applyType+'</em></div><div class="l-i-1 list-info2 pull-left"><p>'+tpyeContent+'</p><em>'+getFloat(account,2)+'</em></div><div class="l-i-2 list-info2 pull-left"><p>产品开放日</p><em>'+item.applyDate+'</em></div></a></div><div class="list-right pull-left"><div class="list-right-info"><a class= "a_ready" href="'+herf+'">查看/编辑意向</a></div></div></li>')
            }
        }else{
            $("#noRecord_4").css("display", "block");
            $("#listBox3").css("display", "none");
        }
    });

    $.getJSON('/getClientCheck/',sendData, function (ret) {
        if(ret.documentList[0].length == 0){
            $("#client_card").css('display','none')
            $(".shenfen").css("height", "40px");
        }else{
            $("#client_card").css('display','block')
            $(".shenfen").css("height", "165px");
            for(var i=0;i<ret.documentList[0].length;i++){
                $("#client_card").children().eq(i).children().eq(0).attr('src','../static/tempfiles/'+ret.documentList[0][i].name);
            }
        }

        if(ret.clientRisk != null){
            //alert(ret.clientRisk);
            var total_point = ret.clientRisk;
            var level = ret.level;
            //var total_point = 0;
            //for(var i=0;i<client_risk_type.length;i++){
            //    total_point += client_risk_type[i];
            //}
            $("#client_risk").html('C'+level+'  '+total_point+'分')
            $("#client_risk_time_title").css('margin-left','45px');
            $("#client_risk_time").html(getLocalTime(ret.documentList[1][0].name.split('_')[3].split('.')[0]));

            $("#check_wenjuan").click(function(){
                window.open('../static/tempfiles/'+ret.documentList[1][0].name);
            });
        }else{
            $("#check_wenjuan").css('display','none');
        }

        if(ret.documentList[2].length == 0){
            $("#client_asset").css('display','none');
            $(".asset1").css("height", "40px");
        }else{
            $("#client_asset").css('display','block');
            $(".asset1").css("height", "165px");
            for(var i=0;i<ret.documentList[2].length;i++){
                $("#client_asset").children().eq(i).children().eq(0).attr('src','../static/tempfiles/'+ret.documentList[2][i].name);
            }
        }

        $(".card_img").click(function(){
            var imgSrc = $(this).attr('src');
            if(imgSrc.substr(imgSrc.length-10) != 'empty0.png'){
                window.open($(this).attr('src'));
            }
        })
    });

    $.getJSON('/get_user_details/',sendData, function (ret) {
        if(ret.page1.mark == 1){
            $("#deletBtn").css("display", "none");
        }
        $("#userName_pc").text(ret.page1.customer_name);
        $("#userName_mb").text(ret.page1.customer_name);
        $("#createInfo").text('创建：'+ret.page1.created_by+'  '+ret.page1.created_date);
        $("#updateInfo").text('最后修改：'+ret.page1.updated_by+'  '+ret.page1.updated_date);
        $("#userUpdate_mb").text(ret.page1.created_by+ret.page1.created_date+'创建，'+ret.page1.updated_by+ret.page1.updated_date+'修改')
        if(ret.page1.customer_mobile == null || ret.page1.customer_mobile == ""){
            $("#customer_mobile").text('电话：－');
        }else{
            $("#customer_mobile").text('电话：'+ret.page1.customer_mobile);
        }
        if(ret.page1.customer_email == null || ret.page1.customer_email == ""){
            $("#customer_email").text('邮箱：－');
        }else{
            $("#customer_email").text('邮箱：'+ret.page1.customer_email);
        }
        var province = '';
        var city = '';
        var address = '';
        if(ret.page1.province != null) {
            province = ret.page1.province;
        }
        if(ret.page1.city != null) {
            city = ret.page1.city;
        }
        if(ret.page1.address != null) {
            address = ret.page1.address;
        }
        var customer_address = province+city+address;
        if(customer_address == ''){
            $("#customer_address").text('－');
        }else{
            $("#customer_address").text(customer_address);
        }
        var website_name = ret.page1.investor_name;
        if(website_name == '' || website_name == null || website_name == "_"){
            $("#website_name").text('网站名：－');
        }else{
            $("#website_name").text('网站名：'+website_name);
        }
        if(ret.page1.customer_wx == null || ret.page1.customer_wx == ''){
            $("#customer_wx").text('其他联系：－');
        }else{
            $("#customer_wx").text('其他联系：'+ret.page1.customer_wx);
        }
        if(ret.page1.customer_managers == null || ret.page1.customer_managers == ''){
            $("#customer_managers").text('－');
        }else{
            $("#customer_managers").text(ret.page1.customer_managers);
        }
        if(ret.page1.customer_interest == null || ret.page1.customer_interest == ''){
            $("#customer_interest").text('－');
        }else{
            $("#customer_interest").text(ret.page1.customer_interest);
        }
        if(ret.page1.customer_manager == null || ret.page1.customer_manager == ''){
            $("#customer_manager").text('－');
        }else{
            $("#customer_manager").text(ret.page1.customer_manager);
        }
        clientType = ret.page1.client_type;
        if(clientType == '' || clientType == null){
            $("#client_type").text('客户类型：－');
        }else{
            switch(clientType){
                case "0":
                    $("#client_type").text('客户类型：机构');
                    break;
                case "1":
                    $("#client_type").text('客户类型：个人');
                    break;
                case "3":
                    $("#client_type").text('客户类型：B级基金');
                    break;
                case "4":
                    $("#client_type").text('客户类型：子基金');
                    break;
            }
        }
        if(ret.page1.card_type == null || ret.page1.card_type == ''){
            $("#card_type").text('证件类型：－');
        }else{
            if(clientType == "0"){
                switch(ret.page1.card_type){
                    case "0":
                        $("#card_type").text("证件类型：组织机构代码证");
                        break;
                    case "1":
                        $("#card_type").text("证件类型：营业执照");
                        break;
                    case "2":
                        $("#card_type").text("证件类型：行政机关");
                        break;
                    case "3":
                        $("#card_type").text("证件类型：社会团体");
                        break;
                    case "4":
                        $("#card_type").text("证件类型：军队");
                        break;
                    case "5":
                        $("#card_type").text("证件类型：武警");
                        break;
                    case "6":
                        $("#card_type").text("证件类型：下属机构（具有主管单位批文号）");
                        break;
                    case "7":
                        $("#card_type").text("证件类型：基金会");
                        break;
                    case "8":
                        $("#card_type").text("证件类型：其他");
                        break;
                    case "9":
                        $("#card_type").text('证件类型: 社会统一信用代码');
                        break;
                    case "12":
                        $("#card_type").text('证件类型：产品备案编码');
                        break;
                }
            }else if(clientType == "1"){
                switch(ret.page1.card_type){
                    case "0":
                        $("#card_type").text("证件类型：身份证");
                        break;
                    case "5":
                        $("#card_type").text("证件类型：户口本");
                        break;
                    case "2":
                        $("#card_type").text("证件类型：军官证");
                        break;
                    case "4":
                        $("#card_type").text("证件类型：港澳居民来往内地通行");
                        break;
                    case "1":
                        $("#card_type").text("证件类型：护照");
                        break;
                    case "3":
                        $("#card_type").text("证件类型：士兵证");
                        break;
                    case "6":
                        $("#card_type").text("证件类型：外国护照");
                        break;
                    case "7":
                        $("#card_type").text("证件类型：其他");
                        break;
                    case "8":
                        $("#card_type").text("证件类型：文职证");
                        break;
                    case "9":
                        $("#card_type").text("证件类型：警官证");
                        break;
                    case "A":
                        $("#card_type").text("证件类型：台胞证");
                        break;
                    default :
                        $("#card_type").text("证件类型：－");
                        break;
                }
            }
        }
        if(ret.page1.card_no == null || ret.page1.card_no == ''){
            $("#card_no").text('证件号码：－');
        }else{
            $("#card_no").text('证件号码：'+ret.page1.card_no);
        }

        if(ret.page1.contact_name == null || ret.page1.contact_name == ''){
            $("#contact_name").text('联系人：－');
        }else{
            $("#contact_name").text('联系人：'+ret.page1.contact_name);
        }
        if(clientType == "1"){
            if(ret.page1.education == null || ret.page1.education == ""){
                $("#client_education").text('学历：－');
            }else{
                $("#client_education").text('学历：'+ret.page1.education);
            }
            if(ret.page1.occupation == null || ret.page1.occupation == ""){
                $("#client_occupation").text('职业：－');
            }else{
                $("#client_occupation").text('职业：'+ret.page1.occupation);
            }
            if(ret.page1.employer == null || ret.page1.employer == ""){
                $("#client_employer").text('工作单位：－');
            }else{
                $("#client_employer").text('工作单位：'+ret.page1.employer);
            }
            if(ret.page1.contact_mobile == null || ret.page1.contact_mobile == ''){
                $("#contact_mobile").text('联系人电话：－');
            }else{
                $("#contact_mobile").text('联系人电话：'+ret.page1.contact_mobile);
            }
        }else{
            $("#businessscope").css('display','block');
            if(ret.page1.businessscope == null || ret.page1.businessscope == ""){
                $("#customer_businessscope").text('－');
            }else{
                $("#customer_businessscope").text(ret.page1.businessscope);
            }

            if(ret.page1.represent1 == null || ret.page1.represent1 == ""){
                $("#client_education").text('法人/授权人：－');
            }else{
                $("#client_education").text('法人/授权人：'+ret.page1.represent1);
            }
            if(ret.page1.represent_idtype == null || ret.page1.represent_idtype == ""){
                $("#client_occupation").text('证件类型：－');
            }else{
                switch(ret.page1.represent_idtype){
                    case "0":
                        $("#client_occupation").text("证件类型：身份证");
                        break;
                    case "5":
                        $("#client_occupation").text("证件类型：户口本");
                        break;
                    case "2":
                        $("#client_occupation").text("证件类型：军官证");
                        break;
                    case "4":
                        $("#client_occupation").text("证件类型：港澳居民来往内地通行");
                        break;
                    case "1":
                        $("#client_occupation").text("证件类型：护照");
                        break;
                    case "3":
                        $("#client_occupation").text("证件类型：士兵证");
                        break;
                    case "6":
                        $("#client_occupation").text("证件类型：外国护照");
                        break;
                    case "7":
                        $("#client_occupation").text("证件类型：其他");
                        break;
                    case "8":
                        $("#client_occupation").text("证件类型：文职证");
                        break;
                    case "9":
                        $("#client_occupation").text("证件类型：警官证");
                        break;
                    case "A":
                        $("#client_occupation").text("证件类型：台胞证");
                        break;
                    default :
                        $("#client_occupation").text("证件类型：－");
                        break;
                }
            }
            if(ret.page1.represent_idno == null || ret.page1.represent_idno == ""){
                $("#client_employer").text('证件号码：－');
            }else{
                $("#client_employer").text('证件号码：'+ret.page1.represent_idno);
            }
            if(ret.page1.controller == null || ret.page1.controller == ''){
                $("#contact_mobile").text('实际控制人：－');
            }else{
                $("#contact_mobile").text('实际控制人：'+ret.page1.controller);
            }
        }
        if(ret.page1.customer_src == null || ret.page1.customer_src == ''){
            $("#customer_src").text('－');
        }else{
            $("#customer_src").text(ret.page1.customer_src);
        }

        if(ret.page1.customer_channel == null || ret.page1.customer_channel == ''){
            $("#customer_channel").text('－');
        }else{
            $("#customer_channel").text(ret.page1.customer_channel);
        }
        if(ret.page1.ta_id == null || ret.page1.ta_id == ''){
            $("#ta_id").text('－');
        }else{
            $("#ta_id").text(ret.page1.ta_id);
        }
        if(ret.page2 == ""){
            $("#client_bar_1").css("display", "none");
            $("#client_bar_2").css("display", "none");
            $("#filter-mb-btn2").css("display", "none");
            $("#filter-mb-btn3").css("display", "none");
            document.getElementById('filter-mb-btn1').style.width = 50+'%';
            document.getElementById('filter-mb-btn4').style.width = 50+'%';
        }else{
            $("#assets").text(fondsFormat(getFloat(ret.page2.assets,2)));
            $("#totalreturn_money").text(fondsFormat(getFloat(ret.page2.totalreturn_money,2)));
            $("#totalreturn_rate").text(getFloat(ret.page2.totalreturn_rate*100,2)+'%');
            if(ret.page2 != "" && ret.page2.fundlist != ""){
                $("#info-title-funds").css("display", "block");
                $("#noRecord_2").css("display", "none");
                for(var i=0; i<ret.page2.fundlist.length; i++){
                    var item = ret.page2.fundlist[i];
                    getHome(item);
                }
            }else{
                $("#info-title-funds").css("display", "none");
                $("#noRecord_2").css("display", "block");
            }
            for(var i=0; i<ret.page3.recordsList.length; i++){
                var item = ret.page3.recordsList[i]
                replaceContent1(item,i)
            }
        }
        var uncontactNum = 0;
        contactList = ret.page4.contactList;
        for(var i=0; i<contactList.length; i++){
            item = ret.page4.contactList[i];
            replaceContent2(item,i);
            if(item.task_status == '2'){
                uncontactNum ++;
            }
        }
        if(uncontactNum == 0){
            if(contactList.length > 0){
                $("#noRecord_5").css("display", "none");
            }else{
                $("#noRecord_5").css("display", "block");
            }
            $("#filter-4").css("display", "none");
            $("#contact_bg").css("display", "none");
            $("#contact_tip").css("display", "none");
        }else{
            $("#noRecord_5").css("display", "none");
            $("#filter-4").css("display", "block");
            $("#contact_bg").css("display", "block");
            $("#contact_tip").css("display", "block");
            $("#contact_tip").text(uncontactNum);
        }
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });
});

function getHome(item){
    var con1 = ''
    var con2 = ''
    if(item.return_money > 0){
        con1 = '<span class="red">'
    }else if(item.return_money < 0){
        con1 = '<span class="green">'
    }else{
        con1 = '<span>'
    }
    if(item.return_rate > 0){
        con2 = '<span class="red">';
    }else if(item.return_rate < 0){
        con2 = '<span class="green">';
    }else{
        con2 = '<span>';
    }
    $("#listBox1").append('<li><a class="list-title clearfix" href="../account_details/fund='+item.fundid+'" target="_black"><p class="pull-left cl-555">'+item.fundname+'</p></a><a class="list-datas clearfix cl-777" href="../account_details/fund='+item.fundid+'"><p class="list-data pull-left">市值（元）<span class="cl-333">'+fondsFormat(getFloat(item.marketcap,2))+'</span></p><p class="list-data1 pull-left">份额（份）<span class="cl-333">'+fondsFormat(getFloat(item.shares,2))+'</span></p><p class="list-data2 pull-left">单位净值<span class="cl-333">'+getFloat(item.nav,4)+'</span></p><p class="list-data2 pull-left">累计净值<span class="cl-333">'+getFloat(item.totalnav,4)+'</span></p><p class="list-data pull-left">净值日期<span class="cl-333">'+item.navday+'</span></p><p class="list-data2 pull-left">持有收益（元）'+con1+''+fondsFormat(getFloat(item.return_money,2))+'</span></p><p class="list-data3 pull-left">持有收益率'+con2+''+getFloat(item.return_rate*100,2)+'%'+'</span></p><p class="list-data1 pull-left">购买渠道<span class="cl-333">'+item.channel+'</span></p><p class="list-data3 pull-right">购买日期<span class="cl-333">'+item.buyday+'</span></p><p class="list-data2 pull-left">下一个开放日<span class="cl-333">'+item.nextopenday+'</span></p></a></li>');
}

function goToUpload(tradeID){
    alert(tradeID);
}

function replaceContent1(item,i){
    var style = '';
    var purfee = '';
    if(i%2==0){
        style = "listBg1"
    }else{
        style = "listBg2"
    }
    //alert(item.fundid);
    switch(item.optype){
        case 0:
            if(item.channelid == 8 ||item.channelid == 9|| item.channelid == 21 ){
                purfee = fondsFormat(getFloat(item.purfee,2))
            }else{
                purfee = '咨询代销机构'
            }
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left goumai">【购买】</em><a href="../account_details/fund='+item.fundid+'" target="_blank" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left clearfix"><p>金额(元)<span class="hidden-xs">：</span><em class="red list_je">'+fondsFormat(getFloat(item.trademoney,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-right clearfix"><p>交易日净值<span class="hidden-xs">：</span><em class="list_jyrjz">'+getFloat(item.tradenav,4)+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left clearfix"><p>份额(份)<span class="hidden-xs">：</span><em class="list_fe">'+fondsFormat(getFloat(item.tradeshares,2))+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix"><p>认购费(元)<span class="hidden-xs">：</span><em class="list_jyrjz">'+purfee+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em class="list_rq">'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div><div class="uploadDiv"><a href="../account_upload/trade_id='+item.tradeid+'" target="_blank" class="uploadA">上传/查看相关文档</a></div></div></li>');
            break;
        case 1:
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left shuhui">【赎回】</em><a href="../account_details/fund='+item.fundid+'" target="_blank" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left clearfix"><p>金额(元)<span class="hidden-xs">：</span><em class="red list_je">'+fondsFormat(getFloat(item.trademoney,2))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left clearfix"><p>份额(份)<span class="hidden-xs">：</span><em class="list_fe">'+fondsFormat(getFloat(item.tradeshares,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left clearfix"><p>交易日净值<span class="hidden-xs">：</span><em class="list_jyrjz">'+getFloat(item.tradenav,4)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left"><p>赎回收益(元)<span class="hidden-xs">：</span><em class="list_ljsy">'+fondsFormat(getFloat(item.returnmoney,2))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left"><p>赎回收益率<span class="hidden-xs">：</span><em class="list_ljsyl">'+(getFloat(item.returnrate*100,2)+'%')+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em class="list_rq">'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div></div></li>')
            break;
        case 3:
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left ticheng">【<span class="hidden-xs">业绩</span>提成】</em><a href="../account_details/fund='+item.fundid+'" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left"><p>份额(份)<span class="hidden-xs">：</span><em class="red">'+fondsFormat(getFloat(item.tradeshares,2))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left"><p>扣减金额(元)<span class="hidden-xs">：</span><em>'+fondsFormat(getFloat(item.trademoney,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left"><p>扣减前净值<span class="hidden-xs">：</span><em class="">'+getFloat(item.beforenav,4)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left"><p>扣减后净值<span class="hidden-xs">：</span><em>'+getFloat(item.afternav,4)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div></div></li>')
            break;
        case 4:
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left ticheng">【<span class="hidden-xs">业绩</span>提成】</em><a href="../account_details/fund='+item.fundid+'" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left"><p>份额净值<span class="hidden-xs">：</span><em class="red">'+fondsFormat(getFloat(item.tradenav,4))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left"><p>扣减金额(元)<span class="hidden-xs">：</span><em>'+fondsFormat(getFloat(item.trademoney,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left"><p>扣减前份额<span class="hidden-xs">：</span><em class="">'+getFloat(item.beforeshares,2)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left"><p>扣减后份额<span class="hidden-xs">：</span><em>'+getFloat(item.aftershares,2)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div></div></li>')
            break;
        case 5:
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left fenhong">【分红】</em><a href="../account_details/fund='+item.fundid+'" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left clearfix"><p>份额(份)<span class="hidden-xs">：</span><em class="list_je">'+fondsFormat(getFloat(item.beforeshares,2))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left clearfix"><p>每份分红(元)<span class="hidden-xs">：</span><em class="list_fe">'+fondsFormat(getFloat(item.dividpershare,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left clearfix"><p>分红金额(元)<span class="hidden-xs">：</span><em class="list_jyrjz">'+getFloat(item.trademoney,2)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left"><p>份额净值<span class="hidden-xs">：</span><em class="list_ljsy">'+fondsFormat(getFloat(item.tradenav,4))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left"><p>累计净值<span class="hidden-xs">：</span><em class="list_ljsyl">'+(getFloat(item.totalnav,4))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left"><p>分红类型<span class="hidden-xs">：</span><em class="list_ljsyl">现金分红</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em class="list_rq">'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div></div></li>')
            break;
        case 6:
            $("#listBox2").append('<li class="'+style+'"><div class="list"><div href="../account_details/fund='+item.fundid+'" target="_blank" class="list-title1 clearfix"><em class="list-title-em1 pull-left fenhong">【分红】</em><a href="../account_details/fund='+item.fundid+'" class="pull-left textEllipsis">'+item.fundname+'</a><p class="date pull-right hidden-xs list_rq">日期：<em>'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div><div class="list-infoContent1 clearfix"><div class="l-i-1 l-i-trade list-info pull-left clearfix"><p>分红前份额(份)<span class="hidden-xs">：</span><em class="red list_je">'+fondsFormat(getFloat(item.beforeshares,2))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left clearfix"><p>分红后份额(份)<span class="hidden-xs">：</span><em class="list_fe">'+fondsFormat(getFloat(item.aftershares,2))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left clearfix"><p>每份分红(元)<span class="hidden-xs">：</span><em class="list_jyrjz">'+getFloat(item.dividpershare,2)+'</em></p></div><div class="l-i-1 l-i-trade list-info pull-left"><p>份额净值<span class="hidden-xs">：</span><em class="list_ljsy">'+fondsFormat(getFloat(item.tradenav,4))+'</em></p></div><div class="l-i-2 l-i-trade list-info pull-left"><p>累计净值<span class="hidden-xs">：</span><em class="list_ljsyl">'+(getFloat(item.totalnav,4))+'</em></p></div><div class="l-i-5 l-i-trade list-info pull-left"><p>分红类型<span class="hidden-xs">：</span><em class="list_ljsyl">红利再投</em></p></div><div class="l-i-1 l-i-trade list-info pull-left clearfix visible-xs-block"><p>日期<span class="hidden-xs">：</span><em class="list_rq">'+timeFormat(item.opday*1000,'yyyy年MM月dd日')+'</em></p></div></div></div></li>')
            break;
    }
}

function replaceContent2(item,i){
    var style = '';
    var liID = "li"+i;
    var btn = 'btn'+i;
    var divID = "div"+i;
    var time = '计划完成时间';
    var user = '被分配人';
    var button = '<a id="'+btn+'" class="a_ready" onclick="complete('+i+','+item.contact_id +')">完成</a>';
    if(i%2==0){
        style = "listBg1"
    }else{
        style = "listBg2"
    }
    var contactDetail = item.contact_detail;
    var type = "自建任务";
    if(item.contact_type == 2){
        type = "静默回访";
    }
    if(item.contact_type == 10){
        type = "适配性确认";
    }
    if(item.contact_type == 3){
        type = "合同收取";
        contactDetail = contactDetail + '<a class="brown" onclick="getDoc('+i+')">点击浏览材料</a>';
    }

    if(item.task_status == "1"){
        time = '完成时间';
        user = '完成人';
        button = '<a class="a_finish" style="cursor:default">已完成</a>';
    }
    var contact_record = item.contact_record;
    if(item.task_status == "2"){
        contact_record = '尚未完成'
        if(item.contact_type == 3){
            button= '<a id="'+btn+'" class="a_ready" onclick="openApply('+i+')">完成</a>';
        }
    }
    if(item.task_status == "1" && contact_record==''){
        contact_record = '没有记录'
    }
    $("#listBox4").append('<li id="'+liID+'" class="'+style+'"><div onclick="gotoDetails('+item.contact_id+','+item.status+')" class="list-left pull-left"><div class="list-infoContent2 clearfix"><p class="l-i-1 list-info pull-left">'+time+'<span>'+item.task_date+'</span></p><p class="l-i-2 list-info pull-left">'+user+'<span>'+item.contact_user+'</span></p><p class="l-i-3 list-info pull-left">接触类型<span>'+type+'</span></p></div><div class="list-left-info"><div class="l-i-4 list-info pull-left"><p>描述：'+contactDetail+'</p><p>记录：'+contact_record+'</p></div></div></div><div class="list-right pull-left hidden-xs"><div id="'+divID+'" class="list-right-info">'+button+'</div></div></li>');
}

function gotoDetails(contact_id,status){
    if(status != 1){
        if(clicking){
            clicking = false;
        }else{
            window.location.href = '../task_detail/contact_id='+contact_id;
        }
    }
}

function getDoc(i){
    var contact = contactList;
    var sendData = {'fundAndApply':contact[i].note,'clientType':clientType}
    $.getJSON('/getClientDoc/',sendData,function(ret){
        var documentList = ret.documentList;
        if(documentList == '403'){
            alert('获取资料出错');
        }else{
            for(var i=0;i<documentList.length;i++){
                window.open('../static/tempfiles/'+documentList[i].name);
            }
        }
    });
    clicking = true;
}

function openApply(i){
    var contact = contactList;
    var applyID = contact[i].note.split('.')[1];
    var applyType = contact[i].note.split('.')[2];
    if(applyType=='1'){
        window.open('/account_apply/applyID='+applyID);
    }else if(applyType=='2'){
        window.open('/account_add_apply/applyID='+applyID);
    }else{
        window.open('/account_redemption_apply/applyID='+applyID);
    }
}

function complete(num,contact_id){
    var li = 'li'+num;
    var quitID = 'quit'+num;
    var saveID = 'save'+num;
    var feedbackID = 'feedback-div'+num;

    var btn = 'btn'+num;
    var finish_btn = document.getElementById(btn);
    finish_btn.className = 'a_finish';
    finish_btn.innerHTML = '正在录入记录';

    $("#"+li).append('<div id="'+feedbackID+'" class="feedback input-group"><textarea id="feedback-textarea" class="form-control" placeholder="留言回访记录（可以为空）"></textarea><a id="'+quitID+'" class="quit pull-left">取消</a> <a id="'+saveID+'" class="quit pull-right">完成</a></div>');
    $("#"+quitID).click(function(){
        $("#"+feedbackID).remove();
        finish_btn.className = 'a_ready';
        finish_btn.innerHTML = '完成';
    });
    $("#"+saveID).click(function(){
        var sendData = {'client_id':clientID,'contact_id':contact_id,'contact_record':$('#feedback-textarea').val()};
        $.getJSON('/save_contact_record/',sendData,function(ret) {
            if(ret.success == 200){
                $("#listBox4").empty();
                contactList = ret.contactList;
                for(var i=0; i<contactList.length; i++){
                    var item = ret.contactList[i]
                    replaceContent2(item,i)
                }
            }
        });
    });
}

function timeFormat(time, format){
    var t = new Date(time);
    var tf = function(i){return (i < 10 ? '0' : '') + i};
    return format.replace(/yyyy|MM|dd|HH|mm|ss/g, function(a){
        switch(a){
            case 'yyyy':
                return tf(t.getFullYear());
                break;
            case 'MM':
                return tf(t.getMonth() + 1);
                break;
            case 'mm':
                return tf(t.getMinutes());
                break;
            case 'dd':
                return tf(t.getDate());
                break;
            case 'HH':
                return tf(t.getHours());
                break;
            case 'ss':
                return tf(t.getSeconds());
                break;
        }
    })
}


function getLocalTime(nS) {
   return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
}
