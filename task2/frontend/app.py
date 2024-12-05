import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def send_request():
    try:
        response = requests.get("http://backend-service/")
        return f"Response from Backend: {response.text}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
