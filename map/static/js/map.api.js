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
var debug = true;

var rovar = {
    elements: {'points': {}, 'tracks': {}},
    sort_ids: {},
    _iconSize: 36,
    _kLeft: 0.317,
    _numberPoint: 0,
    _numberLoadPoint: 0,
    _cache_tpl : {},
    messages: {
        'edit': 'Редактировать',
        'travel time': 'Время в пути',
        'add point': '<i class=\"icon plus\"></i> Добавить точку',
        'set coordinates': 'Выберите место на карте (Esc для отмены)',
        'unknown error': 'Неизвестная ошибка.',
        'success message': 'Ваше предложение будет рассмотрено модератором.',
        'error request method': "Неверный тип запроса.",
        'not init client': "Ваш клиент не инициализирован.",
        'required fields': "Поля 'Название', 'Категория', 'Описание', 'Адрес' являются обязательными.",
        'unknown url': "Указанный тип точки не существует.",
        'required image': "Вы не выбрали изображение или оно не верного формата.",
        'invalide url': "Не верный URL для поля 'Cайт'.",
        'feedback email': "Введите email для обратной связи.",
        'description length': "\"Описание\" не должно превышать 256 символов.",
    },

    _visible_pins: function () {
    },

    init: function () {
        if (typeof rovar_transplate != 'undefined' & typeof language_code != 'undefined') {
            if (typeof rovar_transplate[language_code] != 'undefined') {
                this.messages = rovar_transplate[language_code];
            }
        }

        this.__errors = {
            1: this.messages['error request method'],
            2: this.messages['not init client'],
            3: this.messages['required fields'],
            4: this.messages['unknown url'],
            5: this.messages['required image'],
            6: this.messages['invalide url'],
            7: this.messages['description length'],
            100: this.messages['feedback email']
        };

        var map = new L.Map('map', {zoomControl: false});
        // map.on('click', function(e) {
        // @TODO Добавить проверку на расстояние
        // и если оно больше некой delta выполнять центрирование
        //     map.panTo(new L.LatLng(e.latlng.lat, e.latlng.lng));
        // });
        var self = this;
        map.on('zoomend', function (ev) {
            self._visible_pins();
        });
        this.copyright = '&copy; <a href="//osm.org/copyright">OpenStreetMap</a> contributors';

        var l_name;
        if (typeof rovar_category != 'undefined') {
            this._category = rovar_category;
        } else {
            this._category = '';
        }
        if (typeof rovar_location != 'undefined') {
            l_name = rovar_location;
        } else {
            l_name = 'Minsk';
        }

        $.ajax({
            url: '/api/location',
            method: 'GET',
            data: {name: l_name},
            success: function (data) {
                self.location = data;
                var selected_location = new L.LatLng(self.location.center[0], self.location.center[1]);
                self.map = map.setView(selected_location, 12);
                L.tileLayer('//onbike.by/map/tile/{z}/{x}/{y}.png',
                    {
                        attribution: self.copyright,
                        key: 'BC9A493B41014CAABB98F0471D759707',
                        minZoom: 12
                    }).addTo(self.map);
                self.map.setMaxBounds(self.location.bounds);
                self.loadTypes();
            }
        });

        this.uploader = new CustomUpload($("#inputfile"));
        $('#upload-imgs').click(function (e) {
            e.preventDefault();
            var p = $('[name="phones"]');
            var phones = [];
            for (var i = p.length; i >= 0; i--)
                phones.push($(p[i]).val());
            self.uploader.uploadFiles(function (response, finish) {
                    self.callbackAddPoint(response);
                },
                {
                    'website': $('[name="website"]').val(),
                    'description': $('textarea[name="description"]').val(),
                    'title': $('[name="title"]').val(),
                    'phones': phones,
                    'coordinates': $('[name="coordinates"]').val(),
                    'address': $('[name="address"]').val(),
                    'type': $('[name="type"]').val(),
                    'email': $('[name="email"]').val(),
                    'uid': 'webclient'
                });
        });

    },

    backToHome: function () {
        if (this.currentPoint) {
            this._hidePointInfo(this.currentPoint);
        }
        if (this.currentTrack) {
            this._hideTrackInfo(this.currentTrack);
        }
    },

    close_button: function (obj){
        $('#main-panel-wrapper .preview-content .button_close')
            .unbind("click")
            .on("click", function () {
                switch (obj.type){
                    case "point":{
                        obj.rovar._hidePointInfo(obj);
                        break;
                    }
                    case "track":{
                        obj.rovar._hideTrackInfo(obj);
                        break;
                    }
                }
            });
    },

    fotorama: function (images) {
        if (images && images.length) {
            console.log(images);
            for (var imgiter = images.length - 1; imgiter >= 0; imgiter--) {
                $('.fotorama').append($('<a></a>').attr({'href': images[imgiter]}));
                console.log(imgiter);
            }
            $('.fotorama').fotorama({
                'nav': false,
                'maxheight': '235px',
                'maxwidth': '320px',
                'allowfullscreen': true
            });
        }
    },

    hide: function (type_name) {
        if (this.currentPoint)
            if (this.currentPoint._data.type_slug == type_name) {
                this._hidePointInfo(this.currentPoint);
                this.currentPoint = null;
            }
        if (this.currentTrack)
            if (this.currentTrack._data.type_slug == type_name) {
                this._hideTrackInfo(this.currentTrack);
                this.currentTrack = null;
            }

        var type_counter = parseInt($("#type_counter").html()) || 0;
        var n_counter = parseInt($("#" + type_name + " .Tnumber").html()) || 0;
        $("#type_counter").html(type_counter - n_counter);

        $("img." + type_name + ', div.' + type_name).hide();
        for (key in this.elements.tracks) {
            if (key == type_name)
                for (id in this.elements.tracks[key])
                    this.elements.tracks[key][id].eachLayer(function (l) {
                        $(l._container).hide();
                    });
        }
    },

    show: function (type_name) {
        var type_counter = parseInt($("#type_counter").html()) || 0;
        var n_counter = parseInt($("#" + type_name + " .Tnumber").html()) || 0;
        $("#type_counter").html(type_counter + n_counter);
        $("img." + type_name + ', div.' + type_name).show();
        for (key in this.elements.tracks) {
            if (key == type_name)
                for (id in this.elements.tracks[key])
                    this.elements.tracks[key][id].eachLayer(function (l) {
                        $(l._container).show();
                    });
        }

    },

    _hidePointInfo: function (point) {
        var self = this;
        point.setIcon(point._data.unactiveIcon);
        $(point._icon).css('z-index', $(point._icon).css('z-index') - 5000);
        $(point._icon)
            .unbind("click")
            .click(function (e) {
                self._showPointInfo(point);
            });
        $(point._icon).addClass(point._data.type_slug);
        $(point._icon).attr('id', 'iconp-' + point._data.id.toString());

        $('.preview-content').html('');
        $('.preview').hide();

        var stateObj = {foo: "bar"};
        history.pushState(stateObj, "page", '/' + this.location.name);

        var rbgCol = '#e95d24';
        var rgbaCol = 'rgba(' + parseInt(rbgCol.slice(-6, -4), 16)
            + ',' + parseInt(rbgCol.slice(-4, -2), 16)
            + ',' + parseInt(rbgCol.slice(-2), 16)
            + ', 0.9)';
        $('#main-header').css('background-color', rgbaCol);

    },

    _showPointInfo: function (point) {
        if (!this._runAddPoint) {
            if (this.currentPoint) {
                this._hidePointInfo(this.currentPoint);
            }
            if (this.currentTrack) {
                this._hideTrackInfo(this.currentTrack);
            }

            var self = this;
            point.setIcon(point._data.activeIcon);
            $(point._icon).css('z-index', $(point._icon).css('z-index') + 5000);
            $(point._icon)
                .unbind("click")
                .click(function () {
                    self._hidePointInfo(point);
                });

            point.type = 'point';
            point.rovar = self;
            this.currentPoint = point;

            var preview = $('.preview-content').html('');

            // preparing data
            var description,
                data = point._data;
            var title = data.title;
            if (data.website) {
                title = '<a target="blank" href="' + data.website + '" style="color:' + data.color + '">' + title + '</a>';
            }

            if (data.comments_count > 0) {
                data['message_comment_string'] = this.messages['comment number'] + data.comments_count;
            } else {
                data['message_comment_string'] = this.messages['comment first'];
            }

            if (data.phones){
                data.array_phones = data.phones.split(",");
            }

            if (data.post_url) {
                data['description'] = "<a href=\"" + data.post_url + "\">" + data.description + "</a>";
            } else {
                data['description'] = data.description;
            }

            // generate popup (target, template name == type object, data, callbacks)
            this.loadTpl(".preview-content", point.type, data, [
                {
                    func: this.fotorama,
                    params: data.images
                },
                {
                    func: this.close_button,
                    params: point
                }
            ]);

            var entryID = data.id; // currentPoint.id
            var rating_get = $.ajax({
                    url: "/api/ratings",
                    method: "GET",
                    data: {
                        entry_id: entryID,
                        entry_type: "Point" // @TODO научиться принимать разные сущности
                    },
                    dataType: "json"
                })
                .done(function (data) {
                    var initialRating = data.initialRating, maxRating = data.maxRating;
                    if (data.is_auth) {
                        $('.ui.rating').rating({
                            initialRating: initialRating,
                            maxRating: maxRating,
                            onRate: function (value) {
                                var $this = $(this);
                                //Проверка на инициализацию
                                //Если ещё не установлен флаг
                                if ($this.hasClass('initial' + entryID)) {

                                    var rating_post = $.ajax({
                                            url: "/api/ratings",
                                            type: "POST",
                                            data: {
                                                "entry_id": entryID,
                                                "entry_type": "Point", // @TODO научиться принимать разные сущности
                                                "value": value
                                            },
                                            dataType: "json"
                                        })
                                        .done(function (data) {
                                            alert("Cпасибо, ваш голос учтён!");
                                        })
                                        .fail(function (jqXHR, textStatus) {
                                            alert("Request failed: " + textStatus);
                                        });
                                } else {
                                    $this.addClass('initial' + entryID)
                                }
                            }
                        });
                    } else {
                        $('.ui.rating').rating({
                            initialRating: initialRating,
                            maxRating: maxRating
                        }).rating('disable');
                    }
                })
                .fail(function (jqXHR, textStatus) {
                    alert("Request failed: " + textStatus);
                });

            if (typeof __editPointLink != "undefined" && __editPointLink != "") {
                var edit_link = __editPointLink.replace("<%id%>", data.id);
                $('<p>').append($('<a>').attr('href', edit_link)
                    .attr('target', edit_link)
                    .text(this.messages['edit']))
                    .appendTo(preview);
            }
            preview.parent().show();
            // $("#type").html(data.type_name);
            var rbgCol = data.color;
            var rgbaCol = 'rgba(' + parseInt(rbgCol.slice(-6, -4), 16)
                + ',' + parseInt(rbgCol.slice(-4, -2), 16)
                + ',' + parseInt(rbgCol.slice(-2), 16)
                + ', 0.9)';
            $('#main-header').css('background-color', rgbaCol);

            var stateObj = {foo: "bar"};
            history.pushState(stateObj, "page", data.url);

        }
    },

    _addPointToMap: function (data) {
        var self = this;
        var type = data.type_slug;
        var eid = data.id;
        data.unactiveIcon = new L.icon({
            iconUrl: data.marker_a,
            iconSize: [this._iconSize, this._iconSize],
            iconAnchor: [this._iconSize * this._kLeft, this._iconSize / 2]
        });
        data.activeIcon = new L.icon({
            iconUrl: data.marker_b,
            iconSize: [this._iconSize, this._iconSize],
            iconAnchor: [this._iconSize * this._kLeft, this._iconSize]
        });

        var point = L.marker(data.coordinates, {color: 'red', icon: data.unactiveIcon});
        point._data = data;
        point.addTo(this.map);
        $(point._icon).addClass(type);
        $(point._icon).attr('id', 'iconp-' + point._data.id.toString());
        $(point._icon).click(function () {
            self._showPointInfo(point);
        });

        //$(point._icon).attr('title', type + ': ' + data.id);

        if (type in this.elements.points) {
            this.elements.points[type][eid] = point;
        } else {
            this.elements.points[type] = {};
            this.elements.points[type][eid] = point;
        }

        //Если определен текущий элемент
        if (rovar_uid == data.uid)
            this._showPointInfo(point);

    },

    loadTypes: function () {
        var self = this;
        $.ajax({
            url: '/api/types',
            method: 'GET',
            data: {uid: 'webclient'},
            success: function (data) {
                for (var i = data.length - 1; i >= 0; i--)
                    self.loadObject(data[i].object, data[i].text_id, data[i]);

                self.map.on('moveend', function (ev) {
                    for (var key in self.elements.points) {
                        self._pointGroup(key);
                    }
                });

                self.map.on('zoomend', function (ev) {
                    for (var key in self.elements.points) {
                        self._pointGroup(key);
                    }
                });

            }
        });
    },

    loadObject: function (object_name, type_id, type_params) {
        var self = this;
        $.ajax({
            url: '/api/' + object_name + 's',
            method: 'GET',
            data: {
                uid: 'webclient',
                location: this.location.id,
                type: type_id
            },
            success: function (data) {
                var arg;
                for (var i = data.length - 1; i >= 0; i--) {
                    arg = data[i];
                    arg.color = type_params.color;
                    arg.marker_a = type_params.marker_a;
                    arg.marker_b = type_params.marker_b;
                    arg.type_name = type_params.name;
                    if (object_name == 'point') {
                        self._addPointToMap(arg);
                    } else {
                        self._addTrackToMap(arg);
                    }
                }
                var n = data.length;
                if (n) {
                    $('#' + type_id + ' .Tnumber').text(n);

                    var type_counter = parseInt($("#type_counter").html()) || 0;
                    $("#type_counter").html(type_counter + n);

                    $('#' + type_id).show();
                } else {
                    $('#' + type_id).hide();
                }

                if (self._category && self._category != type_id) {
                    $('#' + type_id).addClass('disable');
                    rovar.hide(type_id);
                }

                if (object_name == 'point' && data.length > 0) {
                    self._pointGroup(type_id);
                }
            }
        });
    },

    loadTpl: function (target, tplname, data, callbacks) {

        var self = this;
        var callback = function(template){
            var rendered = Jinja.render(template, data);
            $(target).html(rendered);
            callbacks.forEach(function(item, i, arr){
                item.func(item.params);
            });
        }

        if(!this._cache_tpl[tplname]){
            $.get("/tpl/"+tplname, function(template) {
                self._cache_tpl[tplname] = template;
                callback(template);
            });
        }else{
            var template = self._cache_tpl[tplname];
            callback(template);
        };

    },

    _hideTrackInfo: function (track) {
        var self = this;
        $(track._data.pointA._icon).hide();
        $(track._data.pointB._icon).hide();

        $('.preview-content').html('');
        $('.preview').hide();

        var stateObj = {foo: "bar"};
        history.pushState(stateObj, "page", '/' + this.location.name);

        var rbgCol = '#e95d24';
        var rgbaCol = 'rgba(' + parseInt(rbgCol.slice(-6, -4), 16)
            + ',' + parseInt(rbgCol.slice(-4, -2), 16)
            + ',' + parseInt(rbgCol.slice(-2), 16)
            + ', 0.9)';
        $('#main-header').css('background-color', rgbaCol);

    },

    _showTrackInfo: function (track) {
        if (!this._runAddPoint) {
            var self = this;
            if (this.currentPoint)
                this._hidePointInfo(this.currentPoint);
            if (this.currentTrack)
                this._hideTrackInfo(this.currentTrack);

            track.type = 'track';
            track.rovar = self;
            this.currentTrack = track;

            $(track._data.pointA._icon).show();
            $(track._data.pointB._icon).show();

            var data = track._data;

            console.log(data);

            var preview = $('.preview-content').html('');

            // preparing data
            if (data.comments_count > 0) {
                data['message_comment_string'] = this.messages['comment number'] + data.comments_count;
            } else {
                data['message_comment_string'] = this.messages['comment first'];
            }

            if (data.post_url) {
                data['description'] = "<a href=\"" + data.post_url + "\">" + data.description + "</a>";
            } else {
                data['description'] = data.description;
            }

            data['message_travel_time'] = this.messages['travel time'];

            // generate popup (target, template name, data, callbacks)
            this.loadTpl(".preview-content", track.type, data, [
                {
                    func: this.close_button,
                    params: track
                }
            ]);

            preview.parent().show();

            var rbgCol = data.color;
            var rgbaCol = 'rgba(' + parseInt(rbgCol.slice(-6, -4), 16)
                + ',' + parseInt(rbgCol.slice(-4, -2), 16)
                + ',' + parseInt(rbgCol.slice(-2), 16)
                + ', 0.9)';
            $('#main-header').css('background-color', rgbaCol);

            var stateObj = {foo: "bar"};
            history.pushState(stateObj, "page", data.url);

        }
    },

    _hex_to_rgba: function (h) {
        var c;
        if (h[0] == '#')
            c = h.substr(1);
        else
            c = h;
        if (c.length == 3) {
            c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
        }
        var i = parseInt(c, 16);
        return [parseInt(i / 256 / 256), parseInt(i / 256) % 256, i % 256];
    },

    _rgba_to_hex: function (c) {
        return '#' + c.map(function (d) {
                return (0xFFFFFFFF + parseInt(d) + 1).toString(16).toUpperCase().substr(7);
            }).join('');
    },

    _addTrackToMap: function (data) {
        var self = this;
        var type = data.type_slug;
        var eid = data.id;

        var rgbacolor = self._hex_to_rgba(data.color);
        //var polyline = L.polyline(data.route, {color: data.color});

        var yourGeoJSON = [];
        var t, t1;
        var maxele = 305, minele = 212, v1, v2, cos = 0;
        for (var ii = 0; ii < data.route.length - 2; ii++) {
            t = data.route[ii];
            t1 = data.route[ii + 1];

            /*while(Math.sqrt( (t[1]-t1[1])*(t[1]-t1[1]) + (t[0]-t1[0])*(t[0]-t1[0]) ) < 0.0003 & ii < data.route.length-1){
             ii += 1;
             t1 = data.route[ii];
             }*/
            //if((t[3]|0)<minele)minele = t[3]|0;
            //if((t[3]|0)>maxele)maxele = t[3]|0;
            //t1 = [t[0] + (t1[0]-t[0])*0.9 , t[1] + (t1[1]-t[1])*0.9 ];
            yourGeoJSON.push({
                "type": "Feature",
                "properties": {"id": ii, "elevation": t[3] | 0},
                "geometry": {"type": "LineString", "coordinates": [[t[1], t[0]], [t1[1], t1[0]]]}
            });
        }
        //var self = this;
        var polyline = L.geoJson(yourGeoJSON, {
            'color': data.color,
            'weight': 4,
            'opacity': 1,
            'smoothFactor': 2
            /*
             style: function (feature) {
             if(feature.properties.elevation > 0)
             return {
             color : self._rgba_to_hex(rgbacolor.map(function(x){return (x + (255 - x) * (feature.properties.elevation - minele)/(maxele - minele));}))
             };
             else
             return {
             "color": data.color
             };

             }*/
        });

        polyline.addTo(this.map);
        polyline._data = data;
        polyline.on('click', function () {
            self._showTrackInfo(polyline);
        });
        var pointA = new L.Icon({
            iconUrl: data.marker_a,
            iconSize: [this._iconSize, this._iconSize],
            iconAnchor: [this._iconSize * this._kLeft, this._iconSize]
        });
        var pointB = new L.Icon({
            iconUrl: data.marker_b,
            iconSize: [this._iconSize, this._iconSize],
            iconAnchor: [this._iconSize * this._kLeft, this._iconSize]
        });
        polyline._data.pointA = L.marker(data.route[0], {color: 'red', icon: pointA});
        polyline._data.pointB = L.marker(data.route[data.route.length - 1], {color: 'red', icon: pointB});
        polyline._data.pointA.addTo(rovar.map);
        polyline._data.pointB.addTo(rovar.map);
        $(polyline._data.pointA._icon).hide().click(function (e) {
            self._hideTrackInfo(polyline);
        });
        $(polyline._data.pointB._icon).hide().click(function (e) {
            self._hideTrackInfo(polyline);
        });


        if (type in this.elements.tracks) {
            this.elements.tracks[type][eid] = polyline;
        } else {
            this.elements.tracks[type] = {};
            this.elements.tracks[type][eid] = polyline;
        }

        if (rovar_uid == data.uid)
            this._showTrackInfo(polyline);

    },

    _pointGroup: function (type_name) {
        var i = 0, j = 0, x0, x1, y0, y1, local_pins, k, p0, p, X, Y, t, id, id0;

        $('div.pingrop-' + type_name).remove();
        $('img.' + type_name).css('visibility', 'visible');
        if (this.map.getZoom() == this.map.getMaxZoom()) {
            return false;
        }

        minX = rovar.map.getBounds()._southWest.lat;
        maxX = rovar.map.getBounds()._northEast.lat;
        var dt = (maxX - minX) / ($(this.map._container).width() / (this._iconSize * 2.0));
        //var dt = this.location.radius/($(this.map._container).width()/(this._iconSize*1.5));

        var pins = this.elements.points[type_name];
        var minX = 60, maxX = 50, minY = 30, maxY = 20, c;
        var color;
        var ids = [];

        for (id0 in pins) {
            pins[id0]._use = false;
        }

        color = pins[id0]._data.color;

        if (!this.sort_ids[type_name]) {
            for (id0 in pins) {
                p0 = pins[id0]._data.coordinates;
                c = 0;
                for (id in pins) {
                    p = pins[id]._data.coordinates;
                    if (id != id0 && Math.sqrt((p0[0] - p[0]) * (p0[0] - p[0]) + (p0[1] - p[1]) * (p0[1] - p[1])) < dt) {
                        c += 1;
                    }
                }
                if (c > 0) {
                    ids.push([id0, c]);
                }
            }
            ids.sort(function (a, b) {
                return a[1] < b[1];
            });
            this.sort_ids[type_name] = ids;
        }
        else {
            ids = this.sort_ids[type_name];
        }

        for (i = 0; i < ids.length; i++) {
            id0 = ids[i][0];

            local_pins = [];
            if (!pins[id0]._use) {
                local_pins = [pins[id0]];
                p0 = pins[id0]._data.coordinates;
                pins[id0]._use = true;
                for (id in pins) {
                    p = pins[id]._data.coordinates;
                    if (!pins[id]._use && id != id0 && Math.sqrt((p0[0] - p[0]) * (p0[0] - p[0]) + (p0[1] - p[1]) * (p0[1] - p[1])) < dt) {
                        local_pins.push(pins[id]);
                        pins[id]._use = true;
                    }
                }

                if (local_pins.length > 1) {
                    X = 0;
                    Y = 0;
                    for (k = local_pins.length - 1; k >= 0; k--) {
                        p = local_pins[k]._data.coordinates;
                        X += p[0];
                        Y += p[1];
                        if (local_pins[k] != this.currentPoint)
                            $(local_pins[k]._icon).css('visibility', 'hidden');
                    }

                    var groupIcon = new L.divIcon({
                        className: type_name + ' pingrop pingrop-' + type_name,
                        html: local_pins.length,
                        iconSize: [this._iconSize * 0.66, this._iconSize * 0.66],
                        iconAnchor: [this._iconSize * 0.66 / 2, this._iconSize * 0.66 / 2]
                    });
                    X = X / local_pins.length;
                    Y = Y / local_pins.length;
                    var point = L.marker([X, Y], {color: 'red', icon: groupIcon});
                    point.addTo(this.map);

                    function fn_click(ev) {
                        var c = ($(this).attr('id').split('-'));
                        c = [parseFloat(c[0]), parseFloat(c[1])];
                        rovar.map.panTo(c);
                        rovar.map.zoomIn(2);
                    }

                    t = [];
                    local_pins.forEach(function (i) {
                        t.push(i._data.id);
                    });
                    //$(point._icon).attr('title', type_name + ':' + local_pins.length + ' ' + t.join(','));
                    $(point._icon).attr('id', X.toString() + "-" + Y.toString());

                    $(point._icon).css({
                        'background-color': color,
                        'border-radius': "100%",
                        'line-height': this._iconSize * 0.75 + 'px',
                        'color': 'white',
                        'vertical-align': 'middle',
                        'font-size': this._iconSize * 0.75 / 2 + 'px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    });

                    var coordinates = point.getLatLng();
                    $(point._icon).click(fn_click);
                }
                else {
                    $(local_pins[0]._icon).css('visibility', 'visible');
                }
            }
        }
        if ($('#type-btns #' + type_name).hasClass('disable')) {
            $("img." + type_name + ', div.' + type_name).hide();
        }
        return true;
    },

    closeAddPoint: function () {
        this._runAddPoint = false;
        $("#add-point-btn-text").html(this.messages['add point']);
        $("#add-point-btn").parent().removeClass("hover");
        $("#add-point-dialog").modal("hide");
        $("#ajax-errors").html("");

        $("#map").attr('style', "");
        $('.leaflet-clickable').css('cursor', 'pointer');

        if (this._addedPoint) {
            this.map.removeLayer(this._addedPoint);
            this._addedPoint = null;
        }
    },

    addPoint: function () {
        if (!this._runAddPoint) {

            this._runAddPoint = true;
            $("#add-point-btn-text").html(this.messages['set coordinates']);
            $("#add-point-btn").parent().addClass("hover");

            var self = this;
            $(this.map._container).css('cursor', "url('/static/icons/pin-add.png') " + (this._iconSize * this._kLeft).toString() + ' ' + (this._iconSize - 1).toString() + ",crosshair");
            $('.leaflet-clickable').css('cursor', "url('/static/icons/pin-add.png') " + (this._iconSize * this._kLeft).toString() + ' ' + (this._iconSize - 1).toString() + ",crosshair");
            __addClick = function (e) {
                self._setCoordinates(e);
            };
            this.map.on('mousedown', __addClick);
        }
    },

    _set_address: function (data) {
        var address = (data.address.road || '') + ' ' + (data.address.house_number || '');
        if (address != ' ')
            $('#add-point-form input[name="address"]').val(address);
        else
            $('#add-point-form input[name="address"]').val('');
    },

    _setCoordinates: function (e) {
        var nosm = document.createElement('script');
        nosm.type = 'text/javascript';
        nosm.async = true;
        nosm.src = '//nominatim.openstreetmap.org/reverse?format=json&lat=' + e.latlng.lat.toString() + '&lon=' + e.latlng.lng.toString() + '&zoom=18&addressdetails=1&json_callback=rovar._set_address';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(nosm, s);


        var addicon = new L.icon({
            iconUrl: "/static/icons/pin-add.png",
            iconSize: [this._iconSize, this._iconSize],
            iconAnchor: [this._iconSize * this._kLeft, this._iconSize]
        });

        this._addedPoint = L.marker(e.latlng, {color: 'red', icon: addicon});
        this._addedPoint.addTo(this.map);

        $('input[name="coordinates"]').val('[' + e.latlng.lat.toString() + ', ' + e.latlng.lng.toString() + ']');

        $("#map").attr('style', "");
        $('.leaflet-clickable').css('cursor', 'pointer');

        this.map.off('mousedown', __addClick);
        $("#ajax-errors").html("");
        $("#add-point-dialog .for-clear").val('');
        var d = $("#add-point-dialog");
        d.modal({blurring: true}).modal("show");
        $("#add-point-dialog input[name=\"title\"]").focus();
        $('#add-point-dialog').animate({'opacity': 1}, 500);
        d.css('left', ($(document).innerWidth() - d.innerWidth()) / 2);
        if (($(document).innerHeight() - d.innerHeight()) / 2 >= 0)
            d.css('top', ($(document).innerHeight() - d.innerHeight()) / 2);
    },

    callbackAddPoint: function (data) {
        if (!data.success) {
            $("#ajax-errors").html($("<p class=\"error alert\">").text(this.__errors[data.error_code] || this.messages['unknown error']));
        } else {
            this._runAddPoint = false;
            $("#add-point-btn-text").html(this.messages['add point']);
            $("#add-point-btn").parent().removeClass("hover");
            $("#ajax-errors").html($("<p class=\"success alert\">").text(this.messages['success message']));
            setTimeout("$('#add-point-dialog').animate({'opacity':0.25}, 500, 'swing', function(){$('#add-point-dialog').modal('hide')})", 2000);
        }
    }

};


$(function () {

    if ($("#map").length) {
        rovar.init();
    };

    $("#add-point-btn").click(function (e) {
        e.preventDefault();
        if (rovar._runAddPoint) {
            rovar.closeAddPoint();
        } else {
            rovar.addPoint();
        }
    });

    $("#add-point-form-close, #form-close").click(function (e) {
        e.preventDefault();
        rovar.closeAddPoint();
    });

    $("#add-point-form").ajaxForm(function (data) {
        rovar.callbackAddPoint(data);
    });

    $("#type-btns li").click(function (ev) {
        var type = this.attributes.id.value;
        var stateObj = {foo: "bar"};
        if (/\/\w+\/[\w\-]+\/$/.test(window.location.href)) {
            history.pushState(stateObj, "page", '..');
        }
        console.log(type);
        if ($(this).hasClass('disable')) {
            $(this).removeClass('disable');
            rovar.show(type);
        } else {
            $(this).addClass('disable');
            rovar.hide(type);
        }
    });

    $(document).keyup(function (e) {
        if (e.keyCode == 27 && rovar._runAddPoint) {
            rovar.closeAddPoint();
        }
    });

});