var clientID = ''
$(document).ready(function() {

	$("#header-1-phone").css('display','None');

	clientID = window.location.href.split("=")[1];
	var sendData = {'clientID':clientID}
	$.getJSON('/infoAboutAuestionnaire/', sendData,function (ret) {
		$("#userName1 em").text(ret.realname);
	});

	$("#queren").click(function () {

		var subQaArray = '';
		var qaArray = '';
		var subWenJuanInfo = $('#subWenJuanInfo').children();
		for(var i=0; i<subWenJuanInfo.length; i++){
			var itemList = subWenJuanInfo.eq(i).children();
			var item2List = itemList.eq(1).children();
			for(var j=0; j<item2List.length; j++){
				var item2 = item2List.eq(j);
				if(item2.children().eq(0).prop("checked")==true){
					subQaArray = subQaArray + item2.text() + '（√）||';
				}else{
					subQaArray = subQaArray + item2.text() + '||';
				}
			}
		}

		var wenJuanInfo = $('#wenjuanInfo').children();
		for(var i=0; i<wenJuanInfo.length; i++){
			var itemList = wenJuanInfo.eq(i).children();
			var item1 = itemList.eq(0).html();
			//qaArray.push(item1)
			qaArray = qaArray + item1 + '||';
			var item2List = itemList.eq(1).children();
			for(var j=0; j<item2List.length; j++){
				var item2 = item2List.eq(j);
				//qaArray.push(item2)
				//alert(item2.children().eq(0).prop("checked"));
				if(item2.children().eq(0).prop("checked")==true){
					qaArray = qaArray + item2.text() + '（√）||';
				}else{
					qaArray = qaArray + item2.text() + '||';
				}
			}
		};
		var testNum = '';
		var allNum = 0;
		//if ($("#userVocation").children("input").val() == "") {
		//	alert("请输入您的职业并完成！《风险属性评估问卷》")
		//	return;
		//}
		for (var i = 0; i < 12; i++) {
			allNum = allNum + parseInt(getRadio("test" + (i + 1)));
			if (getRadio("test" + (i + 1)) == "") {
				alert("您在第" + (i + 1) + "条问卷测试题中尚未选择，请完成！");
				return;
			}
			if (i == 11) {
				testNum += parseInt(getRadio("test" + (i + 1)));
			} else {
				testNum += parseInt(getRadio("test" + (i + 1))) + '.';
			}
		}
		//if(allNum < 33){
		//	alert('您的分数低于28分，属于保守型用户，请放弃购买或重新进行测评！');
		//	return;
		//}

		var sendData = {
			//'education': $("#userDegree select").children('option:selected').text(),
			//'occupation': $("#userVocation").children("input").val(),
			'clientID':clientID,
			'clientArray':qaArray,
			'subQaArray':subQaArray,
			'point': testNum,
		}
		$.post('/ResultAboutAuestionnaire/', sendData, function(ret){
			window.location.href = ret.url;
		});
	});
});

function getRadio(name){
	var value="";
	var radio=document.getElementsByName(name);
	for(var i=0;i<radio.length;i++){
		if(radio[i].checked==true){
			value=radio[i].value;
			break;
		}
	}
	return value;
}