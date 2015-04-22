var Player = Class.extend(
    {init: function(video, controlls, data){
	 this.$video = $(video)[0];
	 this.$controlls = $(controlls);
	 this._trackData = data;

	 var self = this;
	 //this.$video[0].onseeked = function(ev){console.log(ev);};
	 //this.$video[0].onseeking = function(ev){console.log(ev);};
	 this.$video.ontimeupdate = function(ev){self._updateTime(ev.srcElement.currentTime);};
	 
	 this.$cPositions = $('<div>').css({'margin': '50px','height': '5px', 'position': 'relative', 'border': 'solid 1px black'}).addClass('player-position').appendTo(this.$controlls).click(function(ev){self._seek(ev.offsetX / $(this).width());});
	 this.$cPositionsCursor = $('<div>').css({'height': '5px', 'width': '5px', 'position': 'absolute', 'background-color': 'black', 'left': 0, 'top': 0}).appendTo(this.$cPositions);
	 
	 
	 

     },
     _updateTime : function(t){
	 console.log(this);
	 console.log(t / this.$video.duration);
	 this.$cPositionsCursor.css('left', (100 * t / this.$video.duration).toString()+'%');
     },

     _seek : function(p){
	  console.log(p * this.$video.duration);
	 this.$video.currentTime = p * this.$video.duration;
     }
     

    });


$(function(){
      var player = new Player('video', '#custom_controlls');
      
});
