var paginationId = 1;
var fundName = '';
var fundID = '';
var timeOut = null;
$(document).ready(function(){

    fundID = window.location.href.split("=")[1];

    var sendData = {'fundid':fundID,'page':1}
    $.getJSON("/fund_details_chart/",sendData,function(ret){
        intiData(ret);
        addECharts(ret.detailInfo);
    });

    var myDate = new Date();
    var yy = myDate.getYear();
    if(yy<1900) yy = yy+1900;
    var MM = myDate.getMonth()+1;
    if(MM<10) MM = '0' + MM;
    var dd = myDate.getDate();
    if(dd<10) dd = '0' + dd;
    //$("#txtBeginDate").val(yy+'-'+MM+'-'+dd);
    $("#txtEndDate").val(yy+'-'+MM+'-'+dd);
    $("#txtBeginDate").datepicker().on('changeDate', function(ev){
        $('#txtBeginDate').datepicker('hide');
    });

    $("#txtEndDate").datepicker().on('changeDate', function(ev){
        $('#txtEndDate').datepicker('hide');
    });

    $(".info-title-more p").mouseover(function(){
        var ID = $(this).index();
        $(this).addClass("info-title-more-curr");
        $(this).siblings().removeClass("info-title-more-curr");
        if(ID == 0){
            $("#info2_content1").css("display", "block");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "none");
        }
        else if(ID == 1){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "block");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "none");
        }
        else if(ID == 2){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "block");
            $("#info2_content4").css("display", "none");
        }
        else if(ID == 3){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "none");
            $("#info2_content3").css("display", "none");
            $("#info2_content4").css("display", "block");
        }
    });

    $.getJSON('/fund_info/',{'fundid':window.location.href.split("=")[1]},function(ret){
        fundName = ret.fundinfo.fundname;
        $("#info1-title p").text(fundName);
        $("#i1 em").text(getFloat(ret.fundinfo.fundnav,4));
        $("#i2 em").text(getFloat(ret.fundinfo.totalnav,4));
        $("#i3 em").text(getFloat(ret.fundinfo.weekreturn*100,2)+'%');
        $("#i4 em").text(getFloat(ret.fundinfo.totalreturn*100,2)+'%');
        $("#i5 em").text(ret.fundinfo.navday);
        $("#info1-clrq-mb").text('净值日期：'+ret.fundinfo.navday);

        //获取并填充投资经理姓名、职位、头像
        var position = getPositon(ret.fundinfo.manager);
        var imgSrc = getSrc(ret.fundinfo.manager);

        $("#info1-jl-name").html(ret.fundinfo.manager+'  ('+position+')');
        $("#details-userInfo p").html(ret.fundinfo.manager);
        $("#details-userInfo em").text(position);

        document.getElementById("info1-jl-pic").src=imgSrc;
        document.getElementById("details-userInfo-pic").src=imgSrc;

        $("#info1-cpzx-btn1").click(function(){
            var sendDate = {'choosedFund':fundName}
            $.get('/get_ready_for_bespeak/',sendDate,function(ret){
                window.location.href = ret.url;
            });
        });
        $("#details-cpzx-btn2").click(function(){
            var sendDate = {'choosedFund':fundName}
            $.get('/get_ready_for_bespeak/',sendDate,function(ret){
                window.location.href = ret.url;
            });
        });
        $("#txtBeginDate").val(ret.fundinfo.startday);

        $("#info3-lists li span").eq(0).text(ret.fundinfo.fundname);
        $("#info3-lists li span").eq(1).text(ret.fundinfo.startday);
        $("#info3-lists li span").eq(2).text(ret.fundinfo.trade_date);
        $("#info3-lists li span").eq(3).text(ret.fundinfo.producttype);
        $("#info3-lists li span").eq(4).text(ret.fundinfo.fundcustodian);
        $("#info3-lists li span").eq(5).text(ret.fundinfo.manager);
        $("#info3-lists li span").eq(6).text(ret.fundinfo.outsource);
        $("#info3-lists li span").eq(7).text(ret.fundinfo.saleschannel);
        
        
        if(fundID=="ddf34ffdd212425199cf6bd79e4ddad7"||fundID=="0690594abccf49dd961925c210017da0"){
            $("#info3-lists li span").eq(8).text("持有超过12个月的份额，每年可赎回1/3，赎回后持有的投资金额不低于100万元（当年未发生赎回的可累计总额）。开放日为每月最后一个交易日");
        }
        else if(fundID=="0f473e12319311e7898300155d64b502"){
            $("#info3-lists li span").eq(8).text("持有超过12个月的份额，每年可赎回1/8，赎回后持有的投资金额不低于100万元（当年未发生赎回的可累计总额）。开放日为每月最后一个交易日");
        }
        else{
            $("#info3-lists li span").eq(8).text(ret.fundinfo.closureperiod);
        }
        
        if(fundID == "6b54a6a145a74fc7b360dcdce32801c9"){
            $("#info3-lists li span").eq(9).text("每日开放");
        }else{
            $("#info3-lists li span").eq(9).text(ret.fundinfo.nextopenday);
        }
        if(ret.fundinfo.directsale == '直销'){
            $("#info3-lists li span").eq(10).text(ret.fundinfo.endpurday+'前');
            $("#info3-lists li span").eq(11).text(ret.fundinfo.begredemday+'~'+ret.fundinfo.endredemday);
        }else{
            $("#info3-lists li span").eq(10).text('咨询代销渠道');
            $("#info3-lists li span").eq(11).text('咨询代销渠道');
        }
        $("#info3-lists li span").eq(12).text(ret.fundinfo.suppsubcribpoint);
        $("#info3-lists li span").eq(14).text(ret.fundinfo.investmentscope);
        $("#info3-lists li span").eq(15).text(ret.fundinfo.investmentstrategy);
        if(ret.fundinfo.warningline==0){
            $("#info3-lists li span").eq(16).text('无');
        }else{
            $("#info3-lists li span").eq(16).text(ret.fundinfo.warningline);
        }
        if(ret.fundinfo.closeline==0){
            $("#info3-lists li span").eq(17).text('无');
        }else{
            $("#info3-lists li span").eq(17).text(ret.fundinfo.closeline);
        }
        $("#info3-lists li span").eq(18).text(fondsFormat(getFloat(ret.fundinfo.totalshares,2)));

        $("#info3-lists li span").eq(19).text(ret.fundinfo.total_investor_count);
        if(getFloat(ret.fundinfo.total_investor_count,2) > 150){
            $("#info3-lists li span").eq(19).css('color','red');
        }

        if(ret.fundinfo.outsourcefee==0){
            $("#info3-lists li span").eq(20).text('-');
        }else{
            $("#info3-lists li span").eq(20).text(formatSpecialNumber(getFloat(ret.fundinfo.outsourcefee,3))+'％／年');
        }
        if(ret.fundinfo.outsourcefee==0){
            $("#info3-lists li span").eq(21).text('-');
        }else{
            $("#info3-lists li span").eq(21).text(formatSpecialNumber(getFloat(ret.fundinfo.custodianfee,3))+'％／年');
        }
        if(ret.fundinfo.custodianfee==0){
            $("#info3-lists li span").eq(21).text('-');
        }else{
            $("#info3-lists li span").eq(21).text(formatSpecialNumber(getFloat(ret.fundinfo.custodianfee,3))+'％／年');
        }
        if(ret.fundinfo.salessfee==0){
            $("#info3-lists li span").eq(22).text('-');
        }else{
            $("#info3-lists li span").eq(22).text(formatSpecialNumber(getFloat(ret.fundinfo.salessfee,3))+'％／年');
        }
        if(ret.fundinfo.managefee==0){
            $("#info3-lists li span").eq(23).text('-');
        }else{
            $("#info3-lists li span").eq(23).text(formatSpecialNumber(getFloat(ret.fundinfo.managefee,3))+'％／年');
        }
        if(ret.fundinfo.invest_advisor_fee==0){
            $("#info3-lists li span").eq(24).text('-');
        }else{
            $("#info3-lists li span").eq(24).text(formatSpecialNumber(getFloat(ret.fundinfo.invest_advisor_fee,3))+'％／年');
        }

        if(ret.fundinfo.purchfee==0){
            if(ret.fundinfo.directsale == '直销'){
                $("#info3-lists li span").eq(25).text('0');
            }else{
                $("#info3-lists li span").eq(25).text('咨询代销渠道');
            }
        }else{
            $("#info3-lists li span").eq(25).text(ret.fundinfo.purchfee*100+'%');
        }
        if(ret.fundinfo.resultdeduct==0){
            $("#info3-lists li span").eq(26).text('-');
        }else{
            $("#info3-lists li span").eq(26).text(ret.fundinfo.resultdeduct*100+'％');
        }
        if(ret.fundinfo.deducttype == 1){
            $("#info3-lists li span").eq(27).text('减净值');
        }else if(ret.fundinfo.deducttype == 2){
            $("#info3-lists li span").eq(27).text('减份额');
        }else{
            $("#info3-lists li span").eq(27).text('-');
        }
        if(ret.fundinfo.performance_frequency != ""){
            $("#info3-lists li span").eq(28).text(ret.fundinfo.performance_frequency);
        }else{
            $("#info3-lists li span").eq(28).text('-');
        }
        $("#info3-lists li span").eq(29).text('上海高毅资产管理合伙企业（有限合伙）');
        if(ret.fundinfo.dedectthreshold==0){
            $("#info3-lists li span").eq(30).text('-');
        }else{
            $("#info3-lists li span").eq(30).text(getFloat(ret.fundinfo.dedectthreshold,4));
        }

        //母基金显示基金报告
        if(ret.fundinfo.fundreports && ret.fundinfo.fundreports.length > 0){
            $("#exportBtn1").css("display", "none");
            $("#exportBtn2").css("margin-top", -40);
            var fundreports = ret.fundinfo.fundreports;
            for(var i=0;i<fundreports.length;i++){
                $("#content3_record").append('<li class="border-b"><a href="javascript:void(0);" onclick="js_method_1('+fundreports[i].reportid+')" ondblclick="js_method_2('+fundreports[i].reportid+')" class="clearfix"><p class="pull-left textEllipsis cl-666">'+fundreports[i].reportname+'</p><span class="cl-999 pull-right hidden-xs">'+fundreports[i].publish_date+'</span></a><button id="sendBtn" onclick="sendmail('+fundreports[i].reportid+')" class="pull-right hidden-xs">发 送</button></li> ')
            }
        }else{
             $("#menu3").css("display", "none");
        }
        //addListener();
    });

    $("#exportBtn1").click(function(){
        var beginDate = $("#txtBeginDate").val();
        var endDate = $("#txtEndDate").val();
        var riskFree = $("#riskFree").val();
        var sendDate = {'beginDate':beginDate,'endDate':endDate,'riskFree':riskFree,'fundID':fundID,'type':112};
        $('#sendbg').css('display','block');
        document.getElementById('sendbg').getElementsByTagName('span')[0].innerHtml = '正在导出数据，预计需要5秒钟，请耐心等待';
        //document.getElementById('sendbgSpan').innerText = '正在导出数据，预计需要5秒钟，请耐心等待';
        $.get('/get_estimate_nav/',sendDate,function(ret){
            $('#sendbg').css('display','none');
            if(ret.success == 200){
                window.open(ret.excalurl);
            }else{
                alert('暂无该区间数据！');
            }
        });
    });

    $("#exportBtn2").click(function(){
        var beginDate = $("#txtBeginDate").val();
        var endDate = $("#txtEndDate").val();
        var riskFree = $("#riskFree").val();
        var sendDate = {'beginDate':beginDate,'endDate':endDate,'riskFree':riskFree,'fundID':fundID,'type':113};
        $('#sendbg').css('display','block');
        document.getElementById('sendbg').getElementsByTagName('span')[0].innerHtml = '正在导出数据，预计需要5秒钟，请耐心等待';
        //document.getElementById('sendbgSpan').innerText = '正在导出数据，预计需要5秒钟，请耐心等待';
        $.get('/get_estimate_nav/',sendDate,function(ret){
            $('#sendbg').css('display','none');
            if(ret.success == 200){
                window.open(ret.excalurl);
            }else{
                alert('暂无该区间数据！');
            }
        });
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });

    $("#filter-mb-btn1").click(function(){
        $("#filter-mb-cp").slideToggle();
    });
    $("#filter-mb-btn2").click(function(){
        $("#filter-mb-px").slideToggle();
    });
});

