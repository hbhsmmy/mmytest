var paginationId = 1;
$(document).ready(function(){
    getArticles(1,true,true);
    var swiper = new Swiper('.mb-top-navs', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });
});

function getArticles(page,first,type){
    var sendDate = {'type':2,'page':page}
    $.getJSON('/get_articles/',sendDate,function(ret) {
        if(type){
            $(".news-lists").empty();
        }
        for (var i = 0; i < ret.len; i++) {
            var item = ret.articlesTitle[i]
            replaceContent(item)
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
    })
}

function addLoadMore(){
    $(".loadMore").append('<img src="../static/img/global/more.png">');
    $(".loadMore").click(function () {
        $(".loadMore").children("img").attr("src","../static/img/global/more.gif");
        paginationId++;
        getArticles(paginationId,false,false);
    });
}

function replaceContent(item){
    $(".news-lists").append('<li class="border-b"><a href="../trends_research_info/'+item.id+'" class="clearfix"><p class="pull-left textEllipsis cl-555">'+item.title+'</p><em class="cl-999 pull-right glyphicon glyphicon-menu-right"></em><span class="pull-right cl-666 hidden-xs">'+item.time+'</span></a></li>');
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
