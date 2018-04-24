
var paginationId = 1;
$(document).ready(function(){
    var sendData = {'fundid':window.location.href.split("=")[1],'page':1}
    $.getJSON("/fund_details_chart/",sendData,function(ret){
        //intiData(ret);
        addECharts(ret.detailInfo);
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });


});

function intiData(ret){
    var detailInfo = ret.detailInfo
    //顶部
    $("#fundname").text(detailInfo.fundname);
    $("#totalasset").text(detailInfo.totalasset);
    $("#totalreturn").text(detailInfo.totalreturn);
    $("#fundnav").text(getFloat(detailInfo.fundnav,4));
    $("#navdate").text(detailInfo.navdate);
    //$("#navdate-mb").html(detailInfo.fundnav);
    //$("#navdate-mb").text("2015-10-10");
    if(detailInfo.totalreturn_rate > 0){
        $("#return-rate").append('<span class="red cl-333 font15">'+detailInfo.totalreturn_rate+'</span>');
    }else if(detailInfo.totalreturn_rate < 0){
        $("#return-rate").append('<span class="green cl-333 font15">'+detailInfo.totalreturn_rate+'</span>');
    }else{
        $("#return-rate").append('<span class="cl-333 font15">'+detailInfo.totalreturn_rate+'</span>');
    }
    //中部
    var dataArray = new Array();
    var fundNavArray = new Array();
    var fundReturnArray = new Array();
    var sh300Array = new Array();
    var gemArray = new Array();

    var fundList = ret.paginatorList[0];
    var sh300List = ret.paginatorList[1];
    var gemList = ret.paginatorList[2];
    for(var i= 0;i<fundList.length;i++){
        dataArray.push(fundList[i].date);
        fundNavArray.push(fundList[i].nav);
        fundReturnArray.push(fundList[i].return_rate);
    }
    for(var i= 0;i<sh300List.length;i++){
        sh300Array.push(sh300List[i].return_rate);
    }
    for(var i= 0;i<gemList.length;i++){
        gemArray.push(gemList[i].return_rate);
    }

    replaceList(dataArray,fundNavArray,fundReturnArray,sh300Array,gemArray);

    //底部
    $("#fundshare").html(detailInfo.fundshare);
    $("#channel").html(detailInfo.channel);
    $("#nextopenday").html(detailInfo.nextopenday);
    $("#buyday").html(detailInfo.buyday);
    $("#buynav").html(detailInfo.buynav);
    $("#buymoney").html(detailInfo.buymoney);

    addPagination(ret.pageCount);
}

function replaceContent(page){
    var sendData = {'fundid':window.location.href.split("=")[1],'page':page}
    $.getJSON("/fund_details_chart/",sendData,function(ret){
        var dataArray = new Array();
        var fundNavArray = new Array();
        var fundReturnArray = new Array();
        var sh300Array = new Array();
        var gemArray = new Array();

        var fundList = ret.paginatorList[0];
        var sh300List = ret.paginatorList[1];
        var gemList = ret.paginatorList[2];
        for(var i= 0;i<fundList.length;i++){
            dataArray.push(fundList[i].date);
            fundNavArray.push(fundList[i].nav);
            fundReturnArray.push(fundList[i].return_rate);
        }
        for(var i= 0;i<sh300List.length;i++){
            sh300Array.push(sh300List[i].return_rate);
        }
        for(var i= 0;i<gemList.length;i++){
            gemArray.push(gemList[i].return_rate);
        }
        $(".list-content").empty();
        replaceList(dataArray,fundNavArray,fundReturnArray,sh300Array,gemArray);
    });
}

