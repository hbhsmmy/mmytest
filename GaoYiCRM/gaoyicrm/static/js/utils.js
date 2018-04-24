// JavaScript Document


// 校验文本
var checkTxt = {
    regMobile : /^0?1[3|4|5|7|8][0-9]\d{8}$/,//手机
    regTel : /^0[\d]{2,3}-[\d]{7,8}$/,
    cardCode : /^\d{17}[\dX]$/,
    emal : /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
}


/* 
 * 检测对象是否是空对象(不包含任何可读属性)。 //如你上面的那个对象就是不含任何可读属性
 * 方法只既检测对象本身的属性，不检测从原型继承的属性。 
 */
function isOwnEmpty(obj) 
{ 
    for(var name in obj) 
    { 
        if(obj.hasOwnProperty(name)) 
        { 
            return false; 
        } 
    } 
    return true; 
}; 
 
/* 
 * 检测对象是否是空对象(不包含任何可读属性)。 
 * 方法既检测对象本身的属性，也检测从原型继承的属性(因此没有使hasOwnProperty)。 
 */
function isEmpty(obj) 
{ 
    for (var name in obj)  
    { 
        return false; 
    } 
    return true; 
}; 




//--------------------------------
//获取action随机码
function getActionStr(platform, action, task) {
	var str = randomString(2) + platform + randomString(7) + action + randomString(5) + task + randomString(3);
	return str;
}


//--------------------------------
//将秒数变成时间格式的字符串
function transformTimeStr(time) {
	var mm = Math.floor(time / 60);
	var ss = time % 60;
	if (mm < 10) {
		mm = "0" + mm;
	}
	if (ss < 10) {
		ss = "0" + ss;
	}
	return mm + ":" + ss;
}

//--------------------------------
//将浮点数变成百分比的字符串
function transformPercent(num) {
	return Math.floor(num * 100) + "%";
}

//--------------------------------
//产生规定长度的随机字符串
function randomString(len) {
	len = len || 32;
	//默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
	var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
	var maxPos = $chars.length;
	var pwd = '';
	for (i = 0; i < len; i++) {
		pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
	}
	return pwd;
}

//--------------------------------
//验证用户名
function checkUserName(str) {
	var Regex = /^(\w|[\u4E00-\u9FA5])*$/;
	
	if (Regex.test(str)){
		return true;
	} else {
		return false;
	}
}

//--------------------------------
//验证是否中文
function checkStrIsCN(str) {
	var Regex = /^[\u4E00-\u9FA5]+$/;
	
	if (Regex.test(str)){
		return true;
	} else {
		return false;
	}
}

//--------------------------------
//验证邮件地址
function checkEmail(emailAddress) {
	var Regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	
	if (Regex.test(emailAddress)){
		return true;
	} else {
		return false;
	} 
}


//--------------------------------
//字符串验证
//txt 为 需要检查的文本对象
//type 为 类型：email——邮箱，phone——手机，username——用户名，zhongwen——全中文，name——姓名，verifyCode——验证码
function checkInputValue(txt, type) {
	
	var defaultVal = $(txt).attr('defaultValue');//获得默认值
	var val = $(txt).val();//获得值
	
	//alert("defaultValue:" + defaultVal);
	//alert("value:" + val);
	
	
	var isDefaultValue = true;
	if (defaultVal == val || val == "") {
		isDefaultValue = true;
	} else {
		isDefaultValue = false;
	}
	
	if (type == "email") {
		if (isDefaultValue) {
			alert("请输入邮箱地址");
			return false;
		}
		else if (!checkStringType(val, type)) {
			alert("邮箱地址不符合规定");
			return false;
		}
		else {
			return true;
		}
	}
	
	
	else if (type == "phone") {
		if (isDefaultValue) {
			alert("请输入手机号码（11位纯数字）");
			return false;
		}
		else if (!checkStringType(val, type)) {
			alert("手机号码不符合规定（11位纯数字）");
			return false;
		}
		else {
			return true;
		}
	}
	
	
	else if (type == "username") {
		if (isDefaultValue) {
			alert("请输入用户名");
			return false;
		}
		else if (!checkStringType(val, type)) {
			alert("用户名必须为2-10位中文/英文/数字/下划线");
			return false;
		}
		else {
			return true;
		}
	}
	
	
	else if (type == "zhongwen") {
		if (isDefaultValue) {
			alert("请输入中文内容");
			return false;
		}
		else if (!checkStringType(val, type)) {
			alert("输入内容必须为中文字符");
			return false;
		}
		else {
			return true;
		}
	}
	
	else if (type == "name") {
		if (isDefaultValue) {
			alert("请输入您的姓名");
			return false;
		}
		else if (!checkStringType(val, type)) {
			alert("姓名必须为2-10位中文/英文");
			return false;
		}
		else {
			return true;
		}
	}
	
	else if (type == "verifyCode") {
		if (isDefaultValue) {
			alert("请输入验证码");
			return false;
		}
		else {
			return true;
		}
	}
	
	
	else {
		if (isDefaultValue) {
			alert("请输入完整的信息");
			return false;
		}
		else {
			return true;
		}
	}
}
//--------------------------------
//字符串验证
//string 为 需要检查的字符串
//type 为 类型：email——邮箱，phone——手机，username——用户名，zhongwen——全中文，name——姓名，verifyCode——验证码
function checkStringType(string, type) {
	var Regex;
	
	if (type == "email") {
		Regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		return Regex.test(string);
	}
	
	else if (type == "phone") {
		if (isNaN(string) || string.length != 11) {
			return false;
		}
		else {
			return true;
		}
	}
	
	else if (type == "username") {
		if (string.length < 2 || string.length > 10) {
			return false;
		}
		else {
			Regex = /^(\w|[\u4E00-\u9FA5])*$/;
			return Regex.test(string);
		}
	}
	
	else if (type == "zhongwen") {
		Regex = /^[\u4E00-\u9FA5]+$/;
		return Regex.test(string);
	}
	
	else if (type == "name") {
		if (string.length < 2 || string.length > 10) {
			return false;
		}
		else {
			Regex = /^(\w|[\u4E00-\u9FA5])*$/;
			return Regex.test(string);
		}
	}
	
	else {
		return true;
	}
}


