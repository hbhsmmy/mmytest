var contactUn  = '';
var contactFin  = '';
var status = 2;
var type = 0;
var clicking = false;
$(document).ready(function(){

    $("#info2_content1").css("display", "block");
    $("#info2_content2").css("display", "none");
    $(".info-title-more p").mouseover(function(){
        var ID = $(this).index();
        $(this).addClass("info-title-more-curr");
        $(this).siblings().removeClass("info-title-more-curr");
        if(ID == 0){
            $("#info2_content1").css("display", "block");
            $("#info2_content2").css("display", "none");
        }
        else if(ID == 1){
            $("#info2_content1").css("display", "none");
            $("#info2_content2").css("display", "block");
        }
    });
    var events = new Array();
    var myDate = new Date();
    var myMonth = myDate.getMonth()+1;
    if(myMonth<10){
        myMonth = '0'+String(myMonth)
    }else{
        myMonth = String(myMonth)
    }
    var fullDate = String(myDate.getFullYear()) + '-' + myMonth + '-' + String(myDate.getDate());

    var sendData = {'status':status}
    $.getJSON('/get_contact/',sendData,function(ret){
        contactUn = ret.contactsList
        for(var i=0;i<contactUn.length;i++){
            var item = contactUn[i]
            events.push({title:item.contact_detail,start:item.contact_date.replace(' ','T')+':00',url:'../task_detail/contact_id='+item.contact_id})
            replaceContent(item,i);
        };
        if(contactUn.length==0){
            $('#noRecord').css("display", "block");
            $('#noRecord_mb').css("display", "block");
            $("#contact_bg").css("display", "none");
        }else{
            $('#noRecord').css("display", "none");
            $('#noRecord_mb').css("display", "none");
            $("#contact_bg").css("display", "block");
            $("#contact_tip").text(contactUn.length);
        }
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
            monthNamesShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
            dayNames: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
            dayNamesShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
            firstDay: 1,
            buttonText: {
                today: '今天',
                month: '月',
                week: '周',
                day: '日',
                prev: '上一月',
                next: '下一月'
            },
            Date: fullDate,
            editable: false,
            eventLimit: true,
            events:events,
            eventClick: function(calEvent, jsEvent, view) {

            }
        });
    });

    $("#filter1 p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        if($(this).text() == "全部"){
            type = 0;
        }else if($(this).text() == "合同收取"){
            type = 3;
        }else if($(this).text() == "静默回访"){
            type = 2;
        }else if($(this).text() == "自建接触"){
            type = 1;
        }else if($(this).text() == "适配性确认"){
            type = 10;
        }
        if(status == 2){
            if(contactUn == ''){
                getContent(status,type);
            }else{
                getContentHere(contactUn,status,type)
            }
        }else{
            if(contactFin == ''){
                getContent(status,type);
            }else{
                getContentHere(contactFin,status,type)
            }
        }
        $("#filter-mb-cp").slideToggle();
    });

    $("#filter2 p").click(function(){
        $(this).addClass("filter-curr");
        $(this).siblings().removeClass("filter-curr");
        if($(this).text() == "未完成"){
            status = 2;
            if(contactUn == ''){
                getContent(status,type);
            }else{
                getContentHere(contactUn,status,type)
            }
        }else{
            status = 1;
            if(contactFin == ''){
                getContent(status,type);
            }else{
                getContentHere(contactFin,status,type)
            }
        }
        $("#filter-mb-cp").slideToggle();
    });

    $("#status-mb p").click(function(){

        $(this).addClass("status-mb-type-navCurr");
        $(this).siblings().removeClass("status-mb-type-navCurr");

        if($(this).text() == "未完成"){
            status = 2;
        }else{
            status = 1;
        }
        getContent(status);
        $("#filter-mb-cp").slideToggle();
    });

    var swiper = new Swiper('#account-navs-mb', {
        slidesPerView: "auto",
        initialSlide: 0,
        freeMode: true
    });
});

function getContentHere(contact,status,type){
    $("#listBox").empty();
    $("#listBox_mb").empty();
    if(type == 0){
        for(var i=0;i<contact.length;i++){
            var item = contact[i]
            replaceContent(item,i);
        };
    }else{
        for(var i=0;i<contact.length;i++){
            var item = contact[i]
            if(item.contact_type == type){
                replaceContent(item,i);
            }
        };
    }
    if(contact.length==0){
        $('#noRecord').css("display", "block");
        $('#noRecord_mb').css("display", "block");
        $("#contact_bg").css("display", "none");
        if(status == 1){
            $('#noRecord_title').text('暂时没有记录')
            $('#noRecord_title_mb').text('暂时没有记录')
        }else{
            $('#noRecord_title').text('暂时没有待办，去放松一下吧')
            $('#noRecord_title_mb').text('暂时没有待办，去放松一下吧')
        }
    }else{
        $('#noRecord').css("display", "none");
        $('#noRecord_mb').css("display", "none");
        $("#contact_bg").css("display", "block");
        $("#contact_tip").text(contact.length);
    }
}

function getContent(status,type){
    var sendData = {'status':status}
    $("#listBox").empty();
    $("#listBox_mb").empty();
    $.getJSON('/get_contact/',sendData,function(ret){
        contactFin = ret.contactsList;
        if(type == 0){
            for(var i=0;i<contactFin.length;i++){
                var item = contactFin[i]
                replaceContent(item,i);
            };
        }else{
            for(var i=0;i<contactFin.length;i++){
                var item = contactFin[i];
                if(item.contact_type == type){
                    replaceContent(item,i);
                }
            };
        }
        if(contactFin.length==0){
            $('#noRecord').css("display", "block");
            $('#noRecord_mb').css("display", "block");
            $("#contact_bg").css("display", "none");
            if(status == 1){
                $('#noRecord_title').text('暂时没有记录')
                $('#noRecord_title_mb').text('暂时没有记录')
            }else{
                $('#noRecord_title').text('暂时没有待办，去放松一下吧')
                $('#noRecord_title_mb').text('暂时没有待办，去放松一下吧')
            }
        }else{
            $('#noRecord').css("display", "none");
            $('#noRecord_mb').css("display", "none");
            $("#contact_bg").css("display", "block");
            $("#contact_tip").text(contactFin.length);
        }
    });
}

