from flask import Flask, render_template, jsonify
import requests
from threading import Timer

app = Flask(__name__)
ping_data = {"status": "No ping yet", "response": ""}

def ping_api():
    global ping_data
    try:
        response = requests.get("https://proxygen-api-v1.onrender.com/generate_proxy")
        ping_data["status"] = "Ping successful"
        ping_data["response"] = response.text
    except Exception as e:
        ping_data["status"] = "Ping failed"
        ping_data["response"] = str(e)
    
    # Schedule the next ping in 10 minutes (600 seconds)
    Timer(600, ping_api).start()

# Start the first ping when the app starts
ping_api()

@app.route('/')
def index():
    return render_template('index.html', data=ping_data)

@app.route('/ping-data', methods=['GET'])
def get_ping_data():
    return jsonify(ping_data)

if __name__ == '__main__':
    app.run(debug=True)
