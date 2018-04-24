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
		window.location.href = "../account_org_editor";
	})


	$("#user-province select").empty();
	for(i = 0; i < province_arr1.length; i++){
		$("#user-province select").append("<option>" + province_arr1[i] + "</option>");
	}

	$("#user-province select").on("change", cityChange);
	if(clientID != undefined){
		fillInfo(clientID);
	}
	$("#quitBtn").click(function(){
		window.opener=null;
		window.open('','_self');
		window.close();
	});


	$("#saveBtn").click(function() {
		$.getJSON('/edit_crm_client/',getSendDate(),function(ret){
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
		$.getJSON('/edit_crm_client/',getSendDate(),function(ret){
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
		$("#user-name input").val(ret.client_name);
		if(ret.sex == "男"){
			$(':radio[name="sex"]').eq(0).attr("checked",true);
		}else if(ret.sex == "女"){
			$(':radio[name="sex"]').eq(1).attr("checked",true);
		}
		if(ret.card_type != ""){
			$("#user-cardType").val(ret.card_type);
			$("#user-cardNo input").val(ret.card_no);
		}

		if(ret.mark == '1'){
			blurOrNot = false;
			document.getElementById("user-name-input").setAttribute("readonly",true);
			document.getElementById("user-cardNo-input").setAttribute("readonly",true);
			document.getElementById("man").disabled = true;
			document.getElementById("woman").disabled = true;
			document.getElementById("user-cardType").disabled = true;
			//document.getElementById("org").disabled = true;
		}

		//var brithday = $('#user-brith-input').val();
		//var nationality = $('#user-nationality-input').val();
		//var education = $('#user-education-input').val();
		//var zipcode = $('#user-zipcode-input').val();
		//var occupation = $('#user-occupation-input').val();
		//var position = $('#user-position-input').val();
		//var employer = $('#user-employer-input').val();
		$("#user-brith-input").val(ret.client_brithday);
		$("#user-nationality-input").val(ret.client_nationality);
		$('#user-education-input').val(ret.client_education);
		$('#user-zipcode-input').val(ret.client_zipcode);

		$('#user-occupation-input').val(ret.client_occupation);
		$('#user-position-input').val(ret.client_position);
		$('#user-employer-input').val(ret.client_employer);
		$("#user-phone input").val(ret.client_phone);
		$("#user-email input").val(ret.client_email);
		$("#user-other input").val(ret.client_other);
		$("#contact-name input").val(ret.contact_name);
		$("#contact-phone input").val(ret.contact_phone);

		if(ret.city != "" && ret.city != null){
			$("#user-province select").val(ret.province);
			resetCity(ret.province);
			$("#user-city select").val(ret.city);
		}else{
			$("#user-province select").val("请选择");
			$("#user-city select").val("请选择");
		}
		$("#user-address input").val(ret.address);
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
	var client_name = $("#user-name input").val();
	if (client_name == "") {
		alert("请填写客户姓名！");
		return;
	}else if(client_name.length > 64){
		alert("填写的客户姓名过长！");
		return;
	}
	var sex = $('input[name="sex"]:checked').val();
	if(sex == undefined){
		sex = "";
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
	if(card_type == "99" && card_no != ""){
		alert("请选择客户证件类型");
		return;
	}
	if(card_type != "99" && card_no == ""){
		alert("请选择客户证件号码");
		return;
	}
	if(card_type == "99" && card_no == ""){
		card_type = "";
	}
	if(card_no.length > 48){
		alert("填写的客户证件号码过长！");
		return;
	}

	var client_other = $("#user-other input").val();
	if(client_other.length > 48){
		alert("填写的客户其他联系方式过长！");
		return;
	}

	var contact_name = $("#contact-name input").val();
	if(contact_name.length > 48){
		alert("填写的联系人姓名过长！");
		return;
	}
	var contact_phone = $("#contact-phone input").val();
	if(contact_phone.length > 16){
		alert("填写的联系人联系方式过长！");
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

	var brithday = $('#user-brith-input').val();
	var nationality = $('#user-nationality-input').val();
	var education = $('#user-education-input').val();
	var zipcode = $('#user-zipcode-input').val();
	var occupation = $('#user-occupation-input').val();
	var position = $('#user-position-input').val();
	var employer = $('#user-employer-input').val();
	var manager_value = "";
	$('input[name="manager"]:checked').each(function () {
		manager_value = manager_value +"."+ $(this).val();
	});
	manager_value = manager_value.substring(1,manager_value.length+1);
	var focuse_message = $("#focuse-message textarea").val();

	var sendData = {'client_org_name':'','client_org_holder':'','client_org_range':'','client_brithday':brithday,
		'client_nationality':nationality,'client_education':education, 'client_zipcode':zipcode,
		'client_occupation':occupation,'client_position':position,'client_employer':employer,
		'client_name':client_name,'client_type':'1','card_type':card_type,'card_no':card_no,'sex':sex,'client_phone':client_phone,
		'client_email':client_email, 'client_other':client_other,'contact_name':contact_name,'contact_phone':contact_phone,
		'client_legal_name':'','client_legal_type':'','client_legal_no':'','client_validbegin':'','client_validend':'',
		'focuse_message':focuse_message,'province':province,'city':city,'address':address,'manager_value':manager_value,
		'client_id':clientID,'build':"new"}
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
	//alert(document.getElementById(id).src);
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
	var reader = new FileReader();
	reader.onload = function(evt){
		imageContent = evt.target.result;
		var sendDate = {'clientID':clientID,'imgID':imgID,'imgName':imgName,'imgType':imgType,'imageContent':imageContent}
		$.post('/imageUpload/',sendDate,function(ret){
			if(imgType != '2'){
				document.getElementById(id).src = '../static/tempfiles/'+ret.url;
			}else{
				alert('上传成功!');
			}
		});
	};
	reader.readAsDataURL(file.files[0]);
}
