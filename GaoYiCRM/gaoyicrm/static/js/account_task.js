var client_id="";
$(document).ready(function(){
	client_id = window.location.href.split("=")[1].split("&")[0];
	var client_name = window.location.href.split("=")[2];
	$("#client_name").text(decodeURI(client_name));
	//var select = document.getElementById('user_name');
	$.getJSON('/get_users/',function(ret){
		for(var i=0;i<ret.userList.length;i++){
			var item = ret.userList[i];
			$("#user_name").append(new Option(item.user_name,item.user_id));
		}
		$("#user_name").val(ret.user_id);
	});

	var myDate = new Date();
	var yy = myDate.getYear();
	if(yy<1900) yy = yy+1900;
	var MM = myDate.getMonth()+1;
	if(MM<10) MM = '0' + MM;
	var dd = myDate.getDate();
	if(dd<10) dd = '0' + dd;
	var date = yy+'/'+MM+'/'+dd;

	$("#txtEndDate").calendar({
		controlId: "divDate",                                // 弹出的日期控件ID，默认: $(this).attr("id") + "Calendar"
		speed: 200,                                           // 三种预定速度之一的字符串("slow", "normal", or "fast")或表示动画时长的毫秒数值(如：1000),默认：200
		complement: true,                                     // 是否显示日期或年空白处的前后月的补充,默认：true
		readonly: true,                                       // 目标对象是否设为只读，默认：true
		upperLimit: new Date("2017/12/31"),                  // 日期上限，默认：NaN(不限制)
		lowerLimit: new Date(date),                   		 // 日期下限，默认：NaN(不限制)
		callback: function () {                              // 点击选择日期后的回调函数
			//var dataArray = $("#txtEndDate").val().split('-');
		}
	});
	$("#txtEndDate").val(yy+'-'+MM+'-'+dd);

	$("#quitBtn").click(function () {
		window.location.href = "../account_home/client="+client_id;
	})

	$("#saveBtn").click(function(){
		var date = $("#txtEndDate").val();
		if(date == ""){
			alert('请选择完成日期');
			return;
		}
		var state = $('input[name="state"]:checked').val();
		if(state == undefined){
			alert('请选择接触状态');
			return;
		}
		var details = $('#focuse-message textarea').val();
		if(details == ""){
			alert('请填写接触描述');
			return;
		}

		var time = $('#task-time option:selected').text();
		var user_id = $('#user-name option:selected').val();
		var sendDate = {'client_id':client_id,'user_id':user_id,'date':date, 'time':time, 'state':state, 'details':details}
		$.getJSON('/new_contact/',sendDate,function(ret){
			if(ret.success==0){
				alert('建立成功');
				window.location.href = "../account_home/client="+client_id;
			}else{
				alert('建立失败');
				window.location.href = "../account_home/client="+client_id;
			}
		});
	});

	var swiper = new Swiper('#account-navs-mb', {
		slidesPerView: "auto",
		initialSlide: 0,
		freeMode: true
	});
});
