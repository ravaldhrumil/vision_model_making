document.getElementById("modelForm").addEventListener("submit", function(event) {
    var learningRateValue = parseFloat(document.getElementById("learning_rate").value);
    if (isNaN(learningRateValue) || learningRateValue <= 0 || learningRateValue >= 1) {
        document.getElementById("learningRateError").innerText = "Learning rate must be a float between 0 and 1.";
        event.preventDefault(); // Prevent form submission
    } else {
        document.getElementById("learningRateError").innerText = ""; // Clear any previous error message
    }
});