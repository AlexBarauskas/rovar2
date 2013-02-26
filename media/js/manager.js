$(function(){
      $('.form-header').click(function(ev){
				var box= $(this).parent();
				var is_opened=box.attr('class').split(' ').filter(function(e){return e=='open';}).length>0;
				if(is_opened)
				    box.removeClass('open');
				else
				    box.addClass('open');
			    });
});