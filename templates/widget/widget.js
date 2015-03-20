//include "inherit.js"

OnbikeWidget = Class.extend(
    {init: function(container_id, options){
	 this._prefix = 'onbikewidget';
	 this.api_url = 'http://localhost:8000/api/';
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
		 "points": [120, 69],
		 "extra_info": true
	     };
	 this._container = $(container_id);
	 this._init_map();
     },
     
     _init_map: function(){
	 this._info_container = $('<div>').attr('id', this._prefix + '-info').appendTo(this._container).width('100%').height('30%').css('background-color', "#fff").append("<h1>Point info</h1>");
	 this._map_container = $('<div>').attr('id', this._prefix + '-map').appendTo(this._container).width('100%').height('70%');
	 var location = new L.LatLng(this.options.location.center[0], this.options.location.center[1]);
	 this.map = new L.Map(this._prefix + '-map');
	 this.map = this.map.setView(location, this.options.location.zoom);
	 L.tileLayer('//onbike.by/map/tile/{z}/{x}/{y}.png',
		     {attribution: self.copyright,
		      key: 'BC9A493B41014CAABB98F0471D759707',
		      minZoom: 14
		     }).addTo(this.map);
	 this.map.setMaxBounds(this.options.location.bounds);
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
	 _call_js.src = this.api_url + event + '?' + jQuery.param(params, true);
	 var s = document.getElementsByTagName('script')[0];
	 s.parentNode.insertBefore(_call_js, s);
     }

     
     
    }
);

/* EXAMPLES*/
var ow = new OnbikeWidget("#widget-example");
ow._request('locations', {}, function(data){console.log(data);});