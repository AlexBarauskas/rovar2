$(function() {

    var _phoneMask = "+999 (99) 999-99-99";
    var _phoneMaskList = [_phoneMask];
  
    $.smartbanner({
      title: "onbike.by",
      author: "Велосипедная карта города",
      price: 'FREE',
      appStoreLanguage: 'ru',
      inAppStore: 'On the App Store',
      inGooglePlay: 'In Google Play',
      inAmazonAppStore: 'In the Amazon Appstore',
      button: 'Скачать',
      scale: 'auto',
      iOSUniversalApp: true
    });

  	$('#locations, #typefilter').click(function(e){
  	  e.preventDefault();
  	});

    $('#info').click(function(e) {
      e.preventDefault();
      $(this).parent().toggleClass("hover");
      $(".popup_overlay").fadeToggle(250);
      $('#info-iframe').fadeToggle();
    });

    $("#info-iframe .button_close, .popup_overlay").click(function(){
      $("#info").click();
    });

    $("#gid-link").click(function(){
      var intro = introJs();
        intro.setOptions({
          nextLabel: 'Далее &rarr;',
          prevLabel: '&larr; Назад',
          skipLabel: "Пропустить",
          doneLabel: "Отлично!",
          steps: [
            {
              intro: "onbike.by — это велосипедная карта c важными объектами вашего города и маршрутами по нему. </br></br> <span style='font-size:10px;'>Нажмите <b>Далее &rarr;</b>, чтобы продолжить.</span>"
            },
            {
              element: '#locations',
              intro: "Выберите свой город.",
              position: 'bottom'
            },
            {
              element: '#typefilter',
              intro: "Кликните на название слоя с объектами, если хотите скрыть его с карты.",
              position: 'bottom'
            },
            {
              intro: 'Нажав на маршрут или точку на карте, можно получить подробную информацию. </br></br> К многим маршрутам прикреплено видео — с его помощью вы сможете лучше ориентироваться на незнакомой местности.',
            },
            {
              element: '#add-point-btn',
              intro: "Добавляйте новые точки на карту!",
              position: 'bottom'
            },
            {
              element: '#app-links',
              intro: 'И скачайте наше мобильное приложение! В нём очень удобно добавлять новые объекты, предлагать изменения и вообще – приближать светлое велосипедное будущее ;)',
              position: 'right'
            }
          ]
        });

        intro.onchange(function(){
          rovar.backToHome()
          $("#contentWrapper").attr('style', "z-index: -1 !important;");
        });

        intro.oncomplete(function() {
          $("#contentWrapper").attr('style', "z-index: 1 !important;");
        });

        intro.onexit(function() {
          $("#contentWrapper").attr('style', "z-index: 1 !important;");
        });

        intro.start();

    });


    function phoneCompleted(){
      $('input[name="phones"]')
        .last()
        .after("<input type='text' class='form-control' value=' placeholder='{% trans 'Добавить телефон' %}' name='phones'>");
      $('input[name="phones"]')
        .last()
        .addClass("other-phones")
        .inputmask("mask", 
          {
            "mask": _phoneMask,
            "oncomplete": phoneCompleted, 
            "oncleared": function(){ $(this).remove() }
          }
        );
    }

    function clearRootPhone(){
      var op = $(".other-phones");
      var set = false;
      for(var i=0; i<=op.length; i++){
        if ($(op[i]).val()) {
          if (!set) {
            $(this).val( $(op[i]).val() );
            $(op[i]).remove();
          }
          set = true;
        }else{
          $(op[i]).remove();
        }
      }
    }

    $('input[name="phones"]')
      .inputmask("mask", 
        { 
          "mask": _phoneMask,
          "oncomplete": phoneCompleted,
          "oncleared": clearRootPhone
        }
      );

});