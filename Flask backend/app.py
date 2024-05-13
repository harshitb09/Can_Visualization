from flask import Flask, url_for, render_template, jsonify
from flask_scheduler import Scheduler
from data_preprocess import get_data
import time
import threading

app = Flask(__name__)

def update_data():
    global processed_data
    while True:
        processed_data = get_data()
        time.sleep(3)

data_thread = threading.Thread(target=update_data)
data_thread.daemon = True  
data_thread.start()

@app.route("/")
def index():
    return render_template("network_vis.html")

@app.route("/data")
def get_data_route():
    global processed_data
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True)