function formatSpecialNumber(oValue){
    oValue = oValue +'';
    
    if(oValue.substring(oValue.length-1)=='0'){
        return oValue.substring(0,oValue.length-1);
    }
    return oValue;
}

function js_method_1(reportid){
    clearTimeout(timeOut);
    timeOut = setTimeout(function(){
        $.getJSON("/report/",{"reportid":reportid},function(ret){
            window.open(ret.url);
        });
    },300);
}

function js_method_2(reportid){
    clearTimeout(timeOut);
    sendmail(reportid);
}

function sendmail(reportid){
    var email_to = prompt('客户的Email为：');
    if(email_to != null ){
        if(email_to == ''){
            alert('请填写客户的Email');
        }else{
            $('#sendbg').css('display','block');
            $.getJSON("/sendmail/",{"reportid":reportid,"email_to":email_to},function(ret){
                $('#sendbg').css('display','none');
                if(ret.success == 200){
                    alert('发送成功');
                }else{
                    alert('发送失败');
                }
            });
        }
    }
}

function getPositon(managerName){
    switch (managerName){
        case '邱国鹭':
            return '高毅资产董事长';
        case '邓晓峰':
            return '首席投资官';
        case '卓利伟':
            return '首席研究官';
        default :
            return '董事总经理';
    }
}

