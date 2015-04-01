
function add_from_url(){
    $.ajax({url: '/dev/utils/get-point',
	    data: {'url': $('[name="from-url"]').val(),
		   'location': $('[name="location"]').val()},
	    success: function(data){console.log(data);
				    if(data.success){
					var el = $('[name="ids"][value=""]');
					if(el.length == 0){
					    el = $("<input type=\"text\" name=\"ids\" value=\"\">").
						appendTo($('[name="ids"]').parent());
					}
					el.val(data.point.id);
					el.attr('value', data.point.id.toString());
					console.log(el, data.point.id);
				    }
				    $("#popup-add-from-url").hide();
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

$(function(){
      $("#add-url").click(show_popup_add_from_url);
      $("#popup-add-from-url a").click(add_from_url);
});