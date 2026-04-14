from flask import Flask
from api import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return "Welcome to the PII Detection & Redaction Tool API!"

if __name__ == '__main__':
    app.run(debug=True)