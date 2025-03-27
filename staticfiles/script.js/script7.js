document.addEventListener('DOMContentLoaded', function() {
    function initMap() {
        var location = {lat: 40.7128, lng: -74.0060};  // Example coordinates for New York City
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 8,
            center: location
        });
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });
    }
    initMap();  // Ensures the map initializes after the DOM is loaded
});
