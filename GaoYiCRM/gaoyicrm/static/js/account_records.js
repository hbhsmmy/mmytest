var clientDetail;
var Khlx=0;
var Khqd=0;
var Khzt=0;
var Jjjl=0;
var classifyOrNot=false;
var paginationId = 1;
var searchContent = '';
var searchOrNot = false;

$(document).ready(function(){

    getManager();

    $(window).keydown(function (e) {
        if (e.which == 13) {
            searchContent = $("#user-search").val();
            if(searchContent == ''){
                alert('请输入您要检索的内容');
            }else{
                $("#filter-khlx p").removeClass("filter-curr");
                $("#filter-khlx p").eq(0).addClass("filter-curr");
                $("#filter-khqd p").removeClass("filter-curr");
                $("#filter-khqd p").eq(0).addClass("filter-curr");
                $("#filter-khzt p").removeClass("filter-curr");
                $("#filter-khzt p").eq(0).addClass("filter-curr");
                $("#filter-jjjl p").removeClass("filter-curr");
                $("#filter-jjjl p").eq(0).addClass("filter-curr");
                searchOrNot = true;
                classifyOrNot = false;
                getSearchList(searchContent,1,true,true);
            }
        }
    });

    $.getJSON('/get_user_count/',function(ret) {
        $("#user-count").text('共'+ret.len+'名客户')
    });
    $("#userBtn_pc").click(function(){
        window.open('../account_editor');
    });
    $("#userBtn_mb").click(function(){
        window.open('../account_editor');
    });
    $("#searchBtn").click(function(){
        searchContent = $("#user-search").val();
        if(searchContent == ''){
            alert('请输入您要检索的内容');
        }else{
            $("#filter-khlx p").removeClass("filter-curr");
            $("#filter-khlx p").eq(0).addClass("filter-curr");
            $("#filter-khqd p").removeClass("filter-curr");
            $("#filter-khqd p").eq(0).addClass("filter-curr");
            $("#filter-khzt p").removeClass("filter-curr");
            $("#filter-khzt p").eq(0).addClass("filter-curr");
            $("#filter-jjjl p").removeClass("filter-curr");
            $("#filter-jjjl p").eq(0).addClass("filter-curr");
            searchOrNot = true;
            classifyOrNot = false;
            getSearchList(searchContent,1,true,true);
        }
    });
    $("#filter-khlx p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        Khlx = khlxNum($(this).text());
        Khqd = khqdNum($("#filter-khqd .filter-curr").text());
        Khzt = khztNum($("#filter-khzt .filter-curr").text());
        Jjjl = jjjlNum($("#filter-jjjl .filter-curr").text());
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
    });

    $("#filter-khqd p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        Khlx = khlxNum($("#filter-khlx .filter-curr").text());
        Khqd = khqdNum($(this).text());
        Khzt = khztNum($("#filter-khzt .filter-curr").text());
        Jjjl = jjjlNum($("#filter-jjjl .filter-curr").text());
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
    });

    $("#filter-khzt p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        Khlx = khlxNum($("#filter-khlx .filter-curr").text());
        Khqd = khqdNum($("#filter-khqd .filter-curr").text());
        Khzt = khztNum($(this).text());
        Jjjl = jjjlNum($("#filter-jjjl .filter-curr").text());
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
    });

    //$("#filter-jjjl p").click(function(){
    //    $(this).addClass("filter-curr");
    //    $(this).siblings().removeClass("filter-curr");
    //    Khlx = khlxNum($("#filter-khlx .filter-curr").text());
    //    Khqd = khqdNum($("#filter-khqd .filter-curr").text());
    //    Khzt = khztNum($("#filter-khzt .filter-curr").text());
    //    Jjjl = jjjlNum($(this).text());
    //    if(searchOrNot){
    //        getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    //    }else{
    //        searchOrNot = false;
    //        classifyOrNot = true;
    //        paginationId = 1;
    //        getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    //    }
    //});

    //移动端客户类型筛选
    $("#filter-mb-cp p").click(function(){
        $(this).addClass("hide");
        $(this).removeClass("show");
        $(this).siblings().removeClass("hide");
        $(this).siblings().addClass("show");
        $("#filter-mb-btn1 span").text($(this).text());
        Khlx = khlxNum($("#filter-mb-btn1 span").text().substr(3));
        Khqd = khqdNum($("#filter-mb-btn2 span").text().substr(3));
        Khzt = khztNum($("#filter-mb-btn3 span").text().substr(3));
        Jjjl = jjjlNum($("#filter-mb-btn4 span").text().substr(3));
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
        $("#filter-mb-cp").slideToggle();
    });
    // 移动端客户渠道筛选
    $("#filter-mb-px p").click(function(){
        $(this).addClass("hide");
        $(this).removeClass("show");
        $(this).siblings().removeClass("hide");
        $(this).siblings().addClass("show");
        $("#filter-mb-btn2 span").text($(this).text());

        Khlx = khlxNum($("#filter-mb-btn1 span").text().substr(3));
        Khqd = khqdNum($("#filter-mb-btn2 span").text().substr(3));
        Khzt = khztNum($("#filter-mb-btn3 span").text().substr(3));
        Jjjl = jjjlNum($("#filter-mb-btn4 span").text().substr(3));
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
        $("#filter-mb-px").slideToggle();
    });
    // 移动端客户状态筛选
    $("#filter-mb-xx p").click(function(){
        $(this).addClass("hide");
        $(this).removeClass("show");
        $(this).siblings().removeClass("hide");
        $(this).siblings().addClass("show");
        $("#filter-mb-btn3 span").text($(this).text());

        Khlx = khlxNum($("#filter-mb-btn1 span").text().substr(3));
        Khqd = khqdNum($("#filter-mb-btn2 span").text().substr(3));
        Khzt = khztNum($("#filter-mb-btn3 span").text().substr(3));
        Jjjl = jjjlNum($("#filter-mb-btn4 span").text().substr(3));
        if(searchOrNot){
            getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }else{
            searchOrNot = false;
            classifyOrNot = true;
            paginationId = 1;
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
        }
        $("#filter-mb-xx").slideToggle();
    });
    // 移动端客户基金经理筛选
    //$("#filter-mb-xy p").click(function(){
    //    $(this).addClass("hide");
    //    $(this).removeClass("show");
    //    $(this).siblings().removeClass("hide");
    //    $(this).siblings().addClass("show");
    //    $("#filter-mb-btn4 span").text($(this).text());
    //
    //    Khlx = khlxNum($("#filter-mb-btn1 span").text().substr(3));
    //    Khqd = khqdNum($("#filter-mb-btn2 span").text().substr(3));
    //    Khzt = khztNum($("#filter-mb-btn3 span").text().substr(3));
    //    Jjjl = jjjlNum($("#filter-mb-btn4 span").text().substr(3));
    //    if(searchOrNot){
    //        getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    //    }else{
    //        searchOrNot = false;
    //        classifyOrNot = true;
    //        paginationId = 1;
    //        getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    //    }
    //    $("#filter-mb-xy").slideToggle();
    //});

    //getUserList(paginationId,true,true);

    $("#filter-mb-btn1").click(function(){
        $("#filter-mb-cp").slideToggle();
    });
    $("#filter-mb-btn2").click(function(){
        $("#filter-mb-px").slideToggle();
    });
    $("#filter-mb-btn3").click(function(){
        $("#filter-mb-xx").slideToggle();
    });
    $("#filter-mb-btn4").click(function(){
        $("#filter-mb-xy").slideToggle();
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
    Khlx = khlxNum($("#filter-khlx .filter-curr").text());
    Khqd = khqdNum($("#filter-khqd .filter-curr").text());
    Khzt = khztNum($("#filter-khzt .filter-curr").text());
    Jjjl = jjjlNum($("#filter-jjjl .filter-curr").text());
    if(searchOrNot){
        getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    }else{
        searchOrNot = false;
        classifyOrNot = true;
        paginationId = 1;
        getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    }
    $("#filter-mb-xy").slideToggle();
}
function mobileManagerClick(value){
    $('#filter-mb-xy').children().removeClass("hide");
    $('#filter-mb-xy').children().addClass("show");
    $('#filter-mb-xy').children().eq(value).addClass("hide");
    $('#filter-mb-xy').children().eq(value).removeClass("show");

    jjjlName = $('#filter-mb-xy').children().eq(value).text();
    $("#filter-mb-btn4 span").text(jjjlName);
    Khlx = khlxNum($("#filter-mb-btn1 span").text().substr(3));
    Khqd = khqdNum($("#filter-mb-btn2 span").text().substr(3));
    Khzt = khztNum($("#filter-mb-btn3 span").text().substr(3));
    Jjjl = jjjlNum($("#filter-mb-btn4 span").text().substr(3));
    if(searchOrNot){
        getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    }else{
        searchOrNot = false;
        classifyOrNot = true;
        paginationId = 1;
        getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
    }
    $("#filter-mb-xy").slideToggle();
}

function getManager(){
    $.getJSON('/get_manager/',function(ret){
        $('#filter-jjjl').append('<p class="pull-left filter-curr" onclick="managerClick(0)">全部</p>');
        $('#filter-mb-xy').append('<p class="pull-left hide" onclick="mobileManagerClick(0)">经理－全部</p>');
        for(var i=0;i<ret.managerList.length;i++){
            var item = ret.managerList[i];
            $('#filter-jjjl').append('<p class="pull-left" onclick="managerClick('+item.value+')">'+item.name+'</p>');
            $('#filter-mb-xy').append('<p class="pull-left show" onclick="mobileManagerClick('+item.value+')">经理－'+item.name+'</p>');
        }
    });
    getUserList(paginationId,true,true);
    //getProduct(jjjlName,'份额净值',px,lx,searchContent,1,true,true);
}

//type:手机访问模式为Ture，电脑访问模式为False
function getUserList(page,first,type){
    var sendDate = {'page':page}
    $.getJSON('/get_client_list/',sendDate,function(ret) {
        addPagination(ret.pageCount,page);
        if(first && ret.pageCount > 1){
            addLoadMore();
        }
        if(!type){
            $("#listBox").empty();
        }
        clientDetail = ret.clientsList
        for(var i=0; i < clientDetail.length; i++){
            replaceClientContent(clientDetail[i],i);
        }
        $(".loadMore img").attr("src","../static/img/global/more.png");
    });
}

function getSearchClassifyList(content,khlx,khqd,khzt,jjjl,page,first,type){
    var sendData = {'content':content,'Khlx':khlx,'Khqd':khqd,'Khzt':khzt,'Jjjl':jjjl,'page':page}
    $.getJSON('/search_classify_user/',sendData,function(ret) {
        $("#user-count").text('共'+ret.len+'名客户')
        if(first){
            $("#listBox").empty();
            $(".loadMore").empty();
            $(".pagination").empty();
        }
        if(!type){
            $("#listBox").empty();
        }
        if(ret.pageCount > 1){
            addPagination(ret.pageCount,page);
            addLoadMore();
        }
        clientDetail = ret.clientsList
        for(var i=0; i < clientDetail.length; i++){
            replaceClientContent(clientDetail[i],i);
        }
        $(".loadMore img").attr("src","../static/img/global/more.png");
    });
}

function getSearchList(content,page,first,type){
    var sendData = {'content':content,'page':page}
    $.getJSON('/search_user/',sendData,function(ret) {
        $("#user-count").text('共'+ret.len+'名客户')
        if(first){
            $("#listBox").empty();
            $(".loadMore").empty();
            $(".pagination").empty();
        }
        if(!type){
            $("#listBox").empty();
        }
        if(ret.pageCount > 1){
            addPagination(ret.pageCount,page);
            addLoadMore();
        }
        clientDetail = ret.clientsList
        for(var i=0; i < clientDetail.length; i++){
            replaceClientContent(clientDetail[i],i);
        }
        $(".loadMore img").attr("src","../static/img/global/more.png");
    });
}

function getClassifyList(khlx,khqd,khzt,jjjl,page,first,type){
    var sendData = {'Khlx':khlx,'Khqd':khqd,'Khzt':khzt,'Jjjl':jjjl,'page':page}
    $.getJSON('/get_client_classify/',sendData,function(ret) {
        $("#user-count").text('共'+ret.len+'名客户')
        if(first){
            $("#listBox").empty();
            $(".loadMore").empty();
            $(".pagination").empty();
        }
        if(!type){
            $("#listBox").empty();
        }
        if(ret.pageCount > 1){
            addPagination(ret.pageCount,page);
            addLoadMore();
        }
        //$("#listBox").empty();
        //$(".pagination").empty();
        clientDetail = ret.clientsList
        if(clientDetail == ''){
            $("#noRecord").css("display", "block");
            $("#record").css("display", "none");
        }else{
            $("#noRecord").css("display", "none");
            $("#record").css("display", "block");
        }
        for(var i=0; i < clientDetail.length; i++){
            replaceClientContent(clientDetail[i],i);
        }
        $(".loadMore img").attr("src","../static/img/global/more.png");
    });
}

function replaceClientContent(item,i){
    var style = 'listBg2';
    var type = '机构';
    var sex = '未知';
    var customer_mobile = '无';
    var contact_name = '无';
    var contact_mobile = '无';
    var customer_channels = '未知';
    var contact_count = '<span>待办事项：0个</span>';
    var contact_count_mb = '<p class="list-data4 pull-left visible-xs-block">待办事项：<span class="cl-333">0个</span></p>';

    if(i%2==0){
        style = "listBg1";
    }
    if(item.type == '1'){
        type = '个人';
    }
    if(item.sex == '男'){
        sex = '先生';
    }else if(item.sex == '女'){
        sex = '女士';
    }

    var customer_name = item.name;
    var id_no = item.id_no
    //if(customer_name.length > 12){
    //    customer_name = customer_name.substring(0,12)+'...';
    //}
    if(id_no == null || id_no == '_'){
        id_no = '';
    }

    if(item.customer_mobile != null && item.customer_mobile != ''){
        customer_mobile = item.customer_mobile
    }
    if(item.contact_name != null && item.contact_name != ''){
        contact_name = item.contact_name
    }
    if(item.contact_mobile != null && item.contact_mobile != ''){
        contact_mobile = item.contact_mobile
    }
    if(item.customer_channels != null && item.customer_channels != ''){
        customer_channels = item.customer_channels;
        if(customer_channels.length>2){
            customer_channels = customer_channels[0]+"，"+customer_channels[1]+"等";
        }
    }
    if(item.contact_count > 0){
        contact_count = '<span class="brown ">待办事项：'+item.contact_count+'个</span>';
        contact_count_mb = '<p class="list-data4 brown pull-left visible-xs-block">待办事项：<span class="brown cl-333">'+item.contact_count+'个</span></p>';
    }
    $("#listBox").append('<li class="'+style+'"><a class="list-title clearfix" href="../account_home/client='+item.id+'" target="_blank"><p class="pull-left cl-555">'+customer_name+'【'+type+'】'+'【'+sex+'】'+' </p><p class="pull-right cl-555 hidden-xs">'+contact_count+'</p><em class="pull-right visible-xs-block glyphicon glyphicon-menu-right"></em></a><a href="../account_home/client='+item.id+'" target="_blank" class="list-datas clearfix cl-777"><p class="list-data1 pull-left">证件号码<span class="cl-333">'+id_no+'</span></p><p class="list-data2 pull-left">电话<span class="cl-333">'+customer_mobile+'</span></p><p class="list-data3 pull-left">购买渠道<span class="cl-333">'+customer_channels+'</span></p><p class="list-data4 pull-left">联系人／联系方式<span class="cl-333">'+contact_name+'／'+contact_mobile+'</span></p>'+contact_count_mb+'</a></li>');
}

function addLoadMore(){
    $(".loadMore").empty();
    $(".loadMore").append('<img id="loadMoreImage" src="../static/img/global/more.png">');
    $(".loadMore img").click(function(){
        $(".loadMore img").attr("src","../static/img/global/more.gif");
        paginationId++;
        if(searchOrNot){
            getSearchList(searchContent,paginationId,false,true);
        }else if(classifyOrNot){
            getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,false,true);
        }else{
            getUserList(paginationId,false,true);
        }
    });
}

