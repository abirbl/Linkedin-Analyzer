function generateReport() {
    const postUrl = document.getElementById('post-url').value;
    if (postUrl.trim() === '') {
        document.getElementById('error').textContent = 'Please enter a valid LinkedIn post URL.';
        document.getElementById('success').textContent = '';
        return;
    }

    document.getElementById('error').textContent = '';
    document.getElementById('success').textContent = '';
    document.getElementById('loading').style.display = 'block';

    // Send a POST request to the Flask API to generate the report
    fetch('/generate_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: postUrl }),
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to generate the report. Please check the LinkedIn post URL.');
        }
    })
    .then(blob => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('success').textContent = 'Report generated successfully!';
        downloadBlob(blob, 'report.pdf');
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').textContent = error.message;
    });
}

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
}
