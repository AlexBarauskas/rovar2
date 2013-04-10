$(function(){
      $('.form-name').click(function(ev){
				var box= $(this).parent().parent();
				var is_opened=box.attr('class').split(' ').filter(function(e){return e=='open';}).length>0;
				if(is_opened)
				    box.removeClass('open');
				else
				    box.addClass('open');
			    });

      $('.delete').click(function(ev){
			     var box=$(this).parent().parent();
			     if(!!this.id){
				 $.ajax({method: 'POST',
					 url: this.id+'/delete/',
					 success: function(data){
					     if(data.success){
						 box.remove();
					     }
					     else{
						 for(var i=data.errors.length-1;i>=0;i--)
						     box.find('.form-fields').prepend('<p class="error">'+data.errors[i]+'</p>');
						 console.log(box);
						 box.addClass('open');
					     }
					 }
					});
			     }
			 });
});