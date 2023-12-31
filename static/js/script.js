document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = '<p>Error: ' + data.error + '</p>';
        } else {
            resultDiv.innerHTML = '<p>Predicted Disease: ' + data.result + '</p>' +
                                  '<p>Remedy: ' + data.remedy + '</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});