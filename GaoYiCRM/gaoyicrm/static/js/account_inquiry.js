var paginationId = 1;
var status = 2;
var messageList = '';
var clicking = false;
$(document).ready(function(){

    getMessage(paginationId,status,true,true);

    $("#filter p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        if($(this).text() == "未回复"){
            status = 2;
        }else{
            status = 1;
        }
        paginationId = 1;
        getMessage(paginationId,status,false,true);
        $("#filter-mb-cp").slideToggle();
    });

    $("#status-mb p").click(function(){

        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");

        if($(this).text() == "未回复"){
            status = 2;
        }else{
            status = 1;
        }
        paginationId = 1;
        getMessage(paginationId,status,false,true);
        $("#filter-mb-cp").slideToggle();
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 5,
        freeMode: true
    });

});

function getMessage(page,status,type,first){
    var sendData = {'status':status,'page':page}
    $.getJSON('/get_message/',sendData,function(ret) {
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
        messageList = ret.messageList;

        for(var i= 0;i<messageList.length;i++){
            var liID = "li"+i;
            var divID = "div"+i;
            var btn = 'btn'+i;
            var item = messageList[i]

            var date = item.contact_date;
            if(date == '工作日（周一至周五）'){
                date = date.substring(0,3);
            }
            var time = item.contact_time;
            if(time == '全天（8:00至20:00）'){
                time = time.substring(3,13);
            }
            if(time == '全天(8:00 - 18:00)'){
                time = time.substring(3,15);
            }
            if(time == '全天(8:00 - 20:00)'){
                time = time.substring(3,15);
            }
            if(time == '全天（8:15 - 18:45）'){
                time = time.substring(3,15);
            }
            var email = item.email;
            if(email == "" || email =="_"){
                email = '-';
            }
            if(item.status == 2){
                var style = '<a id="'+btn+'" class="a_ready" onclick="revert('+i+','+item.messageID +')">完成</a>';
            }else if(item.status == 1){
                var myTime = new Date(item.revert_date*1000);
                var myMonth = myTime.getMonth()+1;
                if(myMonth<10){
                    myMonth = '0' + myMonth;
                }
                var myDate = myTime.getDate();
                if(myDate<10){
                    myDate = '0' + myDate;
                }
                var myHour = myTime.getHours();
                if(myHour<10){
                    myHour = '0' + myHour;
                }
                var myMin = myTime.getMinutes();
                if(myMin<10){
                    myMin = '0' + myMin;
                 }
                var totalDate = myTime.getFullYear()+myMonth+myDate+' '+myHour+':'+myMin;
                var style = '<a class="a_finish" style="cursor:default">'+totalDate+'</a><br/><a class="a_finish" style="cursor:default">'+item.updated_by+'完成回复</a>';
            }
            var message = item.message;
            if(message == null){
                message = '';
            }
            var revert_record = item.revert_record;
            if(revert_record == null){
                revert_record = '尚未完成';
            }
            if(revert_record == ""){
                revert_record = '没有记录';
            }
            var exist = '';
            if(item.exist == '1'){
                exist = '<img id="repeat" onclick="client_info('+i+')" src="../static/img/account/repeat.png"/>';
            }
            var messageTime = item.message_time.substr(0,10)+' '+item.message_time.substr(11,5)
            var email = '<img id="email" onclick="email_info('+i+')" src="../static/img/account/more.png"></img>';
            $("#listBox").append('<li id="'+liID+'" class="listBg1" ><div class="list-left pull-left" onclick="gotoDetail('+item.messageID+','+item.status+')"><div class="list-infoContent clearfix"><p class="l-i-1 list-info pull-left">留言时间<span>'+messageTime+'</span></p><p class="l-i-2 list-info pull-left">客户姓名</span><span>'+item.username+exist+'</span></p><p class="l-i-3 list-info pull-left">期望回复时间<span>'+date+' '+time+'</span></p><p class="l-i-3 list-info pull-left">联系方式<span>'+item.mobile+email+'</span></p></div><div class="list-left-info"><p class="l-i-4 list-info pull-left">内容：'+item.message+'</p><p class="l-i-4 list-info pull-left">记录：'+revert_record+'</p></div></div><div class="list-right pull-left hidden-xs"><div id="'+divID+'" class="list-right-info">'+style+'</div></div></li>');
        }
        if(ret.pageCount > 1){
            addPagination(ret.pageCount,page);
        }
        $(".loadMore img").attr("src","../static/img/global/more.png");
    });
}

function gotoDetail(contact_id,status){
    if(status != 1){
        if(clicking){
            clicking = false;
        }else{
            window.location.href = '../message_detail/message_id='+contact_id
        }
    }
}

function addLoadMore(){
    $(".loadMore").empty();
    $(".loadMore").append('<img id="loadMoreImage" src="../static/img/global/more.png">');
    $(".loadMore img").click(function(){
        $(".loadMore img").attr("src","../static/img/global/more.gif");
        paginationId++;
        getMessage(paginationId,status,true,false);
    });
}


function revert(num,messageID){
    var btn = 'btn'+num;
    var li = 'li'+num;
    var quitID = 'quit'+num;
    var saveID = 'save'+num;
    var feedbackID = 'feedback-div'+num;
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
        var sendData = {'message_id':messageID,'revert_record':$('#feedback-textarea').val()};
        $.getJSON('/save_revert_record/',sendData,function(ret) {
            if(ret.success == 200){
                window.location.href=window.location.href;
            }
        });
    });
}

function email_info(i){
    if(messageList[i].email == null){
        alert('客户的Email为空');
    }else{
        prompt('客户的Email为：',messageList[i].email);
    }
    clicking = true;
    return;
}

function client_info(i){
    for(var j=0;j<messageList[i].existList.length;j++){
        var item = messageList[i].existList[j]
        window.open('../account_home/client='+item.client_id);
    }
    clicking = true;
    return;
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
    if(stylenum==1){
        $(".pagination li").eq(page).addClass("active");
    }else if(stylenum==3){
        $(".pagination li").eq("6").addClass("active");
    }else if(stylenum==2){
        $(".pagination li").eq(String(10-(num-page))).addClass("active");
    }
    paginationAddEvent(page,num);
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
            //getMessage(paginationId,false)
            getMessage(paginationId,status,false,false);
        }else if(ID == '»'){
            // 下一页
            paginationId = parseInt(page)+1;
            if(paginationId > num){
                return;
            }
            //getMessage(paginationId,false)
            getMessage(paginationId,status,false,false);

        }else{
            // 切换到第几页（12345）
            paginationId = ID;
            getMessage(paginationId,status,false,false);
        }
    });
}


