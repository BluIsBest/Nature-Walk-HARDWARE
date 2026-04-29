from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Example JSON endpoint
@app.route('/data')
def data():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')

    with open(json_path, 'r') as f:
        data = json.load(f)

    return jsonify(data)

# Optional: root route (so browser shows something)
@app.route('/')
def home():
    return "Jetson Nano is Running!"

if __name__ == '__main__':
    # 0.0.0.0 makes it accessible from your phone
    app.run(host='0.0.0.0', port=5000)
