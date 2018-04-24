var data = new Array();
var fundID = '';
var type = 'rengou';
var typeNum = '1';
var clientID = '';
var failedType = '';
var productList = '';
$(document).ready(function() {

	clientID = window.location.href.split("=")[1].split("&")[0];
	$("#shares").css('display','none');
	$("#user-select").css('display','none');

	var sendData = {'client_id':clientID}
	$.getJSON('/getFundsList/',sendData,function(ret){
		if(ret.fundlist == ''){
			$("#zhuijia").css('display','none');
			$("#shuhui").css('display','none');
			$("#zhuijia-span").css('display','none');
			$("#shuhui-span").css('display','none');
		}else{
			var content = '<option>请选择</option>';
			$("#user-select").append(content);
			for(var i=0;i<ret.fundlist.length;i++){
				var item = ret.fundlist[i];
				var value = item['fundid']+'|'+item['nextopenday']
				var content = '<option value='+value+'>'+item['fundname']+'</option>'
				$("#user-select").append(content);
				$("#user-select").change(function(){
					var FundIDandDate = $("#user-select option:selected").val().split('|');
					var Date = FundIDandDate[1];
					fundID = FundIDandDate[0];
					$("#openday").text('下一开放日：'+Date);
					var sendData = {'clientID':clientID,'applyType':typeNum};
					judgeAcc(sendData);
					$.getJSON('/getAvailableShares/',{'clientID':clientID},function(ret){

					});
				});
			}
		}
	})

	$.getJSON('/getFuzzyProduct/',function(ret){
		productList = ret.productList;
		for(var i=0;i<productList.length;i++){
			var item = productList[i];
			if(item['saleschannel']=="直销" || item['saleschannel']=="员工"){
				data.push({title:item['name'],'nextopenday':item['nextopenday'],'fundid':item['fundid']});
			}
		}
		$("#user-search").bigAutocomplete({
			width:355,
			data:data,
			callback:function(data){
				fundID = data.fundid;
				$("#openday").text('下一开放日：'+data.nextopenday);
				var sendData = {'clientID':clientID,'applyType':typeNum};
				judgeAcc(sendData);
			}
		});
	});

	$("input:radio[name='type']").change(function (){
		type = $("input[name='type']:checked").val();
		if(type == 'rengou'){
			$("#shares").css('display','none');
			$("#user-search").css('display','block');
			$("#user-select").css('display','none');
			$("#trade_tpye").text('认购金额（元）：');
			typeNum = '1';
		}else if(type == 'zhuijia') {
			$("#shares").css('display','none');
			$("#user-search").css('display','none');
			$("#user-select").css('display','block');
			$("#trade_tpye").text('追购金额（元）：');
			typeNum = '2';
		}else{
			$("#shares").css('display','block');
			$("#user-search").css('display','none');
			$("#user-select").css('display','block');
			$("#trade_tpye").text('赎回份额（份）：');
			$("#trade_input").attr('placeholder','填写意向份额');
			typeNum = '3';
		}
	});

	$("#fund_details").click(function(){
		if(fundID==''){
			alert('输入意向产品名称使用')
		}else{
			window.open('../account_details/fund='+fundID);
		}
	});

	$("#quitBtn").click(function(){
		self.location=document.referrer;
	})

	$("#saveBtn").click(function(){
		if(failedType != ''){
			var sendDate = {'clientID':clientID,'failedType':failedType};
			$.getJSON('/sentInfoMail/',sendDate,function(ret){});
		}
		var sendDate = {'clientID':clientID,'fundid':fundID,'apply_type':typeNum,'apply_date':$("#openday").text().split('：')[1],'apply_amount':$("#trade_input").val(),'failedType':failedType}
		$.getJSON('/saveApply/',sendDate,function(ret){
			window.location.href='/account_home/client='+clientID;
		});
	});
	$('.help').popover();
})