function getSrc(managerName){
    switch (managerName){
        case '邱国鹭':
            return '../static/img/account/qgl.png';
        case '邓晓峰':
            return '../static/img/account/dxf.png';
        case '孙庆瑞':
            return '../static/img/account/sqr.png';
        case '卓利伟':
            return '../static/img/account/zlw.png';
        case '冯柳':
            return '../static/img/account/fl.png';
        case '王世宏':
            return '../static/img/account/wsh.png';
    }
}

function addECharts(detailInfo){
    var dataArray = new Array();
    var fundNavArray = new Array();
    var sh300Array = new Array();
    var gemArray = new Array();
    var fundNavlist = detailInfo.fundNavlist;
    var sh300list = detailInfo.sh300;
    var gemlist = detailInfo.gem;
    var firstsh300 = sh300list[fundNavlist.length-1].nav;
    var firstgem = gemlist[fundNavlist.length-1].nav
    for(var i=0;i<fundNavlist.length;i++){
        dataArray.unshift(fundNavlist[i].date);
        fundNavArray.unshift(getFloat(fundNavlist[i].totalnav,4));
        sh300Array.unshift(getFloat(sh300list[i].nav/firstsh300,4));
        gemArray.unshift(getFloat(gemlist[i].nav/firstgem,4));
    }
    var max1 = getFloat(Math.max.apply(null, fundNavArray),4); //最大值
    var max2 = getFloat(Math.max.apply(null, sh300Array),4); //最大值
    var max3 = getFloat(Math.max.apply(null, gemArray),4); //最大值
    var max = getFloat(Math.max.apply(null, [max1,max2,max3]),4)+0.2;
    //var min = 0.5;
    var min1 = getFloat(Math.min.apply(null, fundNavArray),4); //最小值
    var min2 = getFloat(Math.min.apply(null, sh300Array),4); //最大值
    var min3 = getFloat(Math.min.apply(null, gemArray),4); //最大值
    var min = getFloat(Math.min.apply(null, [min1,min2,min3]),4)-0.2;

    // 路径配置
    require.config({
        paths: {
            echarts: '../../static/build/dist'
        }
    });
    // 使用
    require(
        [
            'echarts',
            'echarts/chart/line' // 使用柱状图就加载bar模块，按需加载
        ],
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('echartsContainer'));
            window.onresize = myChart.resize;
            var option ={

                tooltip: {
                    trigger: "axis",
                    islandFormatter: "{a} <br> {b} : {c}"
                },
                legend: {
                    data: ["累计净值", "沪深300指数", "创业板指数"],
                    y: 10,
                    x: "center"
                },
                toolbox: {
                    feature: {
                        dataView: {
                            readOnly: true,
                            show: false
                        },
                        magicType: {
                            type: ["line", "bar"],
                            show: false
                        },
                        mark: {
                            show: true
                        },
                        dataZoom: {
                            show: true
                        },
                        restore: {
                            show: true
                        },
                        saveAsImage: {
                            show: true
                        }
                    },
                    backgroundColor: "rgb(255, 255, 0)",
                    showTitle: true,
                    x: "center",
                    show: false
                },
                dataZoom : {
                    show : true,
                    realtime: true,
                },
                xAxis: [
                    {
                        type: "category",
                        boundaryGap: false,
                        data: dataArray,
                        splitArea: {
                            show: false
                        },
                        axisLine: {
                            show: true
                        },
                        splitLine: {
                            show: true
                        }
                    }
                ],
                yAxis: [
                    {
                        type : 'value',
                        name : '净值',
                        min: min, //净值最低阶段
                        max: max,  //净值最高阶段
                        scale: true,
                        axisLabel : {
                            formatter: function(value) {
                                return getFloat(value,2);
                            }
                        },
                    },
                ],

                series: [
                    {
                        name: "累计净值",
                        type: "line",
                        data: fundNavArray,
                    },
                    {
                        name: "沪深300指数",
                        type: "line",
                        //yAxisIndex: 1,
                        data: sh300Array,
                    },
                    {
                        name: "创业板指数",
                        type: "line",
                        //yAxisIndex: 1,
                        data: gemArray,
                    }
                ],
                grid: {
                    x: 45,
                    x2: 55,
                    y: 45,
                    y2: 60
                }
            };
            // 为echarts对象加载数据
            myChart.setOption(option);
        }
    );
}

