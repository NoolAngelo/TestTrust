# ui/dashboard.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import logging
import signal
import sys

class Dashboard:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.current_metrics = {}  # Initialize current_metrics
        self.setup_logging()
        self.setup_routes()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('Dashboard')
        
    def setup_routes(self):
        @self.app.route('/')
        def index():
            self.logger.debug('Rendering dashboard.html')
            return render_template('dashboard.html')
            
        @self.app.route('/api/metrics')
        def get_metrics():
            self.logger.debug('Returning current metrics')
            return jsonify(self.current_metrics)
            
        @self.socketio.on('connect')
        def handle_connect():
            self.logger.debug('Client connected')
            
    def start(self):
        self.logger.debug('Starting server')
        self.socketio.run(self.app, host='0.0.0.0', port=5001)  # Run directly in the main thread
        
    def update_metrics(self, metrics):
        self.current_metrics = metrics
        self.socketio.emit('metrics_update', metrics)

def signal_handler(sig, frame):
    print('Shutting down server...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    dashboard = Dashboard()
    dashboard.start()

# network/secure_transmission.py
import asyncio
import websockets
import json
import ssl
from cryptography.fernet import Fernet  # Fix import

class SecureTransmission:
    def __init__(self, server_url, encryption_key):
        self.server_url = server_url
        self.fernet = Fernet(encryption_key)  # Fix initialization