function checkNum(inputNum) {
	var num = inputNum;
	num = num.replace(/\D/gi,"");
	$("#upper").text(DX(num));
}

function judgeAcc(sendData){
	$.getJSON('/judgeAcc/',sendData,function(ret){
		failedType = ret.failedType;
		var failedTypeList = failedType.split('|');
		var failedZero = false;
		var failedOne = false;
		var failedTwo = false;
		var failedThree = false;
		for(var i=0; i<failedTypeList.length; i++){
			if(failedTypeList[i] == '0'){
				$("#client_type").children().eq(1).attr('src','../static/img/crm_intention/icons_s_r_72.png');
				$("#client_type").children().eq(2).attr('class','red');
				$("#modal-body0").html('请完整填写客户姓名、联系电话、联系邮箱、证件类型和证件号码。');
				failedZero = true;
			}
			if(failedTypeList[i] == '1'){
				$("#client_type").children().eq(3).attr('src','../static/img/crm_intention/icons_s_r_72.png');
				$("#client_type").children().eq(4).attr('class','red');
				$("#modal-body1").html('尚未上传客户的身份证明材料。');
				failedOne = true;
			}
			if(failedTypeList[i] == '2'){
				$("#client_type").children().eq(5).attr('src','../static/img/crm_intention/icons_s_r_72.png');
				$("#client_type").children().eq(6).attr('class','red');
				if(ret.threeYear){
					$("#modal-body2").html('距离上一份填写风险问卷已经超过三年');
				}else{
					$("#modal-body2").html('客户尚未填写的风险问卷。');
				}
				failedTwo = true;
			}
			if(failedTypeList[i] == '3'){
				$("#client_type").children().eq(7).attr('src','../static/img/crm_intention/icons_s_r_72.png');
				$("#client_type").children().eq(8).attr('class','red');
				if(ret.threeYear){
					$("#modal-body3").html('距离上一次上传资产证明已经超过三月且客户在高毅资产的资产金额低于300万');
				}else{
					$("#modal-body3").html('客户尚未上传的资产证明。');
				}
				failedThree = true;
			}
		}
		if(!failedZero){
			$("#client_type").children().eq(1).attr('src','../static/img/crm_intention/icons_s_g_72.png')
			$("#client_type").children().eq(2).attr('class','green')
			$("#modal-body0").html('信息填写完整');
		}
		if(!failedOne){
			$("#client_type").children().eq(3).attr('src','../static/img/crm_intention/icons_s_g_72.png')
			$("#client_type").children().eq(4).attr('class','green')
			$("#modal-body1").html('身份材料完整');
		}
		if(!failedTwo){
			$("#client_type").children().eq(5).attr('src','../static/img/crm_intention/icons_s_g_72.png')
			$("#client_type").children().eq(6).attr('class','green')
			$("#modal-body2").html('风险问卷完整');
		}
		if(!failedThree){
			$("#client_type").children().eq(7).attr('src','../static/img/crm_intention/icons_s_g_72.png')
			$("#client_type").children().eq(8).attr('class','green')
			$("#modal-body2").html('资产证明完整');
		}
	});
}

function DX(n) {
	if (!/^(0|[1-9]\d*)(\.\d+)?$/.test(n))
		return "";
	var unit = "千百十亿千百十万千百十元角分", str = "";
	n += "00";
	var p = n.indexOf('.');
	if (p >= 0)
		n = n.substring(0, p) + n.substr(p+1, 2);
	unit = unit.substr(unit.length - n.length);
	for (var i=0; i < n.length; i++)
		str += '零一二三四五六七八九'.charAt(n.charAt(i)) + unit.charAt(i);
	return str.replace(/零(千|百|十|角)/g, "零").replace(/(零)+/g, "零").replace(/零(万|亿|元)/g, "$1").replace(/(亿)万|壹(十)/g, "$1$2").replace(/^元零?|零分/g, "").replace(/元$/g, "");
}