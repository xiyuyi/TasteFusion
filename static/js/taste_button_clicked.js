function bindTasteButtonEvents() {
    // Add event listener for all taste buttons
    const tasteButtons = document.querySelectorAll('.btn');
    tasteButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the associated count span for this button
            const countSpan = button.nextElementSibling;
            let count = parseInt(countSpan.textContent, 10);
            count += 1;
            countSpan.textContent = count.toString();
        });
    });

    // Add event listener for all minus buttons
    const minusButtons = document.querySelectorAll('.btn-minus');
    minusButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the associated count span for this button (it's the previous element)
            const countSpan = button.previousElementSibling;
            let count = parseInt(countSpan.textContent, 10);
            if(count > 0) { // Ensure the count doesn't go below 0
                count -= 1;
                countSpan.textContent = count.toString();
            }
        });
    });
}

// Attach event listeners on initial page load
document.addEventListener("DOMContentLoaded", function() {
    bindTasteButtonEvents();
});
