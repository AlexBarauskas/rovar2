var __addClick;

var addpoint = {
    run: false,
    init: function(){
	//var ths = this;
/*
	$("#add-point-btn").click(
	    function(){
		$("#map").css('cursor', "crosshair");
		//ths.run = true;
		__addClick = function(e){addpoint.setCoordinates(e);};
		rovar.map.on('mousedown',__addClick);
	    });	
	$("#add-point-form-close").click(
	    function(){addpoint.hideDialog();}
	);
*/	
    },
    hideDialog: function(){
	$("#add-point-dialog").hide();
    },

    showDialog: function(){
	var d=$("#add-point-dialog").show();
	d.css('left', ($(document).innerWidth() - d.innerWidth())/2);
	d.css('top', ($(document).innerHeight() - d.innerHeight())/2);
    },

    setCoordinates: function(e){
	$('input[name="coordinates"]').val('[' + e.latlng.lng.toString() + ', ' + e.latlng.lat.toString() + ']');
	$("#map").attr('style', "");
	rovar.map.off('mousedown',__addClick);
	this.showDialog();
    }
};

$(function(){
      addpoint.init();
  });