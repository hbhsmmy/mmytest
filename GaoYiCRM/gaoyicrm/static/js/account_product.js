var oldPx = "默认排序";
var jjjlName = "全部";
var px = 0;
var lx = "全部";
var paginationId = 1;
var searchContent = '';
$(document).ready(function(){

    getManager();

    $(window).keydown(function (e) {
        if (e.which == 13) {
            $(".loadMore").empty();
            searchContent = $("#user-search").val();
            getProduct(jjjlName,'份额净值',px,lx,searchContent,1,true,true);
        }
    });

    $("#searchBtn").click(function(){
        $(".loadMore").empty();
        searchContent = $("#user-search").val();
        $("#filter-jjjl p").removeClass("filter-curr");
        $("#filter-jjjl p").eq(0).addClass("filter-curr");
        getProduct('全部','份额净值',px,lx,searchContent,1,true,true);
    });

    //for (var i = 0; i < $("#filter-jjjl p").length; i++) {
    //    if($("#filter-jjjl p").eq(i).text() == jjjlName){
    //        $("#filter-jjjl p").eq(i).addClass("filter-curr");
    //    }else{
    //        $("#filter-jjjl p").eq(i).removeClass("filter-curr");
    //    }
    //};
    //
    //getProduct(jjjlName,'份额净值',px,lx,searchContent,1,true,true);

    //$("#filter-jjjl p").click(function(){
    //    $(this).addClass("filter-curr");
    //    $(this).siblings().removeClass("filter-curr");
    //    jjjlName = $(this).text();
    //    getProduct(jjjlName,$("#filter-px .filter-curr").text(),px,lx,searchContent,1,true,false);
    //    $("#filter-mb-cp").slideToggle();
    //});
    $("#filter-lx p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        lx = $(this).text();
        getProduct(jjjlName,$("#filter-px .filter-curr").text(),px,lx,searchContent,1,true,false);
    });
    $("#filter-px p").click(function() {
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        if ($(this).children("span").text() != '默认排序') {
            if ($(this).children("span").text() != oldPx) {
                px = 0;
                oldPx = $(this).children("span").text();
                $(this).children("img").remove();
                $(this).append('<img src="../static/img/global/paixujiantou2.png" alt="">');
            } else {
                if ($(this).children("img").attr("src") == "../static/img/global/paixujiantou1.png") {
                    $(this).children("img").attr("src", "../static/img/global/paixujiantou2.png");
                    px = 0;
                } else {
                    $(this).children("img").attr("src", "../static/img/global/paixujiantou1.png");
                    px = 1;
                }
            }
        }
        getProduct($("#filter-jjjl .filter-curr").text(),$(this).text(),px,lx,searchContent,1,true,false);
        $("#filter-mb-px").slideToggle();
    });

    //$("#filter-mb-cp p").click(function(){
    //    $(this).addClass("hide");
    //    $(this).removeClass("show");
    //    $(this).siblings().removeClass("hide");
    //    $(this).siblings().addClass("show");
    //    $("#filter-mb-btn1 span").text($(this).text());
    //    $(".loadMore").empty();
    //    getProduct($(this).text(),$("#filter-mb-btn2 span").text(),px,lx,searchContent,1,true,true);
    //    $("#filter-mb-cp").slideToggle();
    //});
    $("#filter-mb-px p").click(function(){
        $(this).addClass("hide");
        $(this).removeClass("show");
        $(this).siblings().removeClass("hide");
        $(this).siblings().addClass("show");
        $("#filter-mb-btn2 span").text($(this).text());
        $(".loadMore").empty();
        getProduct($("#filter-mb-btn1 span").text(),$(this).text(),px,lx,searchContent,1,true,true);
        $("#filter-mb-px").slideToggle();
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

function managerClick(value){
    $('#filter-jjjl').children().removeClass("filter-curr");
    $('#filter-jjjl').children().eq(value+1).addClass("filter-curr");
    jjjlName = $('#filter-jjjl').children().eq(value+1).text();
    getProduct(jjjlName,$("#filter-px .filter-curr").text(),px,lx,searchContent,1,true,false);
    $("#filter-mb-cp").slideToggle();
}
function mobileManagerClick(value){
    $('#filter-mb-cp').children().removeClass("hide");
    $('#filter-mb-cp').children().addClass("show");
    $('#filter-mb-cp').children().eq(value).addClass("hide");
    $('#filter-mb-cp').children().eq(value).removeClass("show");
    jjjlName = $('#filter-mb-cp').children().eq(value).text();
    $("#filter-mb-btn1 span").text(jjjlName);
    $(".loadMore").empty();
    getProduct(jjjlName,$("#filter-mb-btn2 span").text(),px,lx,searchContent,1,true,true);
    $("#filter-mb-cp").slideToggle();
}

function getManager(){
    $.getJSON('/get_manager/',function(ret){
        $('#filter-jjjl').append('<p class="pull-left filter-curr" onclick="managerClick(0)">全部</p>');
        $('#filter-mb-cp').append('<p class="pull-left hide" onclick="mobileManagerClick(0)">全部</p>');
        for(var i=0;i<ret.managerList.length;i++){
            var item = ret.managerList[i];
            $('#filter-jjjl').append('<p class="pull-left" onclick="managerClick('+item.value+')">'+item.name+'</p>');
            $('#filter-mb-cp').append('<p class="pull-left" onclick="mobileManagerClick('+item.value+')">'+item.name+'</p>');
        }
    });
    getProduct(jjjlName,'份额净值',px,lx,searchContent,1,true,true);
}

//type:手机访问模式为Ture，电脑访问模式为False
function getProduct(manager, order, px, lx, searchContent, page, first, type){
    if(searchContent == ''){
        var sendDate = {'manager':manager,'order':order,'px':px,'type':lx,'page':page}
    }else{
        var sendDate = {'manager':manager,'order':order,'search':searchContent,'px':px,'type':lx,'page':page}
    }

    $.getJSON('/get_product/',sendDate,function(ret){
        if(first){
            if(ret.pageCount > 1){
                addLoadMore();
                addPagination(ret.pageCount,page);
            }else{
                $(".pagination").empty();
            }
        }
        if(type){
            $(".loadMore img").attr("src","../static/img/global/more.png");
            if(first){
                $("#listBox").empty();
            }
            if(ret.pageCount == 1){
                $(".loadMore").empty();
            }
            if(page == ret.pageCount){
                $(".loadMore").empty();
            }
        }else{
            $("#listBox").empty();
        }
        for (var i = 0, len = ret.productList.length; i < len; i++){
            var item = ret.productList[i];
            replaceContent(item['fundid'],item['name'], item['startday'], getFloat(item['nav'],4), getFloat(item['weekreturn']*100,2), getFloat(item['totalreturn']*100,2), item['navday'],item['totalshares'], "100", i);
        }
    });
}

function addLoadMore(){
    $(".loadMore").append('<img id="loadMoreImage" src="../static/img/global/more.png">');
    $(".loadMore img").click(function(){
        $(".loadMore img").attr("src","../static/img/global/more.gif");
        paginationId++;
        getProduct($("#filter-mb-btn1 span").text(),$("#filter-mb-btn2 span").text(),px,lx,searchContent,paginationId,false,true);
    });
}

// "标题", "成立时间", "单位净值", "累计净值", "累计收益率", "净值日期"
function replaceContent(id, title, clrq, dwjz, zsyl, ljsyl, jzrq, totalshares ,yuyueNum, i){
    var con1 = '';
    var con2 = '';
    var title = title;
    if(zsyl>0){
        con1 = '<em class="red">'
    }else{
        con1 = '<em class="green">'
    }
    if(ljsyl>0){
        con2 = '<em class="red">'
    }else{
        con2 = '<em class="green">'
    }
    if(i%2==0){
        if(ljsyl > 0){
            $("#listBox").append('<li class="listBg1"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1+ zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }else if(ljsyl < 0){
            $("#listBox").append('<li class="listBg1"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1 + zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }else{
            $("#listBox").append('<li class="listBg1"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1 + zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }
    }else{
        if(ljsyl > 0){
            $("#listBox").append('<li class="listBg2"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1 + zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }else if(ljsyl < 0){
            $("#listBox").append('<li class="listBg2"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1 + zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }else{
            $("#listBox").append('<li class="listBg2"><div class="list-left pull-left"><a href="../account_details/fund='+id+'" target="_blank" class="list-title clearfix"><p class="pull-left">' + title + '</p><em class="pull-right hidden-xs">' + clrq + ' 成立</em><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_details/fund='+id+'" target="_blank" class="list-infoContent clearfix"><div class="l-i-1 list-info pull-left"><p>份额净值</p><em>' + dwjz + '</em></div><div class="l-i-2 list-info pull-left"><p>周涨跌幅</p>'+con1 + zsyl+'%' + '</em></div><div class="l-i-3 list-info pull-left"><p>累计收益率</p>'+con2 + ljsyl+'%' + '</em></div><div class="l-i-4 list-info pull-left"><p>净值日期</p><em>' + jzrq + '</em></div><div class="l-i-5 list-info pull-right"><p>基金总份额</p><em>' + fondsFormat(getFloat(totalshares,2)) + '</em></div></a></div></li>');
        }
    }
}

function addPagination(num,page){

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

    $(".pagination li").eq(page).addClass("active");
    paginationAddEvent(page);
}


function paginationAddEvent(page) {
    paginationId = page;

    $(".pagination li").click(function () {
        var ID = $(this).index();

        if (ID == 0) {
            // 上一页
            paginationId--;

            if (paginationId < 1) {
                paginationId = 1;
                return;
            }

            getProduct($("#filter-jjjl .filter-curr").text(),$("#filter-px .filter-curr").text(),px,lx,searchContent,paginationId,false,false);

            $(".pagination li").eq(paginationId).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if (paginationId != i) {
                    $(".pagination li").eq(i).removeClass("active");
                }
            }
            ;

        } else if (ID == $(".pagination li").length - 1) {
            // 下一页

            paginationId++;
            if (paginationId > $(".pagination li").length - 2) {
                paginationId = $(".pagination li").length - 2;
                return;
            }
            getProduct($("#filter-jjjl .filter-curr").text(),$("#filter-px .filter-curr").text(),px,lx,searchContent,paginationId,false,false);

            $(".pagination li").eq(paginationId).addClass("active");

            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if (paginationId != i) {
                    $(".pagination li").eq(i).removeClass("active");
                }
            };
        } else {
            paginationId = ID;
            getProduct($("#filter-jjjl .filter-curr").text(),$("#filter-px .filter-curr").text(),px,lx,searchContent,paginationId,false,false);
            $(".pagination li").eq(ID).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if (ID != i) {
                    $(".pagination li").eq(i).removeClass("active");
                }
            };
        }
    });
}
