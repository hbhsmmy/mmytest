var tradeID = ''
$(document).ready(function(){
    tradeID = window.location.href.split("=")[1];
    $.post('/getuploadData/',{'tradeID':tradeID},function(ret){
        //alert(ret);
        var documentList = ret.documentList;
        for(var i=0;i<documentList.length;i++){
            var item = documentList[i];
            $("#uploadImg"+item.type).attr('src','../static/tempfiles/'+item.name);
        }
        $(".card_img").click(function(){
            var imgSrc = $(this).attr('src');
            window.open($(this).attr('src'));
        })
    });

    $.getJSON('/getTradeDoc/',{'tradeID':tradeID},function(ret){
        $('#location input').val(ret.location);
    });

    $('#saveBtn').click(function(){
        if($('#location input').val() != ''){
            var sendData = {'tradeID':tradeID,'location':$('#location input').val()};
            $.getJSON('/saveTradeDoc/',sendData,function(ret){
                alert('保存成功');
                window.close();
            })
        }
    })
});


function selectImage(file,id,type){
    var name = file.files[0].name;
    var size = file.files[0].size;
    alert(name);
    alert(size);
    var reader = new FileReader();
    reader.onload = function(evt){
        imageContent = evt.target.result;
        var sendData = {'tradeID':tradeID,'name':name,'type':type,'imageContent':imageContent}

        $.post('/uploadData/',sendData,function(ret){
            document.getElementById(id).src = '../static/tempfiles/'+ret.url;
            alert('上传成功！')
        });
    }
    reader.readAsDataURL(file.files[0]);
}