function intiData(ret){
    var dataArray = new Array();
    var fundNavArray = new Array();
    var totalNavArray = new Array();
    var fundReturnArray = new Array();
    var sh300Array = new Array();
    var gemArray = new Array();

    var fundList = ret.paginatorList[0];
    var sh300List = ret.paginatorList[1];
    var gemList = ret.paginatorList[2];
    for(var i= 0;i<fundList.length;i++){
        dataArray.push(fundList[i].date);
        fundNavArray.push(fundList[i].nav);
        totalNavArray.push(fundList[i].totalnav);
        fundReturnArray.push(fundList[i].return_rate);
    }
    for(var i= 0;i<sh300List.length;i++){
        sh300Array.push(sh300List[i].return_rate);
    }
    for(var i= 0;i<gemList.length;i++){
        gemArray.push(gemList[i].return_rate);
    }
    replaceList(dataArray,fundNavArray,totalNavArray,fundReturnArray,sh300Array,gemArray);

    if(ret.pageCount>1){
        addPagination(ret.pageCount);
        addLoadMore();
    }
}

function addLoadMore(){
    $(".loadMore").append('<img id="loadMoreImage" src="../static/img/global/more.png">');
    $(".loadMore img").click(function(){
        $(".loadMore img").attr("src","../static/img/global/more.gif");
        paginationId++;
        replaceContent(paginationId,true);
    });
}

