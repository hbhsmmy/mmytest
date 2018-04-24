var paginationId = 1;
var managerID = 1;
var managerNews = ''
$(document).ready(function(){

    switch (window.location.href.split("/")[3].split("_")[2]){
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
    getArticles(1,true,true);
    var swiper = new Swiper('.mb-top-navs', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });

});

function getArticles(page,first,type){
    $.getJSON('/manageMedia/',{'manager':managerID,'type':'all','page':page},function(ret){
        if(type){
            $(".news-lists").empty();
        }
        if(page=1){
	    for(var i=0;i<ret.recommendArticles.length;i++){
           	 var item = ret.recommendArticles[i];
           	 replaceContent(item);
	    }
        }
        for(var i=0;i<ret.articles.length;i++){
            var item = ret.articles[i];
            replaceContent(item);
        }
        if(first && ret.totalcount > 1){
            addPagination(ret.totalcount);
            addLoadMore();
        }
        if(page == ret.totalcount){
            $(".loadMore").remove();
        }else{
            $(".loadMore").children("img").attr("src","../static/img/global/more.png");
        }
    });

}

function replaceContent(item){
    $(".news-lists").append('<li class="border-b"><a href="../'+managerNews+'/'+item.id+'" class="clearfix"><p class="pull-left textEllipsis cl-333">'+item.title+'</p><em class="cl-999 pull-right glyphicon glyphicon-menu-right"></em><span class="pull-right cl-999 hidden-xs">'+item.time+'</span></a></li>');
}

function addLoadMore(){
    $(".loadMore").append('<img src="../static/img/global/more.png">');
    $(".loadMore").click(function () {
        $(".loadMore").children("img").attr("src","../static/img/global/more.gif");
        paginationId++;
        getArticles(paginationId,false,false);
    })
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
            getArticles(paginationId,false,true);
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
            getArticles(paginationId,false,true);
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
            getArticles(paginationId,false,true);
            $(".pagination li").eq(ID).addClass("active");
            for (var i = 1; i < $(".pagination li").length - 1; i++) {
                if(ID != i){
                    $(".pagination li").eq(i).removeClass("active");
                }
            };
        }
    });
}