//--------------------------------
//监测应用是否是本地运行
function checkLocal() {
	//return location.host == "127.0.0.1:8020";
	if (location.host == "127.0.0.1:8020" || location.host == "") {
		return true;
	} else {
		return false;
	}
}


//--------------------------------
//数值计算
function numCalculation(oldVol, Increase) {
	var danwei;
	if (oldVol.indexOf("%") > 0) {
		danwei = "%";
	} else if (oldVol.indexOf("px") > 0) {
		danwei = "px";
	}
	return (parseInt(oldVol.replace(danwei,"")) + Increase) + danwei;
}

//--------------------------------
//隐藏对象
function hideObj(obj) {
	$(obj).css("display", "none");
}

//--------------------------------
//获取url的参数
function getRequest() {
   var url = location.search; //获取url中"?"符后的字串
   var theRequest = new Object();
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}


//--------------------------------
//截图
//displayObject: 要截取的DOM对应
//callback: 完成后回调函数，定义此函数接收截取结果
//pictyle: 返回的图片类型，"img"或"dataUrl"，img将返回img元素，dataUrl将返回图片数据
function snapPic(displayObject, callback, pictyle){
	var type = pictyle ? pictyle : "img";
	html2canvas(displayObject, {
		allowTaint: true,
		taintTest: false,
		onrendered: function(canvas) {
			//截图完成
			//canvas.id = "mycanvas";
			//document.body.appendChild(canvas);
			//var dataUrl = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); //生成png图像并下载
			//var dataUrl = canvas.toDataURL();//生成base64图片数据
			canvas.crossOrigin = "*";
			var dataUrl = canvas.toDataURL("image/jpeg");//生成jpg图像
			
			if (callback) {
				if (type == "img") {
					var newImg = document.createElement("img");
					newImg.src =  dataUrl;
					callback(newImg);
				} else {
					callback(dataUrl);
				}
			}
		}
	});				
}


//--------------------------------
//截取整个页面
function snapPage(){
	//alert("开始截图");
	
	html2canvas(document.body, {
		allowTaint: true,
		taintTest: false,
		onrendered: function(canvas) {
			//截图完成
			//canvas.id = "mycanvas";
			//document.body.appendChild(canvas);
			//生成base64图片数据
			var dataUrl = canvas.toDataURL();
			var newImg = document.createElement("img");
			newImg.src =  dataUrl;
			//document.body.appendChild(newImg);
			document.getElementById("page1").appendChild(newImg);
			//alert("ok");
		}
	});				
}

//--------------------------------
//切换容器内的内容
function shiftContent(content, container){
	container.empty();//清空容器
	container.load(content);//加载内容
	//container.append("<div>aaasasasasa2</div>");  //追加元素至容器
}

