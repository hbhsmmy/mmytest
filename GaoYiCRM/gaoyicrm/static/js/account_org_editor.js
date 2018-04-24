var clientID = '';
var blurOrNot = true;
var imgID = '';
$(document).ready(function(){

	clientID = window.location.href.split("=")[1];
	if(clientID != undefined){
		$("#changeBtn").css("display","none");
	}else{
		$("#relativeInfo").css("display","none");
		$("#relativeDiv").css("display","none");
	}
	$("#shouquanBtn").css("display","none");
	$("#user-name-input").blur(function(){
		if(blurOrNot){
			var sendData = {'customer_name':$("#user-name-input").val()}
			$.getJSON('/check_client/',sendData,function(ret){
				if(ret.len != 0){
					var result = confirm("检索到同名用户，是否需要查看？");
					if(result){
						for(var i=0;i<ret.clientsList.length;i++){
							var item = ret.clientsList[i];
							window.open('../account_home/client='+item.client_id);
						}
					}
				}
			});
		}
	});

	$("#changeBtn").click(function(){
		window.location.href = "../account_editor";
	})

	$("#user-province select").empty();
	for(i = 0; i < province_arr1.length; i++){
		$("#user-province select").append("<option>" + province_arr1[i] + "</option>");
	}

	$("#user-province select").on("change", cityChange);
	if(clientID != undefined){
		fillInfo(clientID);
	}

	$('input[name="represent"]').click(function(){
		switch ($('input[name="represent"]:checked').attr("id")){
			case 'faren':
				$('#user-legal-name-span').text('法人姓名');
				$("#shouquanBtn").css("display","none");
				break;
			case 'shouquan':
				$('#user-legal-name-span').text('授权人姓名');
				$("#shouquanBtn").css("display","block");
				break;
		}
	});

	$("#quitBtn").click(function(){
		window.opener=null;
		window.open('','_self');
		window.close();
	});


	$("#saveBtn").click(function() {
		$.getJSON('/edit_client/',getSendDate(),function(ret){
			if(ret.message.url == '0'){
				alert('新增客户信息成功');
				window.location.href = '../account_records';
			}else if(ret.message.url == '1'){
				alert('更新客户信息成功');
				window.location.href = '../account_home/client='+clientID;
			}else{
				alert('更新失败，请稍后尝试');
			}
		});
	});

	$("#saveAndNewBtn").click(function(){
		$.getJSON('/edit_client/',getSendDate(),function(ret){
			if(ret.message.url == '0'){
				alert('新增客户信息成功');
				window.location.href = '../account_task/client_id='+ret.message.client_id+'&client_name='+ret.message.client_name;
			}else if(ret.message.url == '1'){
				alert('更新客户信息成功');
				window.location.href = '../account_task/client_id='+ret.message.client_id+'&client_name='+ret.message.client_name;
			}else{
				alert('更新失败，请稍后尝试');
			}
		});
	});

	var swiper = new Swiper('#account-navs-mb', {
		slidesPerView: "auto",
		initialSlide: 0,
		freeMode: true
	});
});

