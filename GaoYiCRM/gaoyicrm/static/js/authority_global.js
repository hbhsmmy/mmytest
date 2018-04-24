/**
 * Created by zhangchengyiming on 16/11/1.
 */

var positonPool = [];
var productOnly = [1];
var clientOnly = [2];
var lawAndIT = [0,1,2,3,4];
var operationAndCollect = [0,1,2,4];
var finishOrNot = false;
var applyListNot = false;
var capitalNot = false;
$(document).ready(function(){
    if(document.title != "高毅 - 登陆"){
        $.getJSON('/getAuthority/',function(ret){
            var authorityPool = getAuthorityPool(ret.roleList);
            if(applyListNot){
                waitGlobal1();
            }
            if(capitalNot){
                waitGlobal2();
            }
            finishOrNot = true;
            for(var i=0;i<5;i++){
                var exist = false;
                for(var k in authorityPool){
                    if(i == k){
                        exist = true;
                        break;
                    }
                }
                if(!exist){
                    $("#account-navs").children().eq(i).css("display", "none");
                    if(i < 4){
                        $("#account-navs-mb-info").children().eq(i).css("display", "none");
                    }
                }
            }
        });
    };
});

function getAuthorityPool(roleList){
    var authorityPool = {};
    for(var i=0;i<roleList.length;i++){
        var item = roleList[i];
        positonPool.push(item);
        switch (item){
            case 1000:
            case 1003: //合规岗和IT岗
                for(var j=0;j<lawAndIT.length;j++){
                    authorityPool[lawAndIT[j]] = lawAndIT[j];
                }
                break;
            case 1001:
            case 1002:  //产品募集岗和运营岗
                for(var j=0;j<operationAndCollect.length;j++){
                    authorityPool[operationAndCollect[j]] = operationAndCollect[j];
                }
                break;
            case 1004:  //产品查询岗
                for(var j=0;j<productOnly.length;j++){
                    authorityPool[productOnly[j]] = productOnly[j];
                }
                break;
            case 1005: //客户查询岗
                for(var j=0;j<clientOnly.length;j++){
                    authorityPool[clientOnly[j]] = clientOnly[j];
                }
                break;
        }
    }
    return authorityPool
}

function judgeAuthority(position){
    for(var i=0;i<positonPool.length;i++){
        if(position == positonPool[i]){
            return true;
        }
    }
    return false;
}