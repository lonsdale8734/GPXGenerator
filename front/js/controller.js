$(document).ready(function() {



function showLatLngInUrl(latLng) {
	var query = '?latlng=' + latLng.toUrlValue();
	window.history.replaceState(null, null, query);
}

function createMarker(map, latLng) {
	var marker = new google.maps.Marker({
		position: latLng,
		map: map,
		draggable: true,
	});

	marker.addListener('dblclick', function() {
		deleteMarker(marker);
	});

	markerGroup.push(marker);
	return marker;
}

function createUserMarker(map, latLng) {
	var marker = new google.maps.Marker({
		position: latLng,
		map: map,
		clickable: false,
		label: new google.maps.MarkerLabel({
			text: 'U',
			color: 'blue',
		}),
	});

	return marker;
}

function deleteMarker(marker) {
	markerGroup.splice(marker, 1);
	marker.setMap(null);
	marker = null;
}

function clearMarker() {
	markerGroup.forEach(function(marker) {
		marker.setMap(null);
		marker = null;
	});
	markerGroup.length = 0;
}

function formatMarkers() {
	return markerGroup.map(function(marker) {
		var latLng = marker.getPosition();
		return [latLng.lat(), latLng.lng()];
	});
}

function createMap(center) {
	var initPoint = center || {lat: 1.344329, lng: 103.824062};
	var holder = document.getElementById('map');
	var config = {
		center: initPoint,
		zoom: 14,
	};

	var map = new google.maps.Map(holder, config);

	map.addListener('rightclick', function(evt) {
		createMarker(map, evt.latLng);
	});

	map.addListener('click', function(evt) {
		showLatLngInUrl(evt.latLng);
	});

	return map;
}

function requestPost(url, data) {
	$.ajax({
		type: 'POST',
		url: url,
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify(data),
		success: function(response) {
			console.log('success');
		}
	});
}

function requestGet(url) {
	$.ajax({
		type: 'GET',
		url: url,
		success: function(response) {
			console.log(response);
		}
	});
}

function setSpeed() {
	var speed = $('#speed').val();
	if (speed) {
		requestPost('/speed', speed);
	}
}

function addRoute() {
	if (markerGroup.length > 0) {
		requestPost('/route', formatMarkers());
	}
}

function scan() {
	requestGet('/scan');
}

function pop() {
	requestGet('/pop')
}

function track() {

}

function pause() {
	requestGet('/pause');
}

function start() {
	requestGet('/start');
}

function bindAction() {
	$('#clear').on('click', clearMarker);
	$('#speedGo').on('click', setSpeed);
	$('#route').on('click', addRoute);
	$('#scan').on('click', scan);
	$('#pop').on('click', pop);
	$('#track').on('click', track);

	$('#pause').on('click', pause);
	$('#start').on('click', start);
}

var markerGroup = [];
var map = createMap();
bindAction();
});