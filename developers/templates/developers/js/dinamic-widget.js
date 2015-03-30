

function _onbike_init(){
    var host = "http://{{host}}";
    var insert_script = function(url, onload){
	var s = document.createElement('script');
	s.type = 'text/javascript';
	s.src = url;
	s.async = false;
	if(typeof onload != 'undefined')
	    s.onload = onload;
	var _s = document.getElementsByTagName('script')[0];
	_s.parentNode.insertBefore(s, _s);
    };
    
    var l = document.createElement('link');
    l.type = "text/css";
    l.rel = "stylesheet";
    l.href = "/static/leaflet73/leaflet.css";
    var h=document.getElementsByTagName('head')[0].childNodes[0];
    h.parentNode.insertBefore(l,h);
    

    var _init_onbike_widget = function(){
	var options = {{options|safe}};
	var ow = new OnbikeWidget(options.root, options, 'http://onbike.by');
    };

    if(typeof jQuery != 'function')
	insert_script(host + "/static/widget/libs/jquery.min.js");
    insert_script(host + "/static/leaflet73/leaflet-src.js");
    insert_script(host + "/static/leaflet73/leaflet.js");
    insert_script(host + "/static/widget/libs/inherit.js");
    insert_script(host + "/static/widget/widget.js", _init_onbike_widget);
    
}



if (window.addEventListener){
  window.addEventListener('load',_onbike_init,false);
} else if (window.attachEvent){
  document.attacheEvent('onload',_onbike_init,false);
} else {
  __onbike_init();
};