function replaceContent(page,type){
    var sendData = {'fundid':window.location.href.split("=")[1],'page':page}
    $.getJSON("/fund_details_chart/",sendData,function(ret){
        $(".loadMore img").attr("src","../static/img/global/more.png");
        var dataArray = new Array();
        var fundNavArray = new Array();
        var totalNavArray = new Array();
        var fundReturnArray = new Array();
        var sh300Array = new Array();
        var gemArray = new Array();

        var fundList = ret.paginatorList[0];
        var sh300List = ret.paginatorList[1];
        var gemList = ret.paginatorList[2];
        for(var i= 0;i<fundList.length;i++){
            dataArray.push(fundList[i].date);
            fundNavArray.push(fundList[i].nav);
            totalNavArray.push(fundList[i].totalnav);
            fundReturnArray.push(fundList[i].return_rate);
        }
        for(var i= 0;i<sh300List.length;i++){
            sh300Array.push(sh300List[i].return_rate);
        }
        for(var i= 0;i<gemList.length;i++){
            gemArray.push(gemList[i].return_rate);
        }
        if(!type){
            $(".list-content").empty();
        }
        if(page==ret.pageCount){
            $(".loadMore").empty();
        }
        replaceList(dataArray,fundNavArray,totalNavArray,fundReturnArray,sh300Array,gemArray);
    });
}

