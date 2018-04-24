var managerNews = ''
$(document).ready(function(){

    var managerID = 1;
    switch (window.location.href.split("/")[3].split("_")[1]){
        case "qgl":
            managerID = 1;
            managerNews = 'investTeam_news_qgl_info'
            break;
        case "dxf":
            managerID = 2;
            managerNews = 'investTeam_news_dxf_info'
            break;
        case "sqr":
            managerID = 3;
            managerNews = 'investTeam_news_sqr_info'
            break;
        case "zlw":
            managerID = 4;
            managerNews = 'investTeam_news_zlw_info'
            break;
        case "fl":
            managerID = 5;
            managerNews = 'investTeam_news_fl_info'
            break;
        case "wsh":
            managerID = 6;
            managerNews = 'investTeam_news_wsh_info'
            break;
    }


    $.getJSON('/manageMedia/',{'manager':managerID,'type':'part'},function(ret){
        if(ret.recommendArticles.length != 0){
            var recommendArticles = ret.recommendArticles[0];
            $("#article").append('<a href="../'+managerNews+'/'+recommendArticles.id+'" id="article-title" class="cl-333 font14 clearfix"><p class="pull-left">'+recommendArticles.title+'</p><span class="pull-right cl-666 siteText">'+recommendArticles.time+'</span></a>');
            $("#article").append('<div id="article-txt" class="siteText cl-777">'+recommendArticles.brief_comment+'</div>');
            $("#article").append('<div id="article-more" class="clearfix"><a href="../'+managerNews+'/'+recommendArticles.id+'" class="pull-right">查看全部</a></div>');
        }
        for(var i=0;i<ret.articles.length;i++){
            var item = ret.articles[i];
            $("#news ul").append('<li class="border-b"><a href="../'+managerNews+'/'+item.id+'" class="clearfix"><p class="pull-left textEllipsis cl-333">'+item.title+'</p><em class="cl-999 pull-right glyphicon glyphicon-menu-right"></em><span class="pull-right cl-999 hidden-xs">'+item.time+'</span></a></li>');
        }
    });


    //$("#info1-text a").click(function(){
        //alert('数据整合中，敬请期待！');
        //url = ""
        //switch ($("#info1-text p").text()){
        //    case "邱国鹭":
        //        url="../account_product/manager=managerOne";
        //        break;
        //    case "邓晓峰":
        //        url="../account_product/manager=managerTwo";
        //        break;
        //    case "孙庆瑞":
        //        url="../account_product/manager=managerThree";
        //        break;
        //    case "卓利伟":
        //        url="../account_product/manager=managerFour";
        //        break;
        //    case "冯柳":
        //        url="../account_product/manager=managerFive";
        //        break;
        //    case "王世宏":
        //        url="../account_product/manager=managerSix";
        //        break;
        //}
        //
        //$.getJSON('/loginOrNot/',function(ret){
        //    if(ret.loginOrNot == '1'){
        //        window.location.href = url;
        //    }else{
        //        alert('请登陆后查看！');
        //        window.location.href = ret.url;
        //    }
        //})
    //});
    if(managerID==1||managerID==2||managerID==3){
        var swiper = new Swiper('#account-navs-mb', {
                slidesPerView: "auto",
                initialSlide: 0,
                freeMode: true
            });
    }else{
        var swiper = new Swiper('#account-navs-mb', {
                slidesPerView: "auto",
                initialSlide: managerID-1,
                freeMode: true
            });
    }
});




