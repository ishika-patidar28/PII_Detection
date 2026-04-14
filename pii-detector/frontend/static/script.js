document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileNameDisplay = document.getElementById('fileName');
    const scanBtn = document.getElementById('scanBtn');
    const loading = document.getElementById('loading');
    const errorContainer = document.getElementById('errorContainer');
    const errorText = document.getElementById('errorText');
    const resultsSection = document.getElementById('resultsSection');
    const piiCount = document.getElementById('piiCount');
    const categoryCount = document.getElementById('categoryCount');
    const piiResults = document.getElementById('piiResults');
    const extractedText = document.getElementById('extractedText');
    const redactedText = document.getElementById('redactedText');

    // Handle file upload
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        handleFileSelect(e.dataTransfer.files);
    });

    function handleFileSelect(files) {
        if (files.length > 0) {
            const file = files[0];
            fileNameDisplay.textContent = file.name;
            fileInfo.style.display = 'block';
        }
    }

    scanBtn.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (file) {
            loading.style.display = 'block';
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/detect_pii', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    showError(data.error);
                } else {
                    displayResults(data);
                }
            })
            .catch(err => {
                loading.style.display = 'none';
                showError('An error occurred while processing the file.');
            });
        }
    });

    function showError(message) {
        errorText.textContent = message;
        errorContainer.style.display = 'block';
    }

    function displayResults(data) {
        piiCount.textContent = data.pii_count;
        categoryCount.textContent = data.category_count;
        piiResults.innerHTML = data.pii_results.map(result => `<p>${result}</p>`).join('');
        extractedText.textContent = data.extracted_text;
        redactedText.textContent = data.redacted_text;
        resultsSection.style.display = 'block';
    }

    // Additional functionality for manual input and other buttons can be added here
});