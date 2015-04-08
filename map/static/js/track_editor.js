var track_editor = {
  init : function(selector){
      this.$input = $(selector);
      this.$input.hide();
      this._points = [];
      this._track_history = [];

      this._state = '';
      this._current_point = null;
      this._edit_line = null;

      var self = this;
      var m = $('#editor');
      m.remove();
      this.$input.parent().append(m);
      m.css('position','relative');

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
      $('#map').css('cursor', 'crosshair');

      this.$mode = $('<div>').css({'position': 'absolute','left':'50px','top':'20px'}).appendTo(m);
      $('<a href="javascript:;" class="btn">Удаление точек</a>').prependTo(this.$mode).css('margin','5px').click(function(ev){if($(this).attr('class').indexOf('success') >=0){$(this).removeClass('success');self._state='';}else{$(this).addClass('success');self._state='delete';}});
      $('<a href="javascript:;" class="btn">Отменить поледнее действие</a>').prependTo(this.$mode).css('margin','5px').click(function(ev){self._undo_last_action();});


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

		  self.map.on('mousemove', function(ev){if(self._state == 'move'){self.show_move_point(self._current_point._index, ev.latlng);}});
		  self.map.on('mouseup', function(ev){if(self._state == 'move'){self._current_point = null;self._state=''; self._push_history();self.show();}});
		  self.map.on('click', function(ev){self.insert_point(ev.latlng);});
	      }
	     });

      
  },

    _push_history : function(){
	if(this._track_history.length > 100){
	    this._track_history.splice(0, 1);
	}
	var t = this._track.slice();
	this._track_history.push(t);
    },
    
    _undo_last_action : function(){
	if(this._track_history.length > 1)
	    this._track_history.pop();
	if(this._track_history.length > 0){
	    var t = this._track_history[this._track_history.length-1];
	    this._track = t.slice();
	    this.show();
	}
    },

    insert_point : function(data){
	var p = [data.lat, data.lng];
	var minh = 1000, h, d, k = -1, t1,t2, v1,v2,v3,cosa, cosb;
	for(var i=this._track.length - 1; i > 0; i--){
	    t1 = this._track[i];
	    t2 = this._track[i-1];
	    if(this._distance(t1, t2) > 0){
		v1 = [-t1[0] + p[0], -t1[1] + p[1]];
		v2 = [t2[0] - t1[0], t2[1] - t1[1]];
		v3 = [t2[0] - p[0], t2[1] - p[1]];
		cosa = (v1[0] * v2[0] + v1[1] * v2[1]) / this._distance(p, t1) / this._distance(t1, t2);
		cosb = (v2[0] * v3[0] + v2[1] * v3[1]) / this._distance(t1, t2) / this._distance(p, t2);
		h = this._distance(p, t1) * Math.sqrt(1 - cosa * cosa);
		d = this._distance(p,t1);
		if(h<minh && cosa * cosb > 0 || d<minh){
		    if(cosa * cosb > 0)
			minh = h;
		    else
			minh = d;
		    k = i;
		}
	    }
	}
	if(k == -1){
	    t1 = this._track[0];
	    t2 = this._track[this._track.length - 1];
	    if(this._distance(t1,p) < this._distance(t2,p)){
		k = 0;
		}
	    else{
		k = this._track.length;
	    }
	}
	this._track.splice(k, 0, [p[0], p[1], this._track[k][2], this._track[k][3]]);
	this._push_history();
	this.show();
    },

    show_move_point : function(i, c){
	if(this._edit_line!=null){
	    this.map.removeLayer(this._edit_line);
	}
	this._track = this._track.slice();
	this._track[i] = [c.lat, c.lng, this._track[i][2], this._track[i][3]];
	if(0<i<this._track.length-1){	    
	    var l = [this._track[i-1], this._track[i] , this._track[i+1]];
	    this._edit_line = L.polyline(l, {color: "#0000ff"});
	    this._edit_line.addTo(this.map);
	}	    
    },

    remove_point : function(i){
	this._track.splice(this._points[i]._index, 1);
	this._push_history();
	this.show();
    },

    _distance : function(p1,p2){
	return Math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]));
    },
    
    load_track : function(data){
	if(typeof data == 'undefined')
	    data = JSON.parse(this.$input.val());
	this._track = data;
	this.remove();
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
      this._push_history();
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
	this._push_history();
	this.show();
    },

    show: function(){
	if(this._polyline != null)
	    this.remove();
	this._polyline = L.polyline(this._track, {color: "#ff0000"});
	this._polyline.addTo(this.map);
	
	var point, lpoint, self=this;
	this._points = {};
	for(var i = this._track.length - 1; i >= 0; i--){
	    lpoint = new L.LayerGroup();
	    point = L.circle(this._track[i], 2, {color: "#00ff00"}).addTo(this.map);
	    point.on('mousedown', function(ev){if(self._state == 'delete'){self.remove_point(ev.target._leaflet_id);}else{self._current_point = self._points[ev.target._leaflet_id];self._state='move';}});
	    point._index = i;
	    this._points[point._leaflet_id] = point;
	}
    },
    
    remove: function(){
	for(var i in this._points){
	    this.map.removeLayer(this._points[i]);
	}    
	if(this._polyline != null){
	    this.map.removeLayer(this._polyline);
	}
	if(this._edit_line!=null){
	    this.map.removeLayer(this._edit_line);
	}

	this._polyline = null;
    },
    
    write_to_input : function(){
	this.$input.val(JSON.stringify(this._track));
	$('#editor-info').text('Изменения приняты. Нажмите кнопку сохранения(внизу).').removeClass('error').addClass('success');
    }
};

$(function(){track_editor.init('#id_coordinates');});