$(function(){
    
$('.hoge').hover(
    function(){
        $(this).parent('.paper').css('background-color', '#efefef');
    },function(){
        $(this).parent('.paper').css('background-color', '#fff');
    }
)
});