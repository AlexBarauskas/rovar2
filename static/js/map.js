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
	tmp=data;
	var video='';
	if(data.video!=''){
	    video=$("<div id=\"video-"+data.id.toString()+"\">"+
		    data.video+
		    "</div>")
		.addClass("video");
	    video.prepend("<a href=\"javascript:play_close("+
			  data.id.toString()+
			  ")\" class=\"close\">X</a><br/>");
	    video.hide().appendTo('#video-wrap');
	}
	    
	   
	console.log(video);
	polyline.addTo(this.map).bindPopup("<h1>"+data.title+"</h1>"+
					   "<p><a href=\""+"#"+"\">"+
					   data.description+"</a></p>"+
					   "<a href=\"javascript:play("+
					   data.id.toString()+
					   ")\">Смотреть видео</a>"
					   );
	tmp =polyline;
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
    }
};

rovar.init();
//L.marker([53.9, 27.566667]).addTo(rovar.map)
//    .bindPopup('Minsk<br/> test popup')
//    .openPopup();


$.ajax({
	   url: '/map/available-tracks/',
	   method: 'GET',
	   success: function(data){
	       for(var i=0;i<data.ids.length;i++){
		   rovar.loadTrack(data.ids[i]);
	       }
	   }
});