function fillInfo(client_id){
	var sendData = {"client_id":client_id};
	$.getJSON('/get_user_edit/',sendData,function(ret){

		$("#user-org-name input").val(ret.client_name);
		$("#user-org-holder input").val(ret.client_org_holder);
		$("#user-org-range input").val(ret.client_org_range);

		if(ret.card_type != ""){
			$("#user-cardType").val(ret.card_type);
			$("#user-cardNo input").val(ret.card_no);
		}
		//if(ret.mark == '1'){
		//	blurOrNot = false;
		//	document.getElementById("user-name-input").setAttribute("readonly",true);
		//	document.getElementById("user-cardNo-input").setAttribute("readonly",true);
		//	document.getElementById("man").disabled = true;
		//	document.getElementById("woman").disabled = true;
		//	document.getElementById("user-cardType").disabled = true;
		//	document.getElementById("org").disabled = true;
		//	//$("#user-name-input")
        //
		//}
		$("#user-name input").val(ret.contact_name);
		$("#user-phone input").val(ret.client_phone);
		$("#user-email input").val(ret.client_email);
		//$("#user-other input").val(ret.client_other);
		//$("#contact-name input").val(ret.contact_name);
		$("#contact-phone input").val(ret.client_nationality);

		$("#user-cardvalidbegin-input").val(ret.client_validbegin);
		$("#user-cardvalidend-input").val(ret.client_validend);
		$("#user-zipcode-input").val(ret.client_zipcode);
		if(ret.city != ""){
			$("#user-province select").val(ret.province);
			resetCity(ret.province);
			$("#user-city select").val(ret.city);
		}else{
			$("#user-province select").val("请选择");
			$("#user-city select").val("请选择");
		}
		$("#user-address input").val(ret.address);
		$("#user-legal-name input").val(ret.client_legal_name);
		if(ret.client_legal_type != ""){
			$("#user-legal-cardType").val(ret.client_legal_type);
			$("#user-legal-no input").val(ret.represent_idno);
		}
		$("#focuse-message textarea").val(ret.focuse_message);
		if(ret.manager_value.length != 0){
			var checkboxArr = document.getElementById("focuse-manager").getElementsByTagName("input");
			var manager_list = ret.manager_value.substring(0,ret.manager_value.length-1).split(".");
			for(var i=0;i<manager_list.length;i++){
				checkboxArr[parseInt(manager_list[i])-1].checked = true;
			}
		}

		for(var i=0;i<ret.documentList[0].length;i++){
			$("#client_card").children().eq(i).children().eq(0).attr('src','../static/tempfiles/'+ret.documentList[0][i].name);
		}

		if(ret.client_risk_type != null) {
			var client_risk_type = ret.client_risk_type.split('.');
			var total_point = 0;
			for (var i = 0; i < client_risk_type.length; i++) {
				total_point += client_risk_type[i];
			}
			if (total_point <= 26) {
				$("#client_risk").children().eq(0).html('保守型')
			} else if (total_point > 26 && total_point < 39) {
				$("#client_risk").children().eq(0).html('稳健型')
			} else {
				$("#client_risk").children().eq(0).html('积极型')
			}

			$("#client_risk").children().eq(1).click(function () {
				window.open('../static/tempfiles/' + ret.documentList[1][0].name)
			});

		}
		//attr('href','../static/tempfiles/'+ret.documentList[1][0].name);
		for(var i=0;i<ret.documentList[2].length;i++){
			$("#client_asset").children().eq(i).children().eq(0).attr('src','../static/tempfiles/'+ret.documentList[2][i].name);
		}

		$(".card_img").click(function(){
			var imgSrc = $(this).attr('src');
			if(imgSrc.substr(imgSrc.length-9) != 'empty.png'){
				window.open($(this).attr('src'));
			}
		})

		$(".upload").click(function(){
			var splitList = $(this).siblings("img").attr("src").split("/");
			var imgList = splitList[splitList.length-1];
			if(imgList == "empty.png"){
				imgID = '';
			}else{
				imgID = imgList.split("_|_")[0];
			}
		})

		$(".delete").click(function(){
			var splitList = $(this).siblings("img").attr("src").split("/");
			var imgList = splitList[splitList.length-1];
			if(imgList == "empty.png"){
				imgID = '';
			}else{
				imgID = imgList.split("_|_")[0];
			}
			var sendDate = {'clientID':clientID,'imgID':imgID}
			$.getJSON('/deleteInAccredited/',sendDate,function(ret){
				$(this).siblings("img").attr("src","../static/img/crm_intention/empty.png");
			});
		})
	});
}