function addPagination(num,page){
    var con = "";
    var tip = true;
    var left = true;
    var right = true;
    var previous = parseInt(page)-2;
    var next = parseInt(page)+2;
    var stylenum = 1;
    for (var i = 1; i <= num; i++) {
        if(page <= 5){
            stylenum = 1;
            if(i<=6){
                con = con + "<li><a>" + i + "</a></li>";
            }else{
                if(tip){
                    con = con + "<li><a>...</a></li>";
                    tip = false;
                }
                if(i > (num-2)){
                    con = con + "<li><a>" + i + "</a></li>";
                }
            }
        }else if((num-page) <= 5){
            stylenum = 2;
            if(i<=2){
                con = con + "<li><a>" + i + "</a></li>";
            }else{
                if(tip){
                    con = con + "<li><a>...</a></li>";
                    tip = false;
                }
                if(i >= (num-6)){
                    con = con + "<li><a>" + i + "</a></li>";
                }
            }
        }else{
            stylenum = 3;
            if(i<=2){
                con = con + "<li><a>" + i + "</a></li>";
            }else if(i>2 && i<previous){
                if(left){
                    con = con + "<li><a>...</a></li>";
                    left = false;
                }
            }else if(i>=previous &&  i<=next){
                con = con + "<li><a>" + i + "</a></li>";
            }else if(i>next && i<(num-2)){
                if(right){
                    con = con + "<li><a>...</a></li>";
                    right = false;
                }
            }else if(i > (num-2)){
                con = con + "<li><a>" + i + "</a></li>";
            }
        }
    };
    $(".pagination").empty();
    $(".pagination").append(
        '<li><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        +con
        +'<li><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
    );
    //alert($(".pagination li"))
    if(stylenum==1){
        $(".pagination li").eq(page).addClass("active");
    }else if(stylenum==3){
        $(".pagination li").eq("6").addClass("active");
    }else if(stylenum==2){
        $(".pagination li").eq(String(10-(num-page))).addClass("active");
    }
    paginationAddEvent(page,num);
}


