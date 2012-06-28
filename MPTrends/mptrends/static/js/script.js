var MPTREND = MPTREND || {};

MPTREND.map = {
	//should be one off initialising for this first bit
	mapObj: undefined,
	infowindow: undefined,
	markersArray: [],
	jsonUrl: '/code/demo',
	currentAjaxRequest: undefined,
	currentOverlay: undefined,
	filter: {
        mp: {
            clusterImage: [{
                url: '/site/img/map_icons/mp_30x30.png',
                height: 31,
                width: 30,
                anchor: [5],
                textColor: '#002776',
                textSize: 12
            }, {
                url: '/site/img/mp_30x30.png',
                height: 35,
                width: 32,
                anchor: [7],
                textColor: '#002776',
                textSize: 12
            }, {
                url: '/site/img/map_icons/mp_45x45.png',
                height: 45,
                width: 45,
                anchor: [11],
                textColor: '#002776',
                textSize: 12
            }],
            markerImageURL: "/site/img/map_icons/mp.png",
            markerImageWidth: 40,
            markerImageHeight: 38,
            markerAnchorX: 20,
            markerAnchorY: 47,
            clusterMaxZoom: 11,
            clusterGridSize: 80,
            jsontTemplate: {
                "self": "{container}",
                "container": "<h2>{$.name}</h2><p>{$.context}</p>"
            }
        }
	},

	mapOptions: {
	  zoom: 2,
	  center: new google.maps.LatLng(53, -3.0),
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	},

	init: function () {

		//if available, set geoLocation, otherwise defaults will display
		this.getGeoLocation();
		//draw the map
		this.mapObj = new google.maps.Map(document.getElementById('map'), this.mapOptions);
		//this.getEntities();
	},
	
	getGeoLocation: function () {
		//if geoLocation is, set default location
		var self = this, infowindow = undefined;
		
		if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(function(position) {
				self.mapOptions.zoom = 3;
			    self.mapOptions.center = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
			    //display default message - although, if they are members we could welcome them back?
			    infowindow = new google.maps.InfoWindow({
			      map: self.mapObj,
			      position: self.mapOptions.center,
			      content: "Your location"
			    });
				self.currentOverlay	= infowindow;
			});
			return true;
		}
		return false;
	},
	
	getEntities: function (mpid) {

		this.clearMarkers();
		
		mpid = mpid || '10251';
		fullJsonUrl = this.jsonUrl + '?mp=' + mpid;
		var self = this;
        // do Ajax to put in cache
        this.currentAjaxRequest = $.ajax({
			url: fullJsonUrl,
			dataType: "json",
            success: function (jsonData) {
                for (var i in jsonData) {
                	var latlng = new google.maps.LatLng(jsonData[i].latitude, jsonData[i].longitude);
					var title = jsonData[i].name + jsonData[i].context;
					var marker = new google.maps.Marker({
					  position: latlng,
					  icon: self.filter['mp'].markerImageURL,
					  map: self.mapObj,
					  title: title
					});

					(function (mymarker, mylatlng) {
					
						var infowindow = new google.maps.InfoWindow({
							content: jsonT({container: jsonData[i]}, MPTREND.map.filter.mp.jsontTemplate),
							position: mylatlng
						});
						
						google.maps.event.addListener(marker, 'click', function() {
							self.clearOverlays();
							infowindow.open(self.mapObj,mymarker);
							self.mapObj.panTo(mylatlng);
							self.currentOverlay	= infowindow;
						});				
					
					})(marker, latlng);

					self.markersArray.push(marker);		

				}
            }
        });
	},

	attachEvents: function () {
		var self = this;
        // click Google Maps event for map canvas to clear all overlays
        google.maps.event.addListener(this.mapObj, 'click', function () {
			self.clearOverlays();
        });
	},
	
	//only one overlay should be displayed
	clearOverlays: function () {
		var self = this;
		if (self.currentOverlay.setMap) {
		    self.currentOverlay.setMap(null);
		}
	},

	clearMarkers: function () {
		if (this.markersArray) {
			for (var i = 0; i < this.markersArray.length; i++ ) {
				this.markersArray[i].setMap(null);
			}
		}
	}

};

MPTREND.getMPs = function () {

    var ajaxRequest = $.ajax({
		url: '/static/mplist.json',
		dataType: "json",

        success: function (jsonData) {
        
        	$('#mps').empty();
            for (var i in jsonData) {
				var s = $('<a id="'+ jsonData[i].person_id +'">' + jsonData[i].name + '</a>').bind('click', clickHandler);
				$('#mps').append(s);

				if(i > 20) break;
			}
        }
    });
	
}

function clickHandler() {
	MPTREND.map.getEntities($(this).attr('id'));
}

//https://api.pearson.com/longman/dictionary/entry.json?q=cat&apikey=1766cba83f05e0a627fbe111ab8ae039
