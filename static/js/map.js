var tmp;
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
	tmp=data;
	var polyline = L.polyline(data.route, {color: 'blue'});
	polyline.addTo(this.map);
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
L.marker([53.9, 27.566667]).addTo(rovar.map)
    .bindPopup('Minsk<br/> test popup')
    .openPopup();


$.ajax({
	   url: '/map/available-tracks/',
	   method: 'GET',
	   success: function(data){for(var i=0;i<data.ids.length;i++){rovar.loadTrack(data.ids[i]);}}
});