function khlxNum(text){
    switch (text){
        case '全部':
            return 9;
        case '个人':
            return 1;
        case '机构':
            return 0;
    }
}

function khqdNum(text){
    switch (text){
        case '全部':
            return 0;
        case '直销':
            return 1;
        case '代销':
            return 2;
    }
}

function khztNum(text){
    switch (text){
        case '全部':
            return 0;
        case '正式':
            return 1;
        case '潜在':
            return 2;
    }
}
function jjjlNum(text){
    switch (text){
        case '全部':
            return 0;
        case '邱国鹭':
            return 1;
        case '邓晓峰':
            return 2;
        case '孙庆瑞':
            return 3;
        case '卓利伟':
            return 4;
        case '冯柳':
            return 5;
        case '王世宏':
            return 6;
        case '韩海峰':
            return 7;
        case '薛松':
            return 8;
    }
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

function paginationAddEvent(page,num){

    $(".pagination li").click(function(){
        var ID = $(this).children("a").html();
        if(ID.length>30){
            ID = $(this).children("a").children("span").html();
        }
        if(ID == '«'){
            paginationId = parseInt(page)-1;
            if(paginationId < 1){
                paginationId = 1;
                return;
            }
            if(searchOrNot && classifyOrNot){
                getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
            }else if(searchOrNot){
                getSearchList(searchContent,paginationId,false,false);
            }else if(classifyOrNot){
                getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,false,false);
            }else{
                getUserList(paginationId,false,false);
            }
        }else if(ID == '»'){
            // 下一页
            paginationId = parseInt(page)+1;
            if(paginationId > num){
                return;
            }
            if(searchOrNot && classifyOrNot){
                getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
            }else if(searchOrNot){
                getSearchList(searchContent,paginationId,false,false);
            }else if(classifyOrNot){
                getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,false,false);
            }else{
                getUserList(paginationId,false,false);
            }

        }else{
            // 切换到第几页（12345）
            paginationId = ID;
            if(searchOrNot && classifyOrNot){
                getSearchClassifyList(searchContent,Khlx,Khqd,Khzt,Jjjl,paginationId,true,true);
            }else if(searchOrNot){
                getSearchList(searchContent,paginationId,false,false);
            }else if(classifyOrNot){
                getClassifyList(Khlx,Khqd,Khzt,Jjjl,paginationId,false,false);
            }else{
                getUserList(paginationId,false,false);
            }
        }
        $(".pagination").empty();
    });
}