/*function imgpv_load(){
    var imgs_preview = $('#images-preview');
    $('#images-preview .row-left, #images-preview .row-right').css({'line-height': imgs_preview.find('img.active').height()+'px'});
    imgs_preview.animate({'height': imgs_preview.find('img.active').height()});
}

function next_imgpv(inc){
    var imgs_preview = $('#images-preview');
    var n = imgs_preview.find('img').length;
    if(n>1){
	var ci = $('#images-preview img.active'), nci;
	var i = imgs_preview.find('img').toArray().indexOf(ci[0]) + inc;
	if((inc>=0 & i<0) | (inc<0 & i<-1)){
	    imgs_preview.find('img').first().addClass('active');
	    imgs_preview.animate({'height': imgs_preview.find('img.active').height()});
	    $('#images-preview .row-left, #images-preview .row-right').animate({'line-height': imgs_preview.find('img.active').height()+'px'});
	}
	else{
	    console.log(i);
	    if(i == n){
		i = 0;
	    }
	    if(i == -1){
		i = n-1;
	    }
	    nci = $(imgs_preview.find('img')[i]);
	    nci.addClass('active');
	    nci.css('opacity', 0);
	    ci.animate({'opacity': 0}, {queue: false});
	    imgs_preview.animate({'height': nci.height()}, {queue: false});
	    $('#images-preview .row-left, #images-preview .row-right').animate({'line-height': nci.height()+'px'});
	    nci.animate({'opacity': 1}, {queue: false});
	    ci.removeClass('active');
	}
    }
}
*/
