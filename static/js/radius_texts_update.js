document.addEventListener('DOMContentLoaded', function() {
    const textLocation = document.getElementById('textLocation');
    const textRadius = document.getElementById('textRadius');

    textRadius.addEventListener('blur', function() {
        const locationValue = textLocation.value;
        const radiusValue = textRadius.value;
        updateMapWithRadius(locationValue, radiusValue);
    });
});

function updateMapWithRadius(location, radius) {
    // Create an AJAX request to the Flask backend
    fetch('/radius-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            address: location,
            radius: radius
        })
    })
    .then(response => response.json())
    .then(data => {
        const mapHtml = data.map_html;
        // Assuming you have a div with id 'map' where you want to display the map
        document.querySelector('.map-container').innerHTML = mapHtml;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