function replaceContent(item,i){
    //alert(item.contact_record)
    var btn = 'btn'+i;
    var liID = "li"+i;
    var contactDetail = item.contact_detail
    var contact_record = '尚未完成';
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
    if(item.status == 2){
        var type_des = '<p class="l-i-1 pull-left">计划完成时间<span class="cl-333">'+item.contact_date+'</span></p>';
        if(item.contact_type == 3){
            var style = '<a id="'+btn+'" class="a_ready" onclick="openApply('+i+')">完成</a>';
        }else{
            var style = '<a id="'+btn+'" class="a_ready" onclick="revert('+i+','+item.contact_id +','+item.client_id+')">完成</a>';
        }
    }else if(item.status == 1){
        var type_des = '<p class="l-i-1 pull-left">完成时间<span class="cl-333">'+item.record_date+'</span></p>';
        var style = '<a class="a_finish" style="cursor:default">'+item.updated_by+'完成回复</a>';
    }
    if(item.status==1){
        contact_record = item.contact_record
        if(contact_record == '' || contact_record == null){
            contact_record = '没有完成'
        }
    }
    var mobile = item.customer_mobile;
    if(mobile=="" || mobile==null){
        mobile = '无';
    }
    var email = '<img id="email" onclick="email_info('+ i + ',' + item.status +')" src="../static/img/account/more.png"></img>';

    $("#listBox").append('<li id="'+liID+'" class="listBg1"><div class="list-left pull-left" onclick="gotoDetail('+item.contact_id+','+item.status+')"><div class="list-infoContent cl-777 clearfix">'+type_des+'<p class="l-i-2 pull-left">待办类型<span class="cl-333">'+type+'</span></p><p class="l-i-3 pull-left">客户姓名<span class="cl-333">'+item.customer_name+'</span></p><p class="l-i-5 pull-left">联系方式<span class="cl-333">'+mobile+email+'</span></p></div><div class="list-left-info"><div class="l-i-4 list-info pull-left"><p>具体内容：'+contactDetail+'</p><p>完成情况：'+contact_record+'</p></div></div></div><div class="list-right pull-left hidden-xs"><div class="list-right-info">'+style+'</div></div>');
    $("#listBox_mb").append('<li id="'+liID+'" class="listBg1"><div class="list-left pull-left" onclick="gotoDetail('+item.contact_id+','+item.status+')"><div class="list-infoContent cl-777 clearfix">'+type_des+'<p class="l-i-2 pull-left">待办类型<span class="cl-333">'+type+'</span></p><p class="l-i-3 pull-left">客户姓名<span class="cl-333">'+item.customer_name+'</span></p><p class="l-i-5 pull-left">联系方式<span class="cl-333">'+mobile+email+'</span></p></div><div class="list-left-info"><div class="l-i-4 list-info pull-left"><p>具体内容：'+contactDetail+'</p><p>完成情况：'+contact_record+'</p></div></div></div><div class="list-right pull-left hidden-xs"><div class="list-right-info">'+style+'</div></div>');
}

function gotoDetail(contact_id,status){
    if(status != 1){
        if(clicking){
            clicking = false;
        }else{
            window.location.href = '../task_detail/contact_id='+contact_id;
        }
    }
}

function email_info(i,status){
    var contact = '';
    if(status == 2){
        contact = contactUn
    }else{
        contact = contactFin
    }
    if(contact[i].customer_email == null){
        alert('客户的Email为空');
    }else{
        prompt('客户的Email为：',contact[i].customer_email);
    }
    clicking = true;
    return;
}

function openApply(i){
    var contact = contactUn;
    var applyID = contact[i].note.split('.')[1];
    window.open('/account_apply/applyID='+applyID);
}

function getDoc(i){
    //alert(contactUn);
    var contact = contactUn;
    //alert(contact[i].note);
    var sendData = {'fundAndApply':contact[i].note}
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
    return;
}

function revert(num,contact_id,client_id){
    var btn = 'btn'+num;
    var li = 'li'+num;
    var quitID = 'quit'+num;
    var saveID = 'save'+num;
    var feedbackID = 'feedback-div'+num;
    var finish_btn = document.getElementById(btn);
    finish_btn.className = 'a_finish';
    finish_btn.innerHTML = '正在录入记录';

    $("#"+li).append('<div id="'+feedbackID+'" class="feedback input-group"><textarea id="feedback-textarea" class="form-control" placeholder="任务完成记录（可以为空）"></textarea><a id="'+quitID+'" class="quit pull-left">取消</a> <a id="'+saveID+'" class="quit pull-right">完成</a></div>');
    $("#"+quitID).click(function(){
        $("#"+feedbackID).remove();
        finish_btn.className = 'a_ready';
        finish_btn.innerHTML = '完成';
    });
    $("#"+saveID).click(function(){
        var sendData = {'contact_id':contact_id,'client_id':client_id,'contact_record':$('#feedback-textarea').val()};
        $.getJSON('/save_contact_record/',sendData,function(ret) {
            if(ret.success == 200){
                window.location.href=window.location.href;
            }
        });
    });
}
