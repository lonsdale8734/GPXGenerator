$(document).ready(function() {
function createMarker(map, latLng) {
	var marker = new google.maps.Marker({
		position: latLng,
		map: map,
		draggable: true,
	});

	marker.addListener('dblclick', function() {
		marker.setMap(null);
		marker = null;
	});

	return marker;
}

function showLatLngInUrl(latLng) {
	var query = '?latlng=' + latLng.toUrlValue();
	window.history.replaceState(null, null, query);
}

function createMap(callback) {
	var initPoint = {lat: 1.344329,lng: 103.824062};
	var holder = document.getElementById('map');
	var config = {
		center: initPoint,
		zoom: 14,
	};

	var map = new google.maps.Map(holder, config);

	var markerGroup = [];
	map.addListener('rightclick', function(evt) {
		var marker = createMarker(map, evt.latLng);
		markerGroup.push(marker);
	});

	map.addListener('click', function(evt) {
		showLatLngInUrl(evt.latLng);
	});

	callback(markerGroup);
	return markerGroup;
}

function formatMarkers(markerGroup) {
	var data = '[';
	var seperator = '';

	markerGroup.forEach(function(marker) {
		var latLng = marker.getPosition();
		if (latLng) data += seperator + '[' + latLng.lat() +
			',' + latLng.lng() + ']';
		seperator = ',';
	});

	data += ']';
	return data;
}

function check(markerGroup) {
	$('#check').on('click', function() {
		var data = formatMarkers(markerGroup);
		if (data === '[]') return;

		var newTab = window.open('', '_blank');
		$.ajax({
			type: 'POST',
			url: '/view',
			contentType: "application/json; charset=utf-8",
			data: data,
			success: function(response) {
				newTab.document.write(response);
			}
		});
	});
}

function check2(markerGroup) {
	$('#check').on('click', function() {
		var data = formatMarkers(markerGroup);
		if (data === '[]') return;
		window.open('/view?' + data, '_blank');
	});
}

function download(markerGroup) {
	$('#download').on('click', function() {
		var data = formatMarkers(markerGroup);
		if (data === '[]') return;
		window.open('/download?' + data, '_blank');
	});
}

function clear(markerGroup) {
	$('#clear').on('click', function() {
		markerGroup.forEach(function(marker) {
			if (marker) {
				marker.setMap(null);
				marker = null;
			}
		});
		markerGroup.length = 0;
	});
}

function initMap() {
	createMap(function(markerGroup) {
		download(markerGroup);
		check2(markerGroup);
		clear(markerGroup);
	});
}

initMap();
});