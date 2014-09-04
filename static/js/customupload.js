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

//var tmp;

o.Image.MAX_RESIZE_HEIGHT = 10000;
o.Image.MAX_RESIZE_WIDTH = 10000;

function MYRESIZE(file, cb){
    var self = this
    , img = new o.Image()
    , url = o.resolveUrl("XMLHttpRequest/poster.jpg")
    ;

    img.onload = function() {
	this.downsize(425, 425, false, false);
    };

    img.onresize = function(e){
	//console.log('resize');

	var blob = img.getAsBinaryString(img.type, 85);
	var a, a8, i;
	a = new ArrayBuffer(blob.length);
	a8 = new Uint8Array(a);
	for(i=blob.length-1; i>=0; i--)
	    a8[i] = blob.charCodeAt(i);
	cb(a8);
    };

    img.onerror = function(e) {
	var blob = img.getAsBinaryString(img.type, 85);
	var a, a8, i;
	a = new ArrayBuffer(blob.length);
	a8 = new Uint8Array(a);
	for(i=blob.length-1; i>=0; i--)
	    a8[i] = blob.charCodeAt(i);
	//cb(a8);
    };


    img.load(file, o.extend({}, self.runtimeOptions, { 
				required_caps: {
				    resize_image: true
				},
				swf_url : '/static/js/moxie/Moxie.swf',
				runtime_order: 'html5,flash',
				container: "mcont"
			    }));
};

(function(){
     var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;
     this.Class = function(){};

     Class.extend = function(prop) {
	 var _super = this.prototype;

	 initializing = true;
	 var prototype = new this();
	 initializing = false;

	 for (var name in prop) {
	     prototype[name] = typeof prop[name] == "function" &&
		 typeof _super[name] == "function" && fnTest.test(prop[name]) ?
		 (function(name, fn){
		      return function() {
			  var tmp = this._super;

			  this._super = _super[name];

			  var ret = fn.apply(this, arguments);
			  this._super = tmp;

			  return ret;
		      };
		  })(name, prop[name]) :
             prop[name];
	 }
	 var bind = function(fn, obj){
	     return function(){
		 return fn.apply(obj, arguments);
	     };
	 };

	 function Class() {
	     if ( !initializing && this.init ) {
		 this.bind = bind(function(fn){
				      return bind(fn, this);
				  }, this);
		 this.init.apply(this, arguments);
	     }
	 }

	 Class.prototype = prototype;

	 Class.prototype.constructor = Class;

	 Class.extend = arguments.callee;

	 return Class;
     };
 })();


