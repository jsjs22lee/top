from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=0.5),
        "mem": psutil.virtual_memory().percent
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
