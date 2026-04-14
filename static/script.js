// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const scanBtn = document.getElementById('scanBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const manualText = document.getElementById('manualText');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorContainer = document.getElementById('errorContainer');
const errorText = document.getElementById('errorText');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

let currentFile = null;
let currentResults = null;

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
        
        // Reset error
        errorContainer.style.display = 'none';
    });
});

// Upload Area - Click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Upload Area - File Selection
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        selectFile(file);
    }
});

// Upload Area - Drag & Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        selectFile(file);
    }
});

// Select File Handler
function selectFile(file) {
    // Check file type
    const allowedTypes = ['.pdf', '.txt', '.png', '.jpg', '.jpeg', '.gif', '.bmp'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExt)) {
        showError('Unsupported file type. Please use PDF, TXT, PNG, JPG, JPEG, GIF, or BMP.');
        return;
    }
    
    // Check file size (50MB max)
    if (file.size > 50 * 1024 * 1024) {
        showError('File size exceeds 50MB limit.');
        return;
    }
    
    currentFile = file;
    fileName.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
    fileInfo.style.display = 'block';
    errorContainer.style.display = 'none';
}

// Scan Button
scanBtn.addEventListener('click', () => {
    if (!currentFile) {
        showError('Please select a file first.');
        return;
    }
    scanFile(currentFile);
});

// Analyze Button
analyzeBtn.addEventListener('click', () => {
    const text = manualText.value.trim();
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }
    analyzeText(text);
});

// Scan File
async function scanFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    loading.style.display = 'block';
    errorContainer.style.display = 'none';
    resultsSection.style.display = 'none';
    
    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error processing file');
        }
        
        const data = await response.json();
        currentResults = data;
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        loading.style.display = 'none';
    }
}

// Analyze Text
async function analyzeText(text) {
    loading.style.display = 'block';
    errorContainer.style.display = 'none';
    resultsSection.style.display = 'none';
    
    try {
        const response = await fetch('/api/redact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error analyzing text');
        }
        
        const data = await response.json();
        currentResults = {
            extracted_text: text.substring(0, 2000),
            full_text: text,
            pii_detected: data.pii_found,
            redacted_text: data.redacted_text,
            has_pii: data.has_pii,
            pii_count: Object.values(data.pii_found).reduce((sum, arr) => sum + arr.length, 0),
            filename: 'manual-input.txt'
        };
        
        displayResults(currentResults);
        
    } catch (error) {
        showError(error.message);
    } finally {
        loading.style.display = 'none';
    }
}

// Display Results
function displayResults(data) {
    resultsSection.style.display = 'block';
    errorContainer.style.display = 'none';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Update summary
    document.getElementById('piiCount').textContent = data.pii_count || 0;
    document.getElementById('categoryCount').textContent = Object.keys(data.pii_detected).length || 0;
    
    // Display PII Results
    const piiResults = document.getElementById('piiResults');
    if (data.has_pii) {
        piiResults.innerHTML = Object.entries(data.pii_detected)
            .map(([category, items]) => `
                <div class="pii-card">
                    <h4>${category} <span class="pii-badge">${items.length}</span></h4>
                    <ul>
                        ${items.slice(0, 5).map(item => `<li>${escapeHtml(item)}</li>`).join('')}
                        ${items.length > 5 ? `<li><em>... and ${items.length - 5} more</em></li>` : ''}
                    </ul>
                </div>
            `)
            .join('');
    } else {
        piiResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #27ae60;"><strong>✓ No PII detected!</strong></div>';
    }
    
    // Display extracted text
    document.getElementById('extractedText').textContent = escapeHtml(data.extracted_text);
    
    // Display redacted text
    document.getElementById('redactedText').textContent = escapeHtml(data.redacted_text);
}

// Copy Redacted Text
document.getElementById('copyRedactedBtn').addEventListener('click', () => {
    if (!currentResults) return;
    
    const text = currentResults.redacted_text;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyRedactedBtn');
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    });
});

// Download Redacted Text
document.getElementById('downloadRedactedBtn').addEventListener('click', () => {
    if (!currentResults) return;
    
    const text = currentResults.redacted_text;
    const filename = currentResults.filename.replace(/\.[^.]*$/, '_redacted.txt');
    
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
});

// New Scan
document.getElementById('newScanBtn').addEventListener('click', () => {
    currentFile = null;
    currentResults = null;
    fileInput.value = '';
    manualText.value = '';
    fileInfo.style.display = 'none';
    resultsSection.style.display = 'none';
    errorContainer.style.display = 'none';
    
    // Switch to upload tab
    document.querySelectorAll('.tab-btn')[0].click();
});

// Show Error
function showError(message) {
    errorText.textContent = message;
    errorContainer.style.display = 'block';
    errorContainer.scrollIntoView({ behavior: 'smooth' });
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