function getSendDate(){
	var client_org_name = $("#user-org-name input").val();
	if (client_org_name == "") {
		alert("请填写机构名称！");
		return;
	}else if(client_org_name.length > 64){
		alert("填写的机构名称过长！");
		return;
	}
	var client_org_holder = $("#user-org-holder input").val();
	var client_org_range = $("#user-org-range input").val();

	var client_name = $("#user-name input").val();
	if(client_name == ""){
		alert("请填写联系人姓名！");
		return;
	}else if(client_name.length >64){
		alert("填写的联系人姓名过长！");
		return;
	}

	var client_phone = $("#user-phone input").val();
	if (client_phone == "") {
		alert("请填写客户电话！");
		return;
	}else if(client_phone.length > 16){
		alert("填写的客户电话过长！");
		return;
	}
	var client_email = $("#user-email input").val();
	if (client_email == "") {
		alert("请填写客户邮件！");
		return;
	}else if(client_email.length > 48){
		alert("填写的客户邮件过长！");
		return;
	}

	var card_type = $("#user-cardType").val();
	var card_no = $("#user-cardNo input").val();
	if(card_type == "9" && card_no != ""){
		alert("请选择客户证件类型");
		return;
	}
	if(card_type != "9" && card_no == ""){
		alert("请选择客户证件号码");
		return;
	}
	if(card_type == "9" && card_no == ""){
		card_type = "";
	}
	if(card_no.length > 48){
		alert("填写的客户证件号码过长！");
		return;
	}

	var province = $("#user-province select").val();
	var city = $("#user-city select").val();
	var address = $("#user-address input").val();
	if(city == "请选择" && address != ""){
		alert("请选择省、市信息！")
		return;
	}
	if(city == "请选择" && address == ""){
		province = "";
		city = "";
	}
	if(address.length > 255){
		alert("填写的联系地址过长！");
		return;
	}
	var user_zipcode = $("#user-zipcode-input").val();
	var client_validbegin = $("#user-cardvalidbegin-input").val();
	var client_validend = $("#user-cardvalidend-input").val();

	var client_legal_name = $("#user-legal-name input").val();
	var client_legal_type = $("#user-legal-cardType").val();
	var client_legal_no = $("#user-legal-no input").val();

	var manager_value = "";
	$('input[name="manager"]:checked').each(function () {
		manager_value = manager_value +"."+ $(this).val();
	});
	manager_value = manager_value.substring(1,manager_value.length+1);
	var focuse_message = $("#focuse-message textarea").val();
	var sendData = {'client_name':client_org_name,'client_org_holder':client_org_holder,'client_org_range':client_org_range,
		'client_validbegin':client_validbegin,'client_validend':client_validend,
		'client_brithday':'', 'client_nationality':'','client_education':'','client_zipcode':user_zipcode, 'client_occupation':'','client_position':'','client_employer':'',
		'client_type':'0','card_type':card_type,'card_no':card_no,'sex':'','client_phone':client_phone,
		'client_email':client_email, 'client_other':'','contact_name':client_name,'contact_phone':'',
		'client_legal_name':client_legal_name,'client_legal_type':client_legal_type,'client_legal_no':client_legal_no,
		'focuse_message':focuse_message,'province':province,'city':city,'address':address,'manager_value':manager_value,
		'client_id':clientID,'build':"old"}
	if(clientID == undefined || clientID == ""){
		sendData.build = "new";
	}
	return sendData;
}

function cityChange(){
	var province = $(this).val();
	var provinceId = province_arr1.indexOf(province);
	$("#user-city select").empty();
	for(i = 0; i < city_arr1[provinceId].length; i++){
		$("#user-city select").append("<option>" + city_arr1[provinceId][i] + "</option>");
	}
}

function resetCity(province){
	var provinceId = province_arr1.indexOf(province);
	$("#user-city select").empty();
	for(i = 0; i < city_arr1[provinceId].length; i++){
		$("#user-city select").append("<option>" + city_arr1[provinceId][i] + "</option>");
	}
}

function deleteImage(id){
	var splitList = document.getElementById(id).src.split("/");
	//var splitList = document.getElementById(id);
	var imgList = splitList[splitList.length-1];
	if(imgList == "empty.png"){
		imgID = '';
	}else{
		imgID = imgList.split("_|_")[0];
	}
	var sendDate = {'clientID':clientID,'imgID':imgID}
	$.getJSON('/deleteInAccredited/',sendDate,function(ret){
		document.getElementById(id).src = "../static/img/crm_intention/empty.png";
	});
}

function selectImage(file,id,imgType){
	var imgName = file.files[0].name;
	var imageContent = '';
	if(!file.files || !file.files[0]){
		return;
	}

	if(imgType != '2'){
		var splitList = document.getElementById(id).src.split("/");
		var imgList = splitList[splitList.length-1];
		if(imgList == "empty.png"){
			imgID = '';
		}else{
			imgID = imgList.split("_|_")[0];
		}
	}else {
		imgID = '';
		var riskType = $("#wenjuan_point").val();
		if (riskType == '') {
			alert('请首先在左侧填写问卷得分');
			return;
		}
		$.getJSON('/changeRiskType/', {'clientID': clientID, 'riskType': riskType}, function (ret) {

		});
	}
	//var splitList = document.getElementById(id).src.split("/");
	//var imgList = splitList[splitList.length-1];
	//if(imgList == "empty.png"){
	//	imgID = '';
	//}else{
	//	imgID = imgList.split("_|_")[0];
	//}
	var reader = new FileReader();
	reader.onload = function(evt){
		imageContent = evt.target.result;
		var sendDate = {'clientID':clientID,'imgID':imgID,'imgName':imgName,'imgType':imgType,'imageContent':imageContent}
		$.post('/imageUpload/',sendDate,function(ret){
			document.getElementById(id).src = '../static/tempfiles/'+ret.url;
		});
	}
	reader.readAsDataURL(file.files[0]);
}