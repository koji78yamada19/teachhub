$(function () {
    $('#delete-confirmation').click(function(){
        $('#modalArea').fadeIn();
        console.log('ここまで確認できてる')
    });
    $('#closeModal , #modalBg, #back-button').click(function(){
      $('#modalArea').fadeOut();
    });
  });