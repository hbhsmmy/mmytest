var clientID = ''
$(document).ready(function() {

	$("#header-1-phone").css('display','None');

	clientID = window.location.href.split("=")[1];
	var sendData = {'clientID':clientID}
	$.getJSON('/infoAboutAuestionnaire/', sendData,function (ret) {
		$("#userName1 em").text(ret.realname);
	});

	$("#queren").click(function () {

		var qaArray = '';

		var wenJuanInfo = $('#wenjuanInfo').children();
		for(var i=0; i<wenJuanInfo.length; i++){
			var itemList = wenJuanInfo.eq(i).children();
			var item1 = itemList.eq(0).html();
			//qaArray.push(item1)
			qaArray = qaArray + item1 + '||';
			var item2List = itemList.eq(1).children();
			for(var j=0; j<item2List.length; j++){
				var item2 = item2List.eq(j);
				if(item2.children().eq(0).prop("checked")==true){
					qaArray = qaArray + item2.text() + '（√）||';
				}else{
					qaArray = qaArray + item2.text() + '||';
				}
			}
		}
		alert(qaArray);

		var testNum = '';
		var allNum = 0;
		for (var i = 0; i <wenJuanInfo.length; i++) {
			allNum = allNum + parseInt(getRadio("test" + (i + 1)));
			if (getRadio("test" + (i + 1)) == "") {
				alert("您在第" + (i + 1) + "条问卷测试题中尚未选择，请完成！");
				return;
			}
			if (i == 18) {
				testNum += parseInt(getRadio("test" + (i + 1)));
			} else {
				testNum += parseInt(getRadio("test" + (i + 1))) + '.';
			}
		}
		var sendData = {
			'clientID':clientID,
			'clientArray':qaArray,
			'point': testNum,
		}
		$.post('/ResultAboutQuestionnaire/', sendData, function(ret){
			window.location.href=ret.url;
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