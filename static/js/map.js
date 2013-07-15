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
    elements:{},

    init : function(){
	var map = new L.Map('map');
	var minsk = new L.LatLng(53.9, 27.566667);
	this.copyright = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
	this.map = map.setView(minsk, 12);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
	//http://tile.stamen.com/toner-lite/6/36/21.png
	//L.tileLayer('http://tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
		    {attribution: this.copyright,key: 'BC9A493B41014CAABB98F0471D759707'}).addTo(this.map);
    },

    addTrack : function (data){
	function show_preview(data){
	var preview = $('.section.preview').html('')
	    .append("<h1>"+data.title+"</h1>");
	if(data.video!=''){
	    var video = $(data.video);
	    preview.append(video);
	    //if(preview.width()<preview.find('iframe').width())
	    video.height(video.height()*preview.width()/video.width());
	    video.width(preview.width());
	    
	    
	}
	if(data.post_url)
	    description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	else
	    description = "<p>"+data.description+"</p>";
	preview.append(description);
	preview.show();
	}
	/*var video='', btn='';
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
	var description;
	if(data.post_url)
	    description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	else
	    description = "<p>"+data.description+"</p>";
	   
	polyline.addTo(this.map).bindPopup("<h1>"+data.title+"</h1>"+
					   description+
					   btn
					   );
	*/
	var polyline = L.polyline(data.route, {color: data.color});
	polyline.addTo(this.map);
	//polyline.onclick(function(){console.log('CLICK');});
	//tmp = polyline;
	polyline._container.onclick = function(){show_preview(data);};
	this.elements[data.type[0]][data.type[1]].push(polyline);
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

    hide : function(layers){
	for(var i=layers.length-1; i>=0;i--)
	    this.map.removeLayer(layers[i]);
    },

    show : function(layers){
	for(var i=layers.length-1; i>=0;i--)
	    layers[i].addTo(this.map);
    },

    addPoint : function (data){
	//console.log(data.coordinates);
	if(data.status == 'success'){
	    var myIcon =new L.Icon({
				       iconUrl: data.marker,
				       iconSize: [20, 20],
				       iconAnchor: [10, 20]
				   });
	    var point = L.marker(data.coordinates, {color: 'red', icon: myIcon});
	    var description;
	    if(data.post_url)
		description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	    else
		description = "<p>"+data.description+"</p>";
	    point.addTo(this.map).bindPopup("<h1>"+data.title+"</h1>"+
					    description
					   );
	    this.elements[data.type[0]][data.type[1]].push(point);
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

$(function(){
      var types = $(".type-all");
      for(var i = types.length-1; i>=0; i--){
	  var id = types[i].id.split('-');
	  if(id[1]=='p'){
	      rovar.loadPoints({type: id[2]});
	  }else if(id[1]=='t'){
	      rovar.loadTracks({type: id[2]});
	  }
	  if(typeof rovar.elements[id[1]] == "undefined"){
	      rovar.elements[id[1]]={};
	  }
	  rovar.elements[id[1]][id[2]]=[];    
	  
      }
	  
      types.click(function(){
		      var id = this.id.split('-');
		      if($(this).attr('class').indexOf('disable')>=0){
			  $(this).removeClass('disable');
			  rovar.show(rovar.elements[id[1]][id[2]]);
		      }
		      else{
			  $(this).addClass('disable');
			  rovar.hide(rovar.elements[id[1]][id[2]]);
		      }		      
		  }
		 );
});
