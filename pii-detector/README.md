# PII Detection & Redaction Tool

## Overview
The PII Detection & Redaction Tool is a full-stack application designed to identify and redact personally identifiable information (PII) from various document types. The application leverages advanced techniques in natural language processing (NLP) and regular expressions to detect sensitive information and provides users with a simple interface to upload files or input text for analysis.

## Project Structure
```
pii-detector
├── backend
│   ├── app.py                # Main entry point for the backend application
│   ├── api.py                # API endpoints for detecting and redacting PII
│   ├── config.py             # Configuration settings for the application
│   ├── models.py             # Data models used in the application
│   ├── services
│   │   ├── pii_processor.py   # Logic for detecting PII
│   │   └── redaction.py       # Functionality to redact detected PII
│   └── utils
│       └── file_utils.py      # Utility functions for file handling
├── frontend
│   ├── static
│   │   ├── script.js          # JavaScript for frontend interactions
│   │   └── style.css          # CSS styles for the frontend application
│   ├── templates
│   │   └── index.html         # Main HTML template for the frontend
│   └── package.json           # Configuration file for the frontend application
├── tests
│   ├── test_api.py           # Unit tests for API endpoints
│   └── test_pii_processor.py  # Unit tests for PII detection logic
├── .gitignore                 # Files and directories to ignore in version control
├── docker-compose.yml         # Services and configurations for Docker
├── README.md                  # Documentation for the project
└── requirements.txt           # Python dependencies for the backend
```

## Features
- **File Upload**: Users can upload files in various formats (PDF, TXT, images) for PII detection.
- **Manual Input**: Users can paste or type text directly into the application for analysis.
- **PII Detection**: The application identifies sensitive information such as names, addresses, and social security numbers.
- **Redaction**: Detected PII is replaced with "[REDACTED]" to protect user privacy.
- **Results Summary**: Users receive a summary of detected PII and can download redacted text.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd pii-detector
   ```

2. **Install Backend Dependencies**:
   Navigate to the backend directory and install the required Python packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the Backend**:
   Start the backend server:
   ```
   python app.py
   ```

4. **Install Frontend Dependencies**:
   Navigate to the frontend directory and install the required packages:
   ```
   cd frontend
   npm install
   ```

5. **Run the Frontend**:
   Start the frontend application:
   ```
   npm start
   ```

## API Usage
- **Endpoint**: `/api/detect`
  - **Method**: POST
  - **Description**: Analyzes uploaded files or text for PII detection.
  - **Request Body**: JSON containing the text or file data.
  - **Response**: JSON containing detected PII and redacted text.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.