//--------------------------------
//图片预加载
//  arr：可以是存放图片路径的一个数组，也可以是选取到的img的jquery对象；
//  funLoading：每一个单独的图片加载完成后执行的操作；
//  funOnLoad：全部图片都加载完成后的操作；
//  funOnError：单个图片加载出错时的操作。
function loadimg(arr, funLoading, funOnLoad, funOnError){  
    var numLoaded=0,  
    numError=0,  
    isObject=Object.prototype.toString.call(arr)==="[object Object]" ? true : false;  
   
    var arr=isObject ? arr.get() : arr;  
    for(a in arr){  
        var src=isObject ? $(arr[a]).attr("data-src") : arr[a];  
        preload(src,arr[a]);  
    }  
   
    function preload(src,obj){  
        var img=new Image();  
        img.onload=function(){  
            numLoaded++;  
            funLoading && funLoading(numLoaded,arr.length,src,obj);  
            funOnLoad && numLoaded==arr.length && funOnLoad(numError);  
        };  
        img.onerror=function(){  
            numLoaded++;  
            numError++;  
            funOnError && funOnError(numLoaded,arr.length,src,obj);  
        }  
        img.src=src;
    }  
}



//--------------------------------
//给phone加XXXX
function phoneXXXX(phoneStr) {
	if (phoneStr.length > 3) {
		if (phoneStr.length > 7) {
			var endStr = phoneStr.substring(7, phoneStr.length-1);
		}
		phoneStr = phoneStr.substr(0,3) + ("XXXX").substr(0, (phoneStr.length - 3));
		if (endStr) {
			phoneStr += endStr;
		}
		return phoneStr;
	} else {
		return phoneStr;
	}
}



//--------------------------------
//绑定文本提示
function inputBind(txt) {
	//输入文本处理
	txt.bind({ 
		focus:focusHandler, 
		blur:blurHandler
	});
	
	function focusHandler() {
		if (this.value == this.defaultValue){ 
			this.value=""; 
		} 
	}
	
	function blurHandler() {
		if (this.value == ""){ 
			this.value = this.defaultValue; 
		} 
	}
}


//绑定文本提示
function getTime()
{
	//获取时间
	var date = new Date();
	
	var currentYear = date.getFullYear();
	var currentMonth = date.getMonth() + 1;
	var currentDay = date.getDate();
	
	if (currentMonth < 10) currentMonth = "0" + String(currentMonth);
	if (date.date < 10) currentDay = "0" + String(currentDay);
	
	var _hours = date.getHours();
	var _minutes = date.getMinutes();
	var _seconds = date.getSeconds();
	
	if (_hours < 10) _hours = "0" + String(_hours);
	if (_minutes < 10) _minutes = "0" + String(_minutes);
	if (_seconds < 10) _seconds = "0" + String(_seconds);
	
	var str = currentYear + "-" + currentMonth + "-" + currentDay + " " + _hours + ":" + _minutes + ":" + _seconds;
	return str;
}


//--------------------------------
//取数组中的一个随机元素
function getRandomOne(oArray) {
	var n = Math.floor(Math.random() * (oArray.length - 0.000001));
	return(oArray[n]); 
}


//--------------------------------
//将整个数组随机排序
function randomArray(oArray) {
	Arr1.sort(function(){return Math.random()>0.5?-1:1;});  
	return(Arr1); 
}


function getFloat(floatvar,digit){
    var f_x = parseFloat(floatvar);
    if (isNaN(f_x)){
        return '0.00';
    }
    var f_x;
    if(digit == 2){
        f_x = Math.round(f_x*100)/100;
    }else if(digit == 4){
        f_x = Math.round(f_x*10000)/10000;
	}else if(digit == 3){
        f_x = Math.round(f_x*1000)/1000;
    }
    var s_x = f_x.toString();
    var pos_decimal = s_x.indexOf('.');
    if (pos_decimal < 0){
        pos_decimal = s_x.length;
        s_x += '.';
    }
    while (s_x.length <= pos_decimal + digit){
        s_x += '0';
    }
    return s_x;
}

function fondsFormat(number) {
	var below = false
	var number = number
	if(number[0]=="-"){
		below = true
		number = number.substring(1,number.length);
	}

	if(number.length==0)
		return "0.00";
	if(number.indexOf(".")==-1){
		number+=".00";
	}
	var firstNumber = number.substring(0, number.indexOf("."));
	var lastNumber = number.substring(number.indexOf(".")+1);
	firstNumber=firstNumber.split("").reverse().join("");
	var numberSB="";
	var leng=firstNumber.length;
	leng= (leng % 3==0?leng/3:(leng/3)+1);
	for (var  i = 0; i <leng ; i++) {
		numberSB+=",";
		if(i+1<leng)
			numberSB+=firstNumber.substring(i*3, (i+1)*3);
		if(i+1==leng)
			numberSB+=firstNumber.substring(i*3);
	}

	var resultNumber=numberSB.split("").reverse().join("");
	resultNumber=resultNumber.substring(0, resultNumber.length-1);
	resultNumber+="."+lastNumber;

	if(resultNumber[0] == ','){
		resultNumber = resultNumber.substring(1,resultNumber.length);
	}

	if(below){
		resultNumber = '-'+ resultNumber
	}
	return resultNumber
}