function replaceList(dataArray,fundNavArray,totalNavArray,fundReturnArray,sh300Array,gemArray){
    for(var i=0;i<dataArray.length;i++){
        var con1 = "";
        var con2 = "";
        var con3 = "";
        var fundReturn = getFloat(fundReturnArray[i]*100,2);
        var sh300 = getFloat(sh300Array[i]*100,2);
        var gem = getFloat(gemArray[i]*100,2);
        if(fundReturn > 0){
            con1 = 'red';
        }else if(fundReturn < 0){
            con1 = 'green';
        }
        if(sh300 > 0){
            con2 = 'red';
        }else if(sh300 < 0){
            con2 = 'green';
        }
        if(gem > 0){
            con3 = 'red';
        }else if(gem < 0){
            con3 = 'green';
        }
        if(i%2==0){
            $(".list-content").append('<li class="clearfix list-bg1"><p class="pull-left list-w1 siteText text-left">'+dataArray[i]+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(fundNavArray[i],4)+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(totalNavArray[i],4)+'</p><p class="pull-left list-w3 siteText text-center '+con1+'">'+(fundReturn+"%")+'</p><p class="hidden-xs pull-left list-w2 siteText text-center '+con2+'">'+(sh300+"%")+'</p><p class="hidden-xs pull-left list-w1 siteText text-right '+con3+'">'+(gem+"%")+'</p></li> ');
        }else{
            $(".list-content").append('<li class="clearfix list-bg2"><p class="pull-left list-w1 siteText text-left">'+dataArray[i]+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(fundNavArray[i],4)+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(totalNavArray[i],4)+'</p><p class="pull-left list-w3 siteText text-center '+con1+'">'+(fundReturn+"%")+'</p><p class="hidden-xs pull-left list-w2 siteText text-center '+con2+'">'+(sh300+"%")+'</p><p class="hidden-xs pull-left list-w1 siteText text-right '+con3+'">'+(gem+"%")+'</p></li> ');
        }

    }
}

function addPagination(num){

    var con = "";
    for (var i = 0; i < num; i++) {
        con = con + "<li><a>" + (i+1) + "</a></li>";
    };


    $(".pagination").empty();
    $(".pagination").append(
        '<li><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        +con
        +'<li><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
    );

    $(".pagination li").eq(1).addClass("active");

    paginationAddEvent();
}

function paginationAddEvent(){
    var paginationId = 1;

    $(".pagination li").click(function(){
        var ID = $(this).index();
        if(ID == 0){
            // 上一页
            console.log("上一页");

            paginationId--;
            if(paginationId < 1){
                paginationId = 1;
                return;
            }
            replaceContent(paginationId,false);
            $(".pagination li").eq(paginationId).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if(paginationId != i){
                    $(".pagination li").eq(i).removeClass("active");
                }
            };

        }else if(ID == $(".pagination li").length - 1){
            // 下一页
            console.log("下一页");

            paginationId++;
            if(paginationId > $(".pagination li").length - 2){
                paginationId = $(".pagination li").length - 2;
                return;
            }
            replaceContent(paginationId,false);
            $(".pagination li").eq(paginationId).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if(paginationId != i){
                    $(".pagination li").eq(i).removeClass("active");
                }
            };

        }else{
            // 切换到第几页（12345）
            console.log(ID);
            paginationId = ID;
            replaceContent(paginationId,false);
            $(".pagination li").eq(ID).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if(ID != i){
                    $(".pagination li").eq(i).removeClass("active");
                }
            };
        }
    });
}
