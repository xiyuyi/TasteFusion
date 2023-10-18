document.addEventListener('DOMContentLoaded', function() {
    const textLocation = document.getElementById('textLocation');

    textLocation.addEventListener('blur', function() {
        const locationValue = textLocation.value;
        updateMap(locationValue);
    });
});

function updateMap(location) {
    // Create an AJAX request to the Flask backend
    fetch('/address-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            address: location
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
