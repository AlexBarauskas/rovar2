//include "inherit.js"

OnbikeWidget = Class.extend(
    {_iconSize: 36,
     _kLeft: 0.317,
     points: [],


     init: function(container_id, options, host){
	 this._prefix = 'onbikewidget';
	 //if(typeof host != 'undefined')
	 //    this.host = host;
	 //else
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
		 "points": [],
		 "default_point": null,
		 "extra_info": true,
		 "popup": false
	     };
	 this._container = $(container_id);
	 this._init_map();
	 this._load_points();
	 if(this.options && this.options.css){
	     $('<style>').text(this.options.css).appendTo('head');
	 }
     },
     
     _init_map: function(){
	 if(this._container.find('#' + this._prefix + '-info').length)
	     this._info_container = this._container.find('#' + this._prefix + '-info');
	 else
	     this._info_container = $('<div>').attr('id', this._prefix + '-info').appendTo(this._container);
	 if(this._container.find('#' + this._prefix + '-map').length)
	     this._map_container = this._container.find('#' + this._prefix + '-map');
	 else
	     this._map_container = $('<div>').attr('id', this._prefix + '-map').appendTo(this._container).height('200px');
	 //this._map_container.css('min-height','400px');
	 var location = new L.LatLng(this.options.location.center[0], this.options.location.center[1]);
	 this.map = new L.Map(this._prefix + '-map');
	 this.map = this.map.setView(location, this.options.location.zoom);
	 L.tileLayer('http://onbike.by/map/tile/{z}/{x}/{y}.png',
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
	 data.unactiveIcon = new L.icon(
	     {iconUrl: this.host + data.marker,
	      iconSize: [this._iconSize, this._iconSize],
	      iconAnchor: [this._iconSize*this._kLeft, this._iconSize/2]
	     });
	 data.activeIcon = new L.icon(
	     {iconUrl: this.host + data.marker_active,
	      iconSize: [this._iconSize, this._iconSize],
	      iconAnchor: [this._iconSize*this._kLeft, this._iconSize]
	     });

	 var mpoint = L.marker(data.coordinates, {icon: data.unactiveIcon});
	 mpoint._data = data;
	 mpoint.addTo(this.map);
	 this.points.push(mpoint);
	 
	 var info_div = $('<div>').attr('id', this._prefix + '-point-' + data.id.toString()).attr('data', data.id).addClass(this._prefix + '-point-info').css('cursor', 'pointer');

	 $('<h1>').text(data.title).appendTo(info_div);
	 $('<p>').text(data.address).appendTo(info_div).addClass(this._prefix + '-address');
	 if(data.images && data.images.length){
	     var img = $('<img>').attr('src', this.host + data.images[0]).appendTo(info_div);
	     if(this.options.popup){
		 img.css({'width': '100%', 'height': 'auto;'});
	     }
	     else{
		 img.css({'max-width': '100%', 'height': 'auto;'});
	     }
	 }
	 if(data.description)
	     $('<p>').text(data.description).appendTo(info_div).addClass(this._prefix + '-description');
	 if(data.phones)
	     $('<p>').text(data.phones).appendTo(info_div).addClass(this._prefix + '-phones');
	 $('<div>').css({'clear': 'both','height': '10px'}).appendTo(info_div);
	 

	 if(this.options.popup){
	     mpoint.bindPopup($('<div>').append(info_div).html());
	     
	 }
	 
	 else{
	     info_div.appendTo(this._info_container).click(this.set_current.bind(this));    
	     $(mpoint._icon).addClass(data.type_slug);
	     $(mpoint._icon).attr('id', 'iconp-'+data.id.toString());
	     $(mpoint._icon).click(function(){info_div.click();});
	     if(data.id == this.options.default_point)
		 info_div.click();
	 }
     },
     
     set_current: function(el){
	 this._info_container.find('.' + this._prefix + '-point-info').removeClass('current');
	 $(el.currentTarget).addClass('current');
	 var pid = parseInt($(el.currentTarget).attr('data'));
	 for(var i = this.points.length - 1; i >= 0; i--){
	     if(this.points[i]._data.id == pid){
		 this.map.setView(this.points[i]._data.coordinates, this.map.getZoom());
		 this.points[i].setIcon(this.points[i]._data.activeIcon);
		 }
	     else{
		 this.points[i].setIcon(this.points[i]._data.unactiveIcon);
		 
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
/*
var popup_base_css = "#onbikewidget-map{position:absolute;width:100%;height:100%;top:0;left:0;}.onbikewidget-point-info h1{font-size: 20px;}.onbikewidget-point-info p{font-size: 14px;margin:0;padding:0;}.onbikewidget-point-info img{margin:10px;}";
var top_popup_base_css = ".onbikewidget-point-info{display:none;}.onbikewidget-point-info.current{display: block;}#onbikewidget-info{left:0;top:0;z-index: 10;position: absolute;background-color: rgba(255,255,255,0.5);width: 70%;margin-left:40px;padding:5px;max-width:400px;}#onbikewidget-map{position:absolute;width:100%;height:100%;top:0;left:0;}.onbikewidget-point-info img{margin:10px;}";
var embed_css = ".onbikewidget-point-info img{margin:10px;}.onbikewidget-point-info{margin:10px; padding:10px;border:solid 1px #999;}.onbikewidget-point-info.current{background-color:#fdfdfd;}";
var options = {location : {
		   "name": "Минск",
		   "bounds": [[53.73909273331522,27.24485246663044],[54.06090726668478,27.888481533369557]],
		   "center": [53.9, 27.566667],
		   "zoom": 12
	       },
	       "points": [120, 69, 190, 154],
	       "default_point": 69,
	       "extra_info": true,
	       //"popup": true,
	       //"css": popup_base_css
	       "popup": false,
	       //"css": top_popup_base_css
	       "css": embed_css
	     };



var ow = new OnbikeWidget("widget-example", options, 'http://onbike.by');
ow._request('locations', {}, function(data){console.log(data);});
*/
