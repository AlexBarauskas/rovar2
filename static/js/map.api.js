var rovar = {
    elements:{},
    _iconSize: 36,
    _kLeft: 0.317,
    _numberPoint: 0,
    _numberLoadPoint: 0,

    _visible_pins : function(){
    },

    init : function(){
	var map = new L.Map('map');
	var self = this;
	map.on('zoomend', function(ev){
		   self._visible_pins();
	       });
	
	var minsk = new L.LatLng(53.9, 27.566667);
	this.copyright = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
	this.map = map.setView(minsk, 12);
	L.tileLayer('http://onbike.by/map/tile/{z}/{x}/{y}.png',
		    {attribution: this.copyright,
		     key: 'BC9A493B41014CAABB98F0471D759707',
		     minZoom: 12
		    }).addTo(this.map);
	this.map.setMaxBounds([[53.775, 27.31304168701172], [54, 27.820472717285156]]);
    },

    backToHome : function(){
	if(this.currentPoint)
	    this._hidePointInfo(this.currentPoint);
    },

    _hidePointInfo : function(point){
	var self = this;
	point.setIcon(point._data.unactiveIcon);
	$(point._icon).click(function(){self._showPointInfo(point);});
	$(point._icon).addClass(point._data.type_slug);

	$('.preview-content').html('');
	$('.preview').hide();

	var stateObj = { foo: "bar" };
	history.pushState(stateObj, "page", '/');	  

	$('#back-to-banner').hide();
	$('#type').hide();
	$('#banner').show();
	$("#header").css('background-color', "#e95d24");
    },

    _showPointInfo : function(point){
	if(this.currentPoint)
	    this._hidePointInfo(this.currentPoint);
	var self = this;
	point.setIcon(point._data.activeIcon);
	$(point._icon).click(function(){self._hidePointInfo(point);});
	this.currentPoint = point;


	$('#banner').hide();
	$('#back-to-banner').show();
	$('#type').show();

	var description,
	data = point._data;
	if(data.post_url)
	    description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	else
	    description = "<p>"+data.description+"</p>";
	var preview = $('.preview-content').html('')
	    .append($("<h1>"+data.title+"</h1>").css('color', data.color))
	    .append($("<p></p>").html(data.address).addClass('description-address'));
	if(data.images && data.images.length){
	    $('<img/>').attr({'src': data.images[0], 'title': "Show more..."}).appendTo(preview);
	}
	preview.append(description);
	if(data.phones)
	    preview.append($("<p></p>").html(data.phones));
	preview.parent().show();
	$("#type").html(data.type_name);
	$("#header").css('background-color', data.color);
	var stateObj = { foo: "bar" };
	history.pushState(stateObj, "page", '/'+ data.uid +'/');	  

	if(typeof DISQUS != 'undefined'){
	    DISQUS.reset({
			     reload: true,
			     config: function () {  
				 this.page.identifier = data.uid;  
				 this.page.title = data.title;
				 this.page.url = "http://onbike.by/"+data.uid+"/";
			     }
			 });
	    $('#disqus_thread').show();
	}	
	
    },


    _addPointToMap : function(data){
	var self = this;
	var type = data.type_slug;
	var eid = data.id;
	data.unactiveIcon = new L.icon({
					   iconUrl: data.marker,
					   iconSize: [this._iconSize, this._iconSize],
					   iconAnchor: [this._iconSize*this._kLeft, this._iconSize/2]
				       });
	data.activeIcon = new L.icon({
					 iconUrl: data.marker_active,
					 iconSize: [this._iconSize, this._iconSize],
					 iconAnchor: [this._iconSize*this._kLeft, this._iconSize]
				     });

	var point = L.marker(data.coordinates, {color: 'red', icon: data.unactiveIcon});
	point._data = data;
	point.addTo(this.map);
	$(point._icon).addClass(type);
	$(point._icon).click(function(){self._showPointInfo(point);});

	if(type in this.elements){
	    this.elements[type][eid] = point;    
	}else{
	    this.elements[type] = {};    
	    this.elements[type][eid] = point;
	}
    },
    
    loadPoints : function(){
	var self = this;
	$.ajax({url: '/api/points',
		method: 'GET',
		data: {uid: 'webclient'},
		success: function(data){
		    for(var i=data.length-1; i>=0; i--)
			self._addPointToMap(data[i]);
		}
	       });	
    }
};


$(function(){
      rovar.init();
      rovar.loadPoints();
      $('#back-to-banner').click(function(){rovar.backToHome();});
  });