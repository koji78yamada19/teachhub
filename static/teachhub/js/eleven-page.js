$(function(){
    
$('.hoge').hover(
    function(){
        $(this).parent('.paper').css('background-color', '#f7f8f9');
    },function(){
        $(this).parent('.paper').css('background-color', '#fff');
    }
)


$('#upload-button-submit').prop('disabled', true);


$('input').on('change', function () {
    var file = $(this).prop('files')[0];
    $('#upload-file-name').text(file.name);
    $('#upload-button-submit').removeAttr('id');
    $('.upload-button-submit').prop('disabled', false);
    console.log('2');
});



});