function replaceList(dataArray,fundNavArray,fundReturnArray,sh300Array,gemArray){
    for(var i=0;i<dataArray.length;i++){
        var con1 = "";
        var con2 = "";
        var con3 = "";
        var fundReturn = getFloat(fundReturnArray[i],2);
        var sh300 = getFloat(sh300Array[i],2);
        var gem = getFloat(gemArray[i],2);
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
            $(".list-content").append('<li class="clearfix list-bg1"><p class="pull-left list-w1 siteText text-left">'+dataArray[i]+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(fundNavArray[i],4)+'</p><p class="pull-left list-w3 siteText text-center '+con1+'">'+(fundReturn+"%")+'</p><p class="hidden-xs pull-left list-w2 siteText text-center '+con2+'">'+(sh300+"%")+'</p><p class="hidden-xs pull-left list-w1 siteText text-right '+con3+'">'+(gem+"%")+'</p></li> ');
        }else{
            $(".list-content").append('<li class="clearfix list-bg2"><p class="pull-left list-w1 siteText text-left">'+dataArray[i]+'</p><p class="pull-left list-w2 siteText text-center">'+getFloat(fundNavArray[i],4)+'</p><p class="pull-left list-w3 siteText text-center '+con1+'">'+(fundReturn+"%")+'</p><p class="hidden-xs pull-left list-w2 siteText text-center '+con2+'">'+(sh300+"%")+'</p><p class="hidden-xs pull-left list-w1 siteText text-right '+con3+'">'+(gem+"%")+'</p></li> ');
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
            replaceContent(paginationId);
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
            replaceContent(paginationId);
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
            replaceContent(paginationId);
            $(".pagination li").eq(ID).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if(ID != i){
                    $(".pagination li").eq(i).removeClass("active");
                }
            };
        }
    });
}


function addECharts(detailInfo){
    var dataArray = new Array();
    var fundNavArray = new Array();
    var sh300Array = new Array();
    var gemArray = new Array();
    var fundNavlist = detailInfo.fundNavlist;
    var sh300list = detailInfo.sh300;
    var gemlist = detailInfo.gem;
    for(var i=0;i<fundNavlist.length;i++){
        dataArray.unshift(fundNavlist[i].date);
        fundNavArray.unshift(getFloat(fundNavlist[i].nav));
        sh300Array.unshift(getFloat(sh300list[i].return_rate));
        gemArray.unshift(getFloat(gemlist[i].return_rate));
    }
    alert(fundNavArray);
    alert(sh300Array);
    alert(gemArray);
    var max = getFloat(Math.max.apply(null, fundNavArray)+0.05,2);//最大值
    var min = getFloat(Math.min.apply(null, fundNavArray)-0.05,2);//最小值
    // 路径配置
    require.config({
        paths: {
            echarts: '../../../static/build/dist'
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
                    islandFormatter: "{a} <br>{b} : {c}"
                },
                legend: {
                    data: ["复权净值", "泸深300指数", "创业板指数"],
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
                    start : 0,
                    end : 10
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
                        max: max  //净值最高阶段
                    },
                    {
                        type : 'value',
                        name : '百分比',
                        axisLabel : {
                            formatter: '{value} %'
                        }
                    }
                ],
                series: [
                    {
                        name: "复权净值",
                        type: "line",
                        data: fundNavArray,
                    },
                    {
                        name: "泸深300指数",
                        type: "line",
                        yAxisIndex: 1,
                        data: sh300Array,
                    },
                    {
                        type: "line",
                        name: "创业板指数",
                        yAxisIndex: 1,
                        data: gemArray,
                    }
                ],
                grid: {
                    x: 45,
                    x2: 45,
                    y: 40,
                    y2: 70
                }
            };

            // 为echarts对象加载数据 
            myChart.setOption(option);
        }
    );
}

function getFloat(floatvar,digit){
    var f_x = parseFloat(floatvar);
    if (isNaN(f_x)){
        return '0.00';
    }
    if(digit == 4){
        f_x = Math.round(f_x*10000)/10000;
    }else{
        f_x = Math.round(f_x*100)/100;
    }
    var s_x = f_x.toString();
    var pos_decimal = s_x.indexOf('.');
    if (pos_decimal < 0){
        pos_decimal = s_x.length;
        s_x += '.';
    }
    while (s_x.length <= pos_decimal + 2){
        s_x += '0';
    }
    return s_x;
}


