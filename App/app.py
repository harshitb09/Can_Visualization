from flask import Flask, url_for, render_template, jsonify, request, redirect
from flask_scheduler import Scheduler
from data_preprocess import get_data
import time
import threading
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import current_user
from config.config import login_manager

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'

def update_data():
    global processed_data
    while True:
        processed_data = get_data()
        time.sleep(3)

data_thread = threading.Thread(target=update_data)
data_thread.daemon = True  
data_thread.start()

login_manager.init_app(app)

from blueprint.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data_route():
    global processed_data
    return jsonify(processed_data)

@app.route("/login")
def login():
    if current_user.is_active:
        return redirect(url_for('index'))  # Redirect to homepage if logged in
    return render_template("login.html")

@app.route("/visualization")
def visualization():
    return render_template("network_vis.html")

if __name__ == '__main__':
    app.run(debug=True)
