var rovar = {
    init : function(){
	var map = new L.Map('map');
	var minsk = new L.LatLng(53.9, 27.566667);
	this.copyright = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
	this.map = map.setView(minsk, 12);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
		    {attribution: this.copyright}).addTo(this.map);
    }
};

rovar.init();
L.marker([53.9, 27.566667]).addTo(rovar.map)
    .bindPopup('Minsk<br/> test popup')
    .openPopup();