CustomUpload = Class.extend(
    {
	files : null,
	host : '',
	api_version : 'v1',
	x_progress : '',

	init : function(box){
	    this.files = {};
	    this.$input = $(box).find('input[type=file]').first();
	    this.$logbox = $(box).find('.logbox').first();
	    this.$input.change(this.bind(this._inputChange));
	    this.$btn = $(box).find('#upload-imgs').first();
	    var ths = this;
	    this.$logbox.bind({dragenter: function() {return false;},
			       dragover: function() {return false;},
			       dragleave: function() {return false;},
			       drop: function(e) {
				   var fl = e.originalEvent.dataTransfer.files;
				   if(fl.length)
				       ths.addFiles(fl);
				   return false;
			       }
			      });
	},

	removeFile : function(target){
	    var file_name = $(target).attr('name');
	    delete this.files[file_name];
	    $(target).remove();
	},

	addFile : function(file){
	    file.id = Math.random().toString().replace('0.', 'img-');
	    file.progress = {'loaded': 0,
			     'total': 10000000};
	    this.files[file.name] = file;
	    var img = $("<img/>").
		attr('name', file.name).
		attr('title', 'Click to remove');
	    var ths = this;
	    img.click(function(){ths.removeFile(img);});
	    img.appendTo(this.$logbox);
	    var reader = new FileReader();			     
	    reader.onload = (function(aImg) {			 				 
				 return function(e) {
				     aImg.attr('src', e.target.result);
				 };
			     })(img);
	    reader.readAsDataURL(file);
	    
	    
	},

	_inputChange : function(){
	    this.addFiles(this.$input[0].files);
	},

	addFiles : function(files){
	    this.files = {};
	    for(var i=files.length-1; i>=0; i--){
		this.addFile(files[i]);
	    }
	},

	_uploaderObject : function(params) {
	    if(!!params.url) {
		//console.log('_uploaderObject1');
		var method;
		//if(!params.method)
		//    method = 'GET';
		//else
		//    method = params.method;
		method = 'POST';
		var self = this;
		var file_name;
		for(f in params.fields)
		    file_name = f;
		//this.list_for_blob
		var description;
		var boundary = "----------xxxxxxxxx";
		if(method=='POST'){
		    if(this.list_for_blob.length == 0){
			self.xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary="+boundary);
			
			for(f in params.data){
			    description='';	
			    description += "--" + boundary + "\r\n";
			    description += "Content-Disposition: form-data; name=\"" + f + "\"\r\n\r\n" + params.data[f] + "\r\n";
			    this.list_for_blob.push(description);
			}
		    }

		    function cd(B){
			
			description='';
			description += "--" + boundary + "\r\n";
			description += "Content-Disposition: form-data; name=\"image\"; filename=\"" + file_name + "\"\r\n";
			description += "Content-Type: application/octet-stream; charset=ascii\r\n\r\n";
			self.list_for_blob.push(description);
			self.list_for_blob.push(B);
			self.list_for_blob.push("\r\n");
			

			//var blob = new Blob(list_for_blob);//,{'type' : 'application/octet-stream'}
			//xhr.send(blob);
			self.numberCompleted ++;
			//console.log('numberCompleted', self.numberCompleted, file_name);
			if(self.numberCompleted==self.numberFiles){
			    var finish_boundary= "\r\n--" + boundary + "--\r\n";
			    self.list_for_blob.push(finish_boundary);
			    var blob = new Blob(self.list_for_blob);//,{'type' : 'application/octet-stream'}
			    self.xhr.send(blob);
			    
			    }
		    }
		    var fr = new FileReader;
		    
		    fr.onload = function(){
			try{
			    MYRESIZE(fr.result, cd);    
			} catch (x) {
			    //var b = atob(fr.result).toString('ascii');
			    //cd(b);
			    self.numberCompleted ++;
			}
			
		    };
		    fr.readAsDataURL(params.fields[file_name]);
		    //readAsDataURL
		}
		else{
		    var blob = null;
		    self.xhr.send(blob);
		}
		
	    }
	},

	_encodeParams: function(params){
	    var str_params = '';
	    for(key in params){
		str_params += encodeURI(key) + '=' + encodeURI(params[key]) + '&';
	    }
	    return str_params;
	},

	_uploadFiles : function(callback, parametrs){
	    /// Отправка всех файлов параллельно, после загрузки файла увеличиваем счетчик загруженных файлов, если количество загруженных совспадает с количеством исходных - выполняем основной callback
	    var p = parametrs;
	    var str_params = this._encodeParams(p);
	    this.numberCompleted = 0;
	    var i=0;for(T in this.files){i++;}
	    this.numberFiles = i;
	    var file_name, fields;
	    $('<div></div>').
		attr('id', 'upload-progress-all').
		addClass('upload-progress').
		appendTo($('#progressbar'));

	    var self = this;
	    this.list_for_blob = [];
	    this.xhr = new XMLHttpRequest();
	    var callbackDefined = callback instanceof Function;
	    var onprogress = this.bind(this.Progress, this);
	    this.xhr.upload.addEventListener("progress", function(e) {
						 if (e.lengthComputable) {
						     self.progress = (e.loaded * 100) / e.total;
						     if(onprogress instanceof Function) {
							 onprogress.call(self,
									 {'loaded': e.loaded,
									  'total': e.total},
									 "");
						     }
						 }
					     }, false);

	    this.xhr.onload = function(){
		if(callbackDefined) {
		    var data = JSON.parse(this.responseText);
		    $('#progressbar').children().remove();
		    if(data.success){
			self.$input.clearInputs();
			self.files = {};
		    }
		    callback.call(self, data);
		}
	    };

	    this.xhr.onreadystatechange = function () {
	    };

	    this.xhr.open("POST", this.host + '/api/point/add');
	    var boundary = "----------xxxxxxxxx";
	    var Nfiles = 0;
	    for(file_name in this.files){
		Nfiles++;
		fields = {};
		fields[file_name] = this.files[file_name];
		this._uploaderObject({url: this.host + '/api/point/add',
				      /*oncomplete: this.bind(function(c){
								this.numberCompleted ++;
								if(this.numberCompleted==this.numberFiles){
								    this.files = {};
								    //this.$btn.text('Upload');
								    callback(c, true);

								    $('.upload-progress').remove();
								}
								else{
								    callback(c, false);	
								}
							    }, this),
	    */
				      //onprogress: this.bind(this.progress, this),
				      fields: fields,
				      method: 'POST',
				      data: parametrs
				     } );		
		
		
	    }
	    
	    if(Nfiles == 0 && this.numberCompleted==self.numberFiles){
		    if(this.list_for_blob.length == 0){
			self.xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary="+boundary);
			var description;
			for(f in parametrs){
			    description='';	
			    description += "--" + boundary + "\r\n";
			    description += "Content-Disposition: form-data; name=\"" + f + "\"\r\n\r\n" + parametrs[f] + "\r\n";
			    this.list_for_blob.push(description);
			}
		    }


		var finish_boundary= "--" + boundary + "--\r\n";
		this.list_for_blob.push(finish_boundary);
		var blob = new Blob(self.list_for_blob);
		this.xhr.send(blob);
	    }

	},

	uploadFiles : function(callback, p){
	    var i=0;for(T in this.files){i++;}
	    //if(i!=0){
		//var p = {'album_id': album_id};
		var str_params = this._encodeParams(p);
		this._uploadFiles(callback, p);
		/*this._uploaderObject({url: this.host + '/photo/start-upload/?'+str_params,
		 oncomplete: this.bind(function(c){this._uploadFiles(callback, c);}, this),
		 fields: {},
		 method: 'GET'
		 } );
		 */
	    //}
	    //else{
	//	callback('');
	 //   }
	},

	Progress : function(p, f){
	    //console.log(p, f);
	    $('#upload-progress-all').css('width', Math.round((p.loaded*100)/p.total) + '%');
	    //this.$btn.html(Math.round((L*100)/T) + '%');
	    /*this.files[f].progress = p;
	    var L = 0;
	    var T = 0;
	    for(file_name in this.files){L += this.files[file_name].progress.loaded;
					 T += this.files[file_name].progress.total;}
	    
	    this.$btn.html(Math.round((L*100)/T) + '%');
	     */
	}
    }
);
