var tasteFusionButton = document.getElementById('tasteFusionButton');
var tasteContainer = document.querySelector('.taste-buttons-container');

tasteFusionButton.addEventListener('click', function() {
    // Collect current labels and values of taste buttons using the taste rows
    let tasteData = [];

    const tasteRows = tasteContainer.querySelectorAll('.taste-row');
    tasteRows.forEach((row) => {
        const tasteButton = row.querySelector('.btn');
        const tasteValueSpan = row.querySelector('.taste-text');

        tasteData.push({
            label: tasteButton.textContent,
            value: tasteValueSpan.textContent
        });
    });

    fetch('/taste-fusion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tastes: tasteData })  // Send the tastes as part of the request payload
    })
    .then(response => response.json())
    .then(data => {
        // Dynamically update the map
        document.querySelector('.map-container').innerHTML = "<p>TasteFusion</p>"+data.map_html;

        // Clear existing tastes
        tasteContainer.innerHTML = '';

        // Dynamically create and render taste buttons
        data.tastes.forEach((taste, index) => {
            // Create the div container for the taste row
            var tasteRow = document.createElement('div');
            tasteRow.classList.add('taste-row');

            // Create the taste button
            var btn = document.createElement('button');
            btn.classList.add('btn');
            btn.id = 'tasteBtn-' + index;
            btn.textContent = taste;
            tasteRow.appendChild(btn);

            // Create the taste text span
            var span = document.createElement('span');
            span.classList.add('taste-text');
            span.textContent = '0';
            tasteRow.appendChild(span);

            // Create the minus button
            var minusBtn = document.createElement('button');
            minusBtn.classList.add('btn-minus');
            minusBtn.textContent = 'X';
            tasteRow.appendChild(minusBtn);

            // Append the entire row to the tasteContainer
            tasteContainer.appendChild(tasteRow);
        });

        // Bind the event listeners to the newly created taste buttons
        bindTasteButtonEvents();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
