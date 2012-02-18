var MPTREND = MPTREND || {};

MPTREND.map = {
	//should be one off initialising for this first bit
	mapObj: undefined,
	infowindow: undefined,
	jsonUrl: 'code/demo',
	currentAjaxRequest: undefined,
	filter: {
        mp: {
            clusterImage: [{
                url: '/img/map_icons/mp_30x30.png',
                height: 31,
                width: 30,
                anchor: [5],
                textColor: '#002776',
                textSize: 12
            }, {
                url: '/img/map_icons/mp_30x30.png',
                height: 35,
                width: 32,
                anchor: [7],
                textColor: '#002776',
                textSize: 12
            }, {
                url: '/img/map_icons/mp_45x45.png',
                height: 45,
                width: 45,
                anchor: [11],
                textColor: '#002776',
                textSize: 12
            }],
            markerImageURL: "/img/map_icons/mp.png",
            markerImageWidth: 40,
            markerImageHeight: 38,
            markerAnchorX: 20,
            markerAnchorY: 47,
            clusterMaxZoom: 11,
            clusterGridSize: 80,
            jsontTemplate: {
                "self": "{container}",
                "container": "<h2>{$.first_name} {$.last_name}</h2>{$.about_me}{$.website}",
                "container.about_me": function (about_me) {
                    return about_me ? "<p>" + about_me + "</p>" : "";
                },
                "container.website": function (website) {
                    return website ? "<p>" + website + "</p>" : "";
                }
            }
        }
	},

	mapOptions: {
	  zoom: 8,
	  center: new google.maps.LatLng(53, -3.0),
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	},

	init: function () {

		//if available, set geoLocation, otherwise defaults will display
		this.getGeoLocation();
		//draw the map
		this.mapObj = new google.maps.Map(document.getElementById('map'), this.mapOptions);
		this.getEntities();
	},
	
	getGeoLocation: function () {
		//if geoLocation is, set default location
		var self = this, infowindow = undefined;
		
		if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(function(position) {
				self.mapOptions.zoom = 8;
			    self.mapOptions.center = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
			    //display default message - although, if they are members we could welcome them back?
			    infowindow = new google.maps.InfoWindow({
			      map: self.mapObj,
			      position: self.mapOptions.center,
			      content: "You are here!"
			    });
				self.mapObj.panTo(self.mapOptions.center);
			});
			return true;
		}
		return false;
	},
	
	getEntities: function () {
		var self = this;
        // do Ajax to put in cache
        console.log('getEntities called');
        this.currentAjaxRequest = $.ajax({
			url: this.jsonUrl,
			dataType: "json",
            //data: $.param(requestQS),
            success: function (jsonData) {
                for (var i in jsonData) {
                	var latlng = new google.maps.LatLng(jsonData[i].latitude, jsonData[i].longitude);
					var marker = new google.maps.Marker({
					  position: latlng,
					  icon: self.filter['mp'].markerImageURL,
					  map: self.mapObj,
					  title: jsonData[i].name
					});
					
					(function (mymarker, mylatlng) {
					
						var infowindow = new google.maps.InfoWindow({
							content: jsonData[i].name,
							position: mylatlng
						});
						
						google.maps.event.addListener(marker, 'click', function() {
							infowindow.open(self.mapObj,mymarker);
							self.mapObj.panTo(mylatlng);
						});				
					
					} )(marker, latlng);			

				}
            }
        });
	}

};
