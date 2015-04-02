function delete_obj(oid, node){
    $.ajax({method: 'POST',
	    url: oid+'/delete/',
	    success: function(data){
		if(data.success){
		    node.parent().remove();
		}
		else{
		    for(var i=data.errors.length-1;i>=0;i--)
			node.find('.form-fields').prepend('<p class="error">'+data.errors[i]+'</p>');
		    node.addClass('open');
		}
	    }
	   });
}


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
			     var box=$(this).parent();
			     if(!!this.id){
				 
				 if (confirm('Удалить "'+(box.parent().find('td').first().text().replace(/^\s+|\s+$/g, '') || box.parent().find('.form-name').text().replace(/^\s+|\s+$/g, ''))+'"?')) {
				     delete_obj(this.id, box);
				 } else {
				 }				 

			     }
			 });
});