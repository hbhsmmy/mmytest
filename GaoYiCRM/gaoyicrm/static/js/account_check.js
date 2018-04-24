$(document).ready(function() {
    cardImage(2);
});

function cardImage(count){
    switch (count){
        case 1:
            $('#card_div img').width("37.5%");
            break;
        case 2:
            $('#card_div img').width("35%");
            $("#card_div img").css("marginLeft",'5%');
            $("#card_div img").css("marginRight",'5%');
            break;
        case 3:
            $('#card_div img').width("27.5%");
            $("#card_div img").css("marginLeft",'2.5%');
            $("#card_div img").css("marginRight",'2.5%');
            break;
        case 4:
            $('#card_div img').width("21.5%");
            $("#card_div img").css("marginLeft",'1%');
            $("#card_div img").css("marginRight",'1%');
            break;
    }
}