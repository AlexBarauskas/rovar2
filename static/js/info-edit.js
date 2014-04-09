function close_editor(e){
    $(this).parent().hide();
    var tcm = tinyMCE.get($(this).parent().find('textarea, input').attr('id'));
    var val;
    if(tcm){
	val = tcm.getContent();
    }
    else{
	val = $(this).parent().find('textarea, input').val();
    }
    $(this).parent().parent().find('.display').html(val).show();
}

function open_editor(e){
	      var h, w;
	      h = $(this).height();
	      w = $(this).width();
	      $(this).hide();
	      $(this).parent().find('.editor').show();
	      var tcm = tinyMCE.get($(this).parent().find('.editor textarea, .editor input').attr('id'));
	      if(tcm){
		  tcm.setContent($(this).html());
		  tcm.theme.resizeTo(w, h);
	      }
	      else{
		  $(this).parent().find('.editor textarea, .editor input').val($(this).html()).focus();//.css({width:w,height:h});
	      }
}

function hide_alerts(){
    $('.form-alert').animate({opacity:0, height:0, margin:0, padding:0},
			     {complete:function(){$('.form-alert').hide();}}
			    );
}

$(function(){
      $('.editable .display').click(open_editor);
      $('.close-editor').click(close_editor);
      $('.editor textarea, .editor input').blur(close_editor);
      setTimeout(hide_alerts,3000);      

      $('input[type="file"]').change(function(e){
					  var file = this.files[0];
					  var img = $(this).parent().find('img');
					  if(typeof file != 'undefined'){
					      var reader = new FileReader();
					      reader.onload = function(e) {
						  img.attr('src', e.target.result);
					      };
					      reader.readAsDataURL(file);
					  }
				      });
  });


