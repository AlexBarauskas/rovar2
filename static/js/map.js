var tmp;

function play(id){
    var video = $("#video-"+id.toString());
    $("#video-wrap").show();
    video.css({position: "relative",
	       top:"100px",
	       margin:"0 auto",
	       width:"700px"
	      })
	.show();
    
};

function play_close(id){
    var video=$("#video-"+id.toString()).hide();
    var tmp =video.html();
    video.html('');
    video.html(tmp);
    $("#video-wrap").hide();
  
};

var rovar = {
    tracks : [],
    points : [],
    services : [],
    parkings : [],
    

    init : function(){
	var map = new L.Map('map');
	var minsk = new L.LatLng(53.9, 27.566667);
	this.copyright = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
	this.map = map.setView(minsk, 12);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
		    {attribution: this.copyright}).addTo(this.map);
    },

    addTrack : function (data){
	var polyline = L.polyline(data.route, {color: 'blue'});
	//tmp=data;
	var video='', btn='';
	if(data.video!=''){
	    video=$("<div id=\"video-"+data.id.toString()+"\">"+
		    data.video+
		    "</div>")
		.addClass("video");
	    video.prepend("<a href=\"javascript:play_close("+
			  data.id.toString()+
			  ")\" class=\"close\">X</a><br/>");
	    video.hide().appendTo('#video-wrap');
	    btn = "<a href=\"javascript:play("+
		data.id.toString()+
		")\">Смотреть видео</a>";
	}
	    
	   
	//console.log(video);
	polyline.addTo(this.map).bindPopup("<h1>"+data.title+"</h1>"+
					   "<p><a href=\""+"#"+"\">"+
					   data.description+"</a></p>"+
					   btn
					   );
	this.tracks.push(polyline);
    },

    loadTrack : function(id){
	var self = this;
	$.ajax({
		   url: '/map/track/'+id+'/',
		   method: 'GET',
		   success: function(data){
		       self.addTrack(data);
		   }
	       });	
    },

    loadTracks : function(filter){
	var self = this;
	$.ajax({url: '/map/available-tracks/',
		method: 'GET',
		data: filter,
		success: function(data){
		    for(var i=0;i<data.ids.length;i++){
			self.loadTrack(data.ids[i]);
		    }
		}
	       });	
    },

    clear : function(layers){
	for(var i=layers.length-1; i>=0;i--)
	    this.map.removeLayer(layers.pop());
    },

    addPoint : function (data){
	console.log(data.coordinates);
	var point = L.circle(data.coordinates,100, {color: 'red'});
	point.addTo(this.map).bindPopup("<h1>"+data.title+"</h1>"+
					"<p><a href=\""+"#"+"\">"+
					data.description+"</a></p>"
				       );
	if(data.type=="s"){
	    this.services.push(point);
	}else if(data.type=="p"){
	    this.parkings.push(point);
	}
    },

    loadPoints : function(filter){
	var self = this;
	$.ajax({url: '/map/available-points/',
		method: 'GET',
		data: filter,
		success: function(data){
		    for(var i=0;i<data.ids.length;i++){
			self.loadPoint(data.ids[i]);
		    }
		}
	       });	
    },
    
    loadPoint: function(id){
	var self = this;
	$.ajax({
		   url: '/map/point/'+id+'/',
		   method: 'GET',
		   success: function(data){
		       self.addPoint(data);
		   }
	       });	
    }

};

rovar.init();
rovar.loadTracks({});
rovar.loadPoints({type: 'Велопарковки'});
rovar.loadPoints({type: 'Сервисы'});

$(function(){
      $('.views .control li')
	  .click(function(){
		 if($(this).attr('class')=='disable'){
		     $(this).removeClass('disable');
		     if($(this).attr('id')=="trackctrl"){
			 rovar.loadTracks();
		     }else if($(this).attr('id')=="parkingctrl"){
			 rovar.loadPoints({type: 'Велопарковки'});
		     }else if($(this).attr('id')=="servicectrl"){
			 rovar.loadPoints({type: 'Сервисы'});
		     }
		 }else{
		     $(this).addClass('disable');
		     if($(this).attr('id')=="trackctrl"){
			 rovar.clear(rovar.tracks);	 
		     }else if($(this).attr('id')=="parkingctrl"){
			 rovar.clear(rovar.parkings);
		     }else if($(this).attr('id')=="servicectrl"){
			 rovar.clear(rovar.services);
		     }
		 }
		 });
});
