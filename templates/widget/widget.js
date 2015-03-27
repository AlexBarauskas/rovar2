//include "inherit.js"

OnbikeWidget = Class.extend(
    {_iconSize: 36,
     _kLeft: 0.317,
     points: [],


     init: function(container_id, options, host){
	 this._prefix = 'onbikewidget';
	 if(typeof host != 'undefined')
	     this.host = host;
	 else
	     this.host = 'http://onbike.by';
	 this.api_url = '/api/';
	 if(typeof options != 'undefined')
	     this.options = options;
	 else
	     this.options = {
		 location : {
		     "name": "Минск",
		     "bounds": [[53.73909273331522,27.24485246663044],[54.06090726668478,27.888481533369557]],
		     "center": [53.9, 27.566667],
		     "zoom": 12
		 },
		 "points": [120, 69, 190],
		 "default_point": 69,
		 "extra_info": true
	     };
	 if(container_id[0] != '#')
	     container_id = '#' + container_id;
	 this._container = $(container_id);
	 this._init_map();
	 this._load_points();
     },
     
     _init_map: function(){
	 if(this._container.find('#' + this._prefix + '-info').length)
	     this._info_container = this._container.find('#' + this._prefix + '-info');
	 else
	     this._info_container = $('<div>').attr('id', this._prefix + '-info').appendTo(this._container);
	 if(this._container.find('#' + this._prefix + '-map').length)
	     this._map_container = this._container.find('#' + this._prefix + '-map');
	 else
	     this._map_container = $('<div>').attr('id', this._prefix + '-map').appendTo(this._container).height('400px');
	 var location = new L.LatLng(this.options.location.center[0], this.options.location.center[1]);
	 this.map = new L.Map(this._prefix + '-map');
	 this.map = this.map.setView(location, this.options.location.zoom);
	 L.tileLayer(//'//onbike.by/map/tile/{z}/{x}/{y}.png',
	     '//{s}.tile.osm.org/{z}/{x}/{y}.png',
	     {attribution: self.copyright,
	      key: 'BC9A493B41014CAABB98F0471D759707',
	      minZoom: 12
	     }).addTo(this.map);
	 this.map.setMaxBounds(this.options.location.bounds);
     },

     _load_points: function(){
	 this._request('points', {'id': this.options.points}, this.on_load_points.bind(this));
     },

     add_point_to_map: function(data){
	 var Icon = new L.icon(
	     {iconUrl: data.marker,
	      iconSize: [this._iconSize, this._iconSize],
	      iconAnchor: [this._iconSize*this._kLeft, this._iconSize/2]
	     });
	 var mpoint = L.marker(data.coordinates, {icon: Icon});
	 mpoint._data = data;
	 mpoint.addTo(this.map);
	 this.points.push(mpoint);
	 
	 var info_div = $('<div>').attr('id', this._prefix + '-point-' + data.id.toString()).attr('data', data.id).addClass(this._prefix + 'point-info').appendTo(this._info_container).css('cursor', 'pointer');
	 $('<h1>').text(data.title).appendTo(info_div);
	 if(data.images && data.images.length){
	     $('<img>').attr('src', this.host + data.images[0]).css({'float':'left','height':'100px','width':'auto'}).appendTo(info_div);
	 }
	 $('<p>').text(data.description).appendTo(info_div);
	 $('<p>').text(data.address).appendTo(info_div);
	 $('<div>').css({'clear': 'both','height': '10px'}).appendTo(info_div);
	 info_div.click(this.set_current.bind(this));


	 if(data.id == this.options.default_point)
	     this.map.setView(mpoint._data.coordinates, this.map.getZoom());
     },
     
     set_current: function(el){
	 this._info_container.find('.' + this._prefix + 'point-info').removeClass('currentr');
	 $(el.currentTarget).addClass('current');
	 var pid = parseInt($(el.currentTarget).attr('data'));
	 for(var i = this.points.length - 1; i >= 0; i--){
	     if(this.points[i]._data.id == pid){
		 this.map.setView(this.points[i]._data.coordinates, this.map.getZoom());
		 return null;
		 }
	 }
	 return null;
     },

     on_load_points: function(data){
	 for(var i = data.length - 1; i >= 0; i--)
	     this.add_point_to_map(data[i]);
     },


     _request: function(event, params, callback){
	 var callbackName = '__callback_' + this._prefix.toString()+'_'+parseInt(Math.random()*1000).toString();

	 var callbackWrapper = function(data){
	     callback(data);
	     window[callbackName] = undefined;
	     try{
		 delete window[callbackName];
		 
	     }catch(e){}
	 };

	 window[callbackName] = callbackWrapper; 
	 
	 params = $.extend({'callback' : callbackName,
			    'rtype': 'js'}, params);
	 
	 var _call_js = document.createElement('script');
	 _call_js.type = 'text/javascript';
	 _call_js.async = true;
	 _call_js.src = this.host + this.api_url + event + '?' + jQuery.param(params, true);
	 var s = document.getElementsByTagName('script')[0];
	 s.parentNode.insertBefore(_call_js, s);
     }

     
     
    }
);

/* EXAMPLES*/
var options = {
		 location : {
		     "name": "Минск",
		     "bounds": [[53.73909273331522,27.24485246663044],[54.06090726668478,27.888481533369557]],
		     "center": [53.9, 27.566667],
		     "zoom": 12
		 },
		 "points": [120, 69, 190],
		 "default_point": 69,
		 "extra_info": true
	     };

var ow = new OnbikeWidget("widget-example", options, 'http://onbike.by');
ow._request('locations', {}, function(data){console.log(data);});