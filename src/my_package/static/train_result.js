// Parse chart data passed from Flask route
var chartData = chart_data;
        
// Create line chart for Loss using Chart.js
var ctxLoss = document.getElementById('lossChart').getContext('2d');
var lossChart = new Chart(ctxLoss, {
    type: 'line',
    data: {
        labels: chartData.epochs,
        datasets: [{
            label: 'Test Loss',
            data: chartData.test_loss,
            borderColor: 'blue',
            fill: false
        }, {
            label: 'Train Loss',
            data: chartData.train_loss,
            borderColor: 'red',
            fill: false
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Train Loss & Test Loss'
        }
    }
});

// Create line chart for Accuracy using Chart.js
var ctxAccuracy = document.getElementById('accuracyChart').getContext('2d');
var accuracyChart = new Chart(ctxAccuracy, {
    type: 'line',
    data: {
        labels: chartData.epochs,
        datasets: [{
            label: 'Test Accuracy',
            data: chartData.test_acc,
            borderColor: 'green',
            fill: false
        }, {
            label: 'Train Accuracy',
            data: chartData.train_acc,
            borderColor: 'orange',
            fill: false
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Train Accuracy & Test Accuracy'
        },
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                    max: 100,
                    stepSize: 10
                }
            }]
        }
    }
});

// Add an event listener to the button
document.getElementById('goBackButton').addEventListener('click', function() {
    // Go back to the previous window
    window.history.back();
});