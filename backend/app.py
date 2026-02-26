import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import blueprints and routes
from routes import auth_routes, camera_routes, alert_routes, video_routes

# Register blueprints
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(camera_routes.camera_bp)
app.register_blueprint(alert_routes.alert_bp)
app.register_blueprint(video_routes.video_bp)

# WebSocket events for real-time alerts
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('subscribe_alerts')
def handle_subscribe_alerts(data):
    print(f'Client subscribed to alerts: {data}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)