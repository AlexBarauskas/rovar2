o.extend(this, {

	     XHR: o.XMLHttpRequest,

	     DOM: jQuery('body'),

	     runtimeOptions: {
		 container: "qunit-fixture",
		 swf_url: "Moxie.swf",
		 xap_url: "Moxie.xap"
	     },

	     runtimeOrder: "html5"
	     //,flash,silverlight,html4
	 });

o.Image.MAX_RESIZE_HEIGHT = 10000;
o.Image.MAX_RESIZE_WIDTH = 10000;


var __addClick;


var rovar = {
    elements:{'points': {}, 'tracks': {}},
    sort_ids: {},
    _iconSize: 36,
    _kLeft: 0.317,
    _numberPoint: 0,
    _numberLoadPoint: 0,
    messages : {
	'edit' : 'Редакрировать',
	'travel time' : 'Время в пути',
	'add point' : '+ Добавить точку',
	'set coordinates' : 'Выберите место на карте (Esc для отмены)',
	'unknown error' : 'Неизвестная ошибка.',
	'success message' : 'Ваше предложение будет рассмотрено модератором.',
	'error request method' : "Неверный тип запроса.",
	'not init client' : "Ваш клиент не инициализирован.",
	'required fields' : "Поля 'Название', 'Категория', 'Описание', 'Адрес' являются обязательными.",
	'unknown url' : "Указанный тип точки не существует.",
	'required image' : "Вы не выбрали изображение или оно не верного формата.",
	'invalide url' : "Не верный URL для поля 'Cайт'.",
	'feedback email' : "Введите email для обратной связи."
    },


    _visible_pins : function(){
    },

    init : function(){
	if(typeof rovar_transplate != 'undefined' & typeof language_code != 'undefined'){
	    if(typeof rovar_transplate[language_code] != 'undefined'){
		this.messages = rovar_transplate[language_code];
		}
	}

	this.__errors = {
	    1 : this.messages['error request method'],
	    2 : this.messages['not init client'],
	    3 : this.messages['required fields'],
	    4 : this.messages['unknown url'],
	    5 : this.messages['required image'],
	    6 : this.messages['invalide url'],
	    100 : this.messages['feedback email']
	};


	var map = new L.Map('map');
	var self = this;
	map.on('zoomend', function(ev){
		   self._visible_pins();
	       });
	this.copyright = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
	
	var l_name;
	if(typeof rovar_location != 'undefined')
	    l_name = rovar_location;
	else
	    l_name = 'Minsk';

	$.ajax({url: '/api/location',
		method: 'GET',
		data: {name: l_name},
		success: function(data){
		    self.location = data;
		    var minsk = new L.LatLng(self.location.center[0], self.location.center[1]);
		    self.map = map.setView(minsk, 12);
		    L.tileLayer('http://onbike.by/map/tile/{z}/{x}/{y}.png',
				{attribution: self.copyright,
				 key: 'BC9A493B41014CAABB98F0471D759707',
				 minZoom: 12
				}).addTo(self.map);
		    //self.map.setMaxBounds([[53.775, 27.31304168701172], [54, 27.820472717285156]]);
		    self.map.setMaxBounds(self.location.bounds);
		    self.loadPoints();
		    self.loadTracks();
		}
	       });	

	this.uploader = new CustomUpload($("#inputfile"));
	$('#upload-imgs').click(
	    function(){
		var p = $('[name="phones"]');
		var phones = [];
		for(var i=p.length; i>=0; i--)
		    phones.push($(p[i]).val());
		self.uploader.uploadFiles(function(response, finish){
					      //console.log(response, finish);
					      self.callbackAddPoint(response);
					  },
					  {'website': $('[name="website"]').val(),
					   'description': $('[name="description"]').val(),
					   'title': $('[name="title"]').val(),
					   'phones': phones,
					   'coordinates': $('[name="coordinates"]').val(),
					   'address': $('[name="address"]').val(),
					   'type': $('[name="type"]').val(),
					   'email': $('[name="email"]').val(),
					   'uid': 'webclient'});
	    });

    },

    backToHome : function(){
	if(this.currentPoint)
	    this._hidePointInfo(this.currentPoint);
	if(this.currentTrack)
	    this._hideTrackInfo(this.currentTrack);

    },
    
    hide : function(type_name){
	if(this.currentPoint)
	    if(this.currentPoint._data.type_slug == type_name)
		this._hidePointInfo(this.currentPoint);
	if(this.currentTrack)
	    if(this.currentTrack._data.type_slug == type_name)
		this._hideTrackInfo(this.currentTrack);

	$("img."+type_name + ', div.' + type_name).hide();
	for(key in this.elements.tracks){
	    if(key == type_name)
		for(id in this.elements.tracks[key])
		    $(this.elements.tracks[key][id]._container).hide();
	}
    },

    show : function(type_name){
	$("img."+type_name + ', div.' + type_name).show();
	for(key in this.elements.tracks){
	    if(key == type_name)
		for(id in this.elements.tracks[key])
		    $(this.elements.tracks[key][id]._container).show();
	}

    },


    _hidePointInfo : function(point){
	var self = this;
	point.setIcon(point._data.unactiveIcon);
	$(point._icon).css('z-index', $(point._icon).css('z-index')-5000);
	$(point._icon).click(function(){self._showPointInfo(point);});
	$(point._icon).addClass(point._data.type_slug);
	$(point._icon).attr('id', 'iconp-'+point._data.id.toString());

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
	if(!this._runAddPoint){
	if(this.currentPoint)
	    this._hidePointInfo(this.currentPoint);
	if(this.currentTrack)
	    this._hideTrackInfo(this.currentTrack);

	var self = this;
	point.setIcon(point._data.activeIcon);
	$(point._icon).css('z-index', $(point._icon).css('z-index')+5000);
	$(point._icon).click(function(){self._hidePointInfo(point);});
	this.currentPoint = point;


	$('#banner').hide();
	$('#back-to-banner').show();
	$('#type').show();

	var description,
	data = point._data;
	var title = data.title;
	if(data.website)
	    title = '<a target="blank" href="'+data.website+'" style="color:' + data.color + '">'+title+'</a>';
	if(data.post_url)
	    description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	else
	    description = "<p>"+data.description+"</p>";
	var preview = $('.preview-content').html('')
	    .append($("<h1>"+title+"</h1>").css('color', data.color))
	    .append($("<p></p>").html(data.address).addClass('description-address'));
	if(data.images && data.images.length){
	    var imgs_preview = $('<div>').addClass('fotorama').appendTo(preview);
	    for(var imgiter = data.images.length-1; imgiter>=0; imgiter--){
		$('<img/>').attr({'src': data.images[imgiter]})
		    .appendTo(imgs_preview);
	    }
	    $('.fotorama').fotorama({'nav':false});
	}
	preview.append(description);
	if(data.phones)
	    preview.append($("<p></p>").html(data.phones));

	if(typeof __editPointLink != "undefined" &&  __editPointLink != ""){
	    var edit_link = __editPointLink.replace("<%id%>", data.id);
	    $('<p>').append($('<a>').attr('href', edit_link)
		.attr('target', edit_link)
		.text(this.messages['edit']))
		.appendTo(preview);
	}
	preview.parent().show();
	$("#type").html(data.type_name);
	$("#header").css('background-color', data.color);
	var stateObj = { foo: "bar" };
	history.pushState(stateObj, "page", '/'+data.type_slug+"/"+data.uid);	  

	if(typeof DISQUS != 'undefined'){
	    DISQUS.reset({
			     reload: true,
			     config: function () {  
				 this.language = language_code;
				 this.page.identifier = data.uid;  
				 this.page.title = data.title;
				 this.page.url = "http://onbike.by/"+data.type_slug+"/"+data.uid;
			     }
			 });
	    $('#disqus_thread').show();
	}	
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
	$(point._icon).attr('id', 'iconp-'+point._data.id.toString());
	$(point._icon).click(function(){self._showPointInfo(point);});

	//$(point._icon).attr('title', type + ': ' + data.id);

	if(type in this.elements.points){
	    this.elements.points[type][eid] = point;    
	}else{
	    this.elements.points[type] = {};    
	    this.elements.points[type][eid] = point;
	}

	//Если определен текущий элемент
	if(rovar_uid == data.uid)
	    this._showPointInfo(point);

    },
    
    loadPoints : function(){
	var self = this;
	$.ajax({url: '/api/points',
		method: 'GET',
		data: {uid: 'webclient',
		       location: this.location.id},
		success: function(data){
		    for(var i=data.length-1; i>=0; i--){
			self._addPointToMap(data[i]);
		    }
		    var n;
		    for(var key in self.elements.points){
			//n = $('img.'+key).length;
			n = 0;
			for(var tkey in self.elements.points[key])
			    n++;

			if(n){
			    $('#'+key+' .number').text(n);
			    $('#'+key).show();
			}
			else{
			    $('#'+key).hide();
			}
			self._pointGroup(key);
		    }
		    
		    

		    self.map.on('moveend', function(ev){
				    for(var key in self.elements.points){
					self._pointGroup(key);
				    }
				});

		    self.map.on('zoomend', function(ev){
				    for(var key in self.elements.points){
					self._pointGroup(key);
				    }
				});
		}
	       });	
    },


    _hideTrackInfo : function(track){
	var self = this;
	$(track._data.pointA._icon).hide();
	$(track._data.pointB._icon).hide();
	track._container.onclick = function(){self._showTrackInfo(track);};
	track.setStyle({'opacity':0.5});

	$('.preview-content').html('');
	$('.preview').hide();

	var stateObj = { foo: "bar" };
	history.pushState(stateObj, "page", '/');	  

	$('#back-to-banner').hide();
	$('#type').hide();
	$('#banner').show();
	$("#header").css('background-color', "#e95d24");

    },

    _showTrackInfo : function(track){
	if(!this._runAddPoint){
	var self = this;
	if(this.currentPoint)
	    this._hidePointInfo(this.currentPoint);
	if(this.currentTrack)
	    this._hideTrackInfo(this.currentTrack);
	this.currentTrack = track;

	$(track._data.pointA._icon).show();
	$(track._data.pointB._icon).show();
	track._container.onclick = function(){self._hideTrackInfo(track);};
	track.setStyle({'opacity':1});

	$('#banner').hide();
	$('#back-to-banner').show();
        $('#type').show();
	var data = track._data;
	
	var preview = $('.preview-content').html('')
	    .append($("<h1>"+data.title+"</h1>").css('color', data.color));
	if(data.duration)
	    preview.append($("<p></p>").html(this.messages['travel time']+': '+data.duration).addClass('description-address'));
	if(data.video!=''){
	    var video = $(data.video);
	    preview.append(video);
	    //if(preview.width()<preview.find('iframe').width())	    
	}
	var description;
	if(data.post_url)
	    description = "<p><a href=\""+data.post_url+"\">"+data.description+"</a></p>";
	else
	    description = "<p>"+data.description+"</p>";
	preview.append(description);
	preview.parent().show();
	if(typeof video != 'undefined'){
	    video.height(video.height()*(preview.width())/video.width());
	    video.width(preview.width());
	}
	
	$("#type").html(data.type_name);
	$("#header").css('background-color', data.color);


	var stateObj = { foo: "bar" };
	history.pushState(stateObj, "page", '/'+data.type_slug+"/"+data.uid);	  

	if(typeof DISQUS != 'undefined'){
	    DISQUS.reset({
			     reload: true,
			     config: function () {  
				 this.language = language_code;
				 this.page.identifier = data.uid;  
				 this.page.title = data.title;
				 //console.log(this);
				 this.page.url = "http://onbike.by/"+data.type_slug+"/"+data.uid;
			     }
			 });
	    $('#disqus_thread').show();
	}
}
    },

    _addTrackToMap : function(data){
	var self = this;
	var type = data.type_slug;
	var eid = data.id;

	var polyline = L.polyline(data.route, {color: data.color});
	polyline.addTo(this.map);
	polyline._data = data;
	polyline._container.onclick = function(){self._showTrackInfo(polyline);};
	var pointA =new L.Icon({
				   iconUrl: data.marker_a,
				   iconSize: [this._iconSize, this._iconSize],
				   iconAnchor: [this._iconSize*this._kLeft, this._iconSize]
			       });
	var pointB =new L.Icon({
				   iconUrl: data.marker_b,
				   iconSize: [this._iconSize, this._iconSize],
				   iconAnchor: [this._iconSize*this._kLeft, this._iconSize]
			       });
	polyline._data.pointA = L.marker(data.route[0], {color: 'red', icon: pointA});
	polyline._data.pointB = L.marker(data.route[data.route.length-1], {color: 'red', icon: pointB});
	polyline._data.pointA.addTo(rovar.map);
	polyline._data.pointB.addTo(rovar.map);
	$(polyline._data.pointA._icon).hide().click(function(e){self._hideTrackInfo(polyline);});
	$(polyline._data.pointB._icon).hide().click(function(e){self._hideTrackInfo(polyline);});
	


	if(type in this.elements.tracks){
	    this.elements.tracks[type][eid] = polyline;    
	}else{
	    this.elements.tracks[type] = {};    
	    this.elements.tracks[type][eid] = polyline;
	}

	if(rovar_uid == data.uid)
	    this._showTrackInfo(polyline);

    },

    loadTracks : function(){
	var self = this;
	$.ajax({url: '/api/tracks',
		method: 'GET',
		data: {uid: 'webclient',
		       location: this.location.id},
		success: function(data){
		    for(var i=data.length-1; i>=0; i--){
			self._addTrackToMap(data[i]);
		    }
		    var n;
		    for(var key in self.elements.tracks){
			n = 0;
			for(var tkey in self.elements.tracks[key])
			    n++;
			if(n){
			    $('#'+key+' .number').text(n);
			    $('#'+key).show();
			}
			else{
			    $('#'+key).hide();
			}
		    }
		}
	       });	
    },
    


    _pointGroup : function(type_name){
	var i=0, j=0, x0, x1, y0, y1, local_pins, k, p0, p, X, Y, t, id, id0;

	$('div.pingrop-' + type_name).remove();
	$('img.' + type_name).css('visibility', 'visible');
	if(this.map.getZoom() == this.map.getMaxZoom()){
	    return false;
	}

	minX = rovar.map.getBounds()._southWest.lat;
	maxX = rovar.map.getBounds()._northEast.lat;
	var dt = (maxX-minX)/($(this.map._container).width()/(this._iconSize*1.5));
	//var dt = this.location.radius/($(this.map._container).width()/(this._iconSize*1.5));

	var pins = this.elements.points[type_name];
	var minX=60, maxX=50, minY=30, maxY=20, c;
	var color;
	var ids = [];

	for(id0 in pins){
	    pins[id0]._use = false;
	}

	color = pins[id0]._data.color;

	if(!this.sort_ids[type_name]){
	    for(id0 in pins){
		p0 = pins[id0]._data.coordinates;
		c = 0;
		for(id in pins){
		    p = pins[id]._data.coordinates;
		    if(id!=id0 && Math.sqrt((p0[0]-p[0])*(p0[0]-p[0]) + (p0[1]-p[1])*(p0[1]-p[1]))<dt){
			c += 1;
		    }
		}
		if(c>0){
		    ids.push([id0, c]);
		}
	    }
	    ids.sort(function(a,b){return a[1]<b[1];});
	    this.sort_ids[type_name] = ids;
	}
	else{
	    ids = this.sort_ids[type_name];
	}

	for(i = 0; i < ids.length; i++){
	    id0 = ids[i][0];
	    
	    local_pins = [];
	    if(!pins[id0]._use){
		local_pins = [pins[id0]];
		p0 = pins[id0]._data.coordinates;
		pins[id0]._use = true;
		for(id in pins){
		    p = pins[id]._data.coordinates;
		    if(!pins[id]._use && id!=id0 && Math.sqrt((p0[0]-p[0])*(p0[0]-p[0]) + (p0[1]-p[1])*(p0[1]-p[1]))<dt){
			local_pins.push(pins[id]);
			pins[id]._use = true;
		    }
		}
		
		if(local_pins.length>1){
		    X=0; Y=0;
		    for(k=local_pins.length-1; k>=0; k--){
			p = local_pins[k]._data.coordinates;
			X += p[0];
			Y += p[1];
			$(local_pins[k]._icon).css('visibility', 'hidden');
		    }
		    
		    var groupIcon = new L.divIcon({className: type_name + ' pingrop pingrop-' + type_name,
						   html:local_pins.length,
						   iconSize: [this._iconSize*0.66, this._iconSize*0.66],
						   iconAnchor: [this._iconSize*0.66/2, this._iconSize*0.66/2]
						  });
		    X = X/local_pins.length; 
		    Y = Y/local_pins.length;
		    var point = L.marker([X, Y], {color: 'red', icon: groupIcon});
		    point.addTo(this.map);

		    function fn_click(ev){
			var c = ($(this).attr('id').split('-'));
			c = [parseFloat(c[0]), parseFloat(c[1])];
			rovar.map.panTo(c);
			rovar.map.zoomIn(2);
		    }
		    t=[];
		    local_pins.forEach(function(i){t.push(i._data.id);});
		    //$(point._icon).attr('title', type_name + ':' + local_pins.length + ' ' + t.join(','));
		    $(point._icon).attr('id', X.toString() + "-" + Y.toString());
		    
		    $(point._icon).css({'background-color': color,
					'border-radius': "100%",
					'line-height': this._iconSize*0.75 + 'px',
					'color': 'white',
					'vertical-align': 'middle',
					'font-size': this._iconSize*0.75/2 + 'px',
					'font-weight': 'bold',
					'text-align': 'center'
				       });

		    var coordinates = point.getLatLng();
		    $(point._icon).click(fn_click);
		}
		else{
		    $(local_pins[0]._icon).css('visibility', 'visible');
		}
	    }
	}
	if($('#type-btns #'+type_name).attr('class').indexOf('disable')>=0)
	    $("img."+type_name + ', div.' + type_name).hide();
	return true;
    },

    closeAddPoint : function(){	
	$("#add-point-btn").html(this.messages['add point']);
	$("#add-point-dialog").hide();
	$("#ajax-errors").html("");

	$("#map").attr('style', "");
	$('.leaflet-clickable').css('cursor', 'pointer');

	this._runAddPoint = false;
	if(this._addedPoint){
	    this.map.removeLayer(this._addedPoint);
	    this._addedPoint = null;
	}
	    
    },

    addPoint : function(){
	if(!this._runAddPoint){
	    
	this._runAddPoint = true;
	$("#add-point-btn").html(this.messages['set coordinates']);
	var self = this;
	$(this.map._container).css('cursor', "url('/static/icons/pin-add.png') "+(this._iconSize*this._kLeft).toString() + ' ' + (this._iconSize-1).toString() +",crosshair");
	$('.leaflet-clickable').css('cursor', "url('/static/icons/pin-add.png') "+(this._iconSize*this._kLeft).toString() + ' ' + (this._iconSize-1).toString() +",crosshair");
	__addClick = function(e){self._setCoordinates(e);};
	this.map.on('mousedown',__addClick);
	}
    },

    _set_address: function(data){
	var address = (data.address.road || '') + ' ' + (data.address.house_number || '');
	if(address != ' ')
	    $('#add-point-form input[name="address"]').val(address);
	else
	    $('#add-point-form input[name="address"]').val('');
    },

    _setCoordinates: function(e){
	var nosm = document.createElement('script');
	nosm.type = 'text/javascript';
	nosm.async = true;
	nosm.src = 'http://nominatim.openstreetmap.org/reverse?format=json&lat=' + e.latlng.lat.toString() + '&lon=' + e.latlng.lng.toString() + '&zoom=18&addressdetails=1&json_callback=rovar._set_address';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(nosm, s);


	
	var addicon = new L.icon({
					  iconUrl: "/static/icons/pin-add.png",
					  iconSize: [this._iconSize, this._iconSize],
					  iconAnchor: [this._iconSize*this._kLeft, this._iconSize]
				      });

	this._addedPoint = L.marker(e.latlng, {color: 'red', icon: addicon});
	this._addedPoint.addTo(this.map);

	$('input[name="coordinates"]').val('[' + e.latlng.lat.toString() + ', ' + e.latlng.lng.toString() + ']');

	$("#map").attr('style', "");
	$('.leaflet-clickable').css('cursor', 'pointer');

	this.map.off('mousedown', __addClick);
	$("#ajax-errors").html("");
	$("#add-point-dialog .for-clear").val('');
	var d=$("#add-point-dialog").show();
	$("#add-point-dialog input[name=\"title\"]").focus();
	$('#add-point-dialog').animate({'opacity':1}, 500);
	d.css('left', ($(document).innerWidth() - d.innerWidth())/2);
	if(($(document).innerHeight() - d.innerHeight())/2 >= 0)
	    d.css('top', ($(document).innerHeight() - d.innerHeight())/2);
    },


    callbackAddPoint: function(data){
	//console.log(data);
	if(!data.success){
	    $("#ajax-errors").html($("<p class=\"error alert\">").text(this.__errors[data.error_code] || this.messages['unknown error']));
	}else{
	    this._runAddPoint = false;
	    $("#add-point-btn").html(this.messages['add point']);
	    $("#ajax-errors").html($("<p class=\"success alert\">").text(this.messages['success message']));
	    setTimeout("$('#add-point-dialog').animate({'opacity':0.25}, 500, 'swing', function(){$('#add-point-dialog').hide()})", 2000);
	}
    }

};


$(function(){
      rovar.init();
      $("#add-point-btn").click(function(){rovar.addPoint();});
      $("#back-to-banner").click(function(){rovar.backToHome();});
      $("#add-point-form-close").click(function(){rovar.closeAddPoint();});
      $("#add-point-form").ajaxForm(function(data){rovar.callbackAddPoint(data);});

      $("#type-btns li").click(function(ev){
				   var type = this.attributes.id.value;
				   if($(this).attr('class').indexOf('disable')>=0){
				       $(this).removeClass('disable');
				       rovar.show(type);
				   }
				   else{
				       $(this).addClass('disable');
				       rovar.hide(type);
				   }
				   
			       });

      $(document).keyup(function(e) {
			    if (e.keyCode == 27 & rovar._runAddPoint){rovar.closeAddPoint();}
			});
      

  });