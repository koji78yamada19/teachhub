$(function(){
    
$('.hoge').hover(
    function(){
        $(this).parent('.paper').css('background-color', '#efefef');
    },function(){
        $(this).parent('.paper').css('background-color', '#fff');
    }
)
});
$('input').on('change', function () {
    var file = $(this).prop('files')[0];
    $('#upload-file-name').text(file.name);
    $('.upload-input-label').attr('id', 'upload-input-label');
    $('#upload-button-submit').removeAttr('id')
});