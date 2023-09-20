from flask import Flask, request, jsonify, render_template
import os
import time

app = Flask(__name__)

cameras = ['cam-frontcenter', 'cam-frontleft', 'cam-frontright', 'cam-frontdown', 'cam-rearcenter', 'cam-rearleft', 'cam-rearright', 'cam-reardown']

@app.route('/control_service', methods=['GET'])
def control_service():
    action = request.args.get('action')
    service_name = request.args.get('service_name')

    if not action or not service_name or service_name not in cameras:
        return jsonify({"error": "Invalid parameters"}), 400

    stop_all()
    time.sleep(1)

    if action == 'start':
        os.system(f'sudo systemctl start {service_name}')
    elif action == 'stop':
        os.system(f'sudo systemctl stop {service_name}')
    else:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({"status": "OK"}), 200

@app.route('/stop_all', methods=['GET'])
def stop_all():
    for cam in cameras:
        os.system(f'sudo systemctl stop {cam}')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

