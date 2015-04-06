var track_editor = {
  init : function(selector){
      this.$input = $(selector);
      this.$input.hide();

      var self = this;
      var m = $('#editor');
      m.remove();
      this.$input.parent().append(m);
      var form = $('<form action="xml/" method="POST" enctype="multipart/form-data">');
      form.append('<input type="file" name="track-from-xml">');
      form.append('<input type="submit" class="btn" name="get-track-from-xml" value="Загрузить из файла">');
      form.ajaxForm(function(data){if(data){self.load_track(data); self.show();}else{$('#editor-info').text('Произошла ошибка. Попробуйте еще раз.').addClass('error').removeClass('success');};});
      var css = m.find('a:last').offset();
      css['position'] = 'absolute';
      css['left'] += $('#editor a:last').innerWidth() + 50;
      form.css(css);
      
      $('form').parent().append(form);
      
      this.load_track();
      var map = new L.Map('map'), l_name;
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
		  L.tileLayer('//onbike.by/map/tile/{z}/{x}/{y}.png',
			      {attribution: self.copyright,
			       key: 'BC9A493B41014CAABB98F0471D759707',
			       minZoom: 12
			      }).addTo(self.map);
		  self.map.setMaxBounds(self.location.bounds);
		  self.show();
	      }
	     });
  },

    _distance : function(p1,p2){
	return Math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]));
    },
    
    load_track : function(data){
	if(typeof data == 'undefined')
	    data = JSON.parse(this.$input.val());
	this._track = data;
      this._polyline = null;
      this._old_polyline = null;
      var i, dx,
      t = 0;
      this.max_dx = 0;
      for(i = this._track.length - 2; i >= 0; i--){
	  dx = this._distance(this._track[i], this._track[i + 1]);
	  t += dx;
	  if(dx > this.max_dx){
	      this.max_dx = dx;
	  }
      }
      this.middle_dx = t / (this._track.length-1);
    },

    normalize : function(dx){
	var res = [];
	var t = this._track[this._track.length-1], t1=null, t0=null;
	var v1, v2, cos = 0;
	res.push(t);
	for(var i = this._track.length - 2; i >= 0; i--){
	    t1 = this._track[i];
	    if(t != null && t1 != null && t0 != null){
		v1 = [t1[0] - t[0], t1[1] - t[1]];
		v2 = [t[0] - t0[0], t[1] - t0[1]];
		cos = (v1[0] * v2[0] + v1[1] * v2[1]) / (this._distance(v1, [0,0]) * this._distance(v2, [0,0]));
	    };
	    while((this._distance(t1, t) * Math.sqrt(1.0 - cos * cos) < dx ) && i>0){
		i += -1;
		t1 = this._track[i];
		if(t != null && t1 != null && t0 != null){
		    v1 = [t1[0] - t[0], t1[1] - t[1]];
		    v2 = [t[0] - t0[0], t[1] - t0[1]];
		    cos = (v1[0] * v2[0] + v1[1] * v2[1]) / (this._distance(v1, [0,0]) * this._distance(v2, [0,0]));
		};
	    }
	    t0 = t;
	    t = t1;
	    res.push(t);
	}
	this._track = res.reverse();
	this.show();
    },

    show: function(){
	if(this._polyline != null)
	    this.remove();
	this._polyline = L.polyline(this._track, {color: "#ff0000"});
	this._polyline.addTo(this.map);
	
	var point, lpoint;
	this._points = [];
	for(var i = this._track.length - 1; i >= 0; i--){
	    point = new L.LayerGroup();
	    L.circle(this._track[i], 2, {color: "#00ff00"}).addTo(point);
	    this.map.addLayer(point);
	    this._points.push(point);
	}
    },
    
    remove: function(){
	for(var i = this._points.length - 1; i >= 0; i--){
	    this.map.removeLayer(this._points[i]);
	}    
	if(this._polyline != null){
	    this.map.removeLayer(this._polyline);
	}
	this._polyline = null;
    },
    
    write_to_input : function(){
	this.$input.val(JSON.stringify(this._track));
	$('#editor-info').text('Изменения приняты. Нажмите кнопку сохранения(внизу).').removeClass('error').addClass('success');
    }
};

$(function(){track_editor.init('#id_coordinates');});