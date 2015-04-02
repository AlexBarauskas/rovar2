$(function(){

      $('#locations').click(function(){
				var el = $(this);
				if(el.attr('class').indexOf('visible')<0){
				    el.addClass('visible'); 
				    el.find('ul>li').animate({'height': '45px'});
				    
				}
				else{
				    el.removeClass('visible'); 
				    el.find('ul>li').animate({'height': 0});
				}
			    });
});