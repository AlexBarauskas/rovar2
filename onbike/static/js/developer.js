(function(){
    

function add_from_url(ev,url){
    if(typeof url == 'undefined')
	url = $('[name="from-url"]').val();
    $.ajax({url: '/dev/utils/get-point',
	    data: {'url': url,
		   'location': $('[name="location"]').val()},
	    success: function(data){if(data.success){
					var el = $('[name="ids"][value=""]');
					if(el.length == 0){
					    el = $("<input type=\"text\" name=\"ids\" value=\"\">").
						appendTo($('[name="ids"]').parent());
					}
					el.val(data.point.id);
					el.attr('value', data.point.id.toString());
					$('.top-allert').text(data.message)
					    .css({'background-color': 'rgba(128,255,128,0.7)',
						 'display':'block'});
				    }
				    else{
					$('.top-allert').text(data.message)
					    .css({'background-color': 'rgba(255,128,128,0.7)',
						  'display':'block'});
				    }
				    $("#popup-add-from-url").hide();
				    setTimeout(hide_alert,5000);
				   }
	    });
};

function show_popup_add_from_url(){
    $("#popup-add-from-url").show();
    var l = ($(window).width() - $("#popup-add-from-url").width())/2;
    var t = ($(window).height() - $("#popup-add-from-url").height())/2;
    $("#popup-add-from-url").css({'left': l.toString()+'px',
				  'top': t.toString()+'px'});
};

function show_popup_map(){
    var l = ($(window).width() - $("#popup-add-from-map").width())/2;
    var t = ($(window).height() - $("#popup-add-from-map").height())/2;
    if(t<0){
	t = 0;
	$("#popup-add-from-map").height($(window).height().toString()+'px');
    }
    $("#popup-add-from-map").css({left:l.toString()+'px'});
    $("#popup-add-from-map").animate({top:t.toString()+'px'});
}

function hide_popup_map(){
    $("#popup-add-from-map").animate({top:'-1000px'});
}

function add_from_map(){
    var url = $("#popup-add-from-map iframe")[0].contentWindow.window.location.href;
    add_from_url(null, url);
}

function hide_alert(){
    $('.top-allert').hide();
}

$(function(){
      $("#add-url").click(show_popup_add_from_url);
      $("#popup-add-from-url a.add").click(add_from_url);
      $("#add-from-map").click(show_popup_map);
      $("#popup-add-from-map a.add").click(add_from_map);
      $("#popup-add-from-map a.btn-close").click(hide_popup_map);
});

})();