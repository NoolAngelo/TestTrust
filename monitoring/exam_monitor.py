# monitoring/exam_monitor.py
import cv2
import numpy as np
import time
import logging
from datetime import datetime
from ml_components.iris_recognition import IrisRecognition
from ml_components.behavior_analysis import BehaviorAnalysis
from ml_components.activity_detection import ActivityDetection

class ExamMonitor:
    def __init__(self):
        self.setup_logging()
        self.iris_recognition = IrisRecognition()
        self.behavior_analysis = BehaviorAnalysis()
        self.activity_detection = ActivityDetection()
        
        self.previous_face_position = None
        self.violation_count = 0
        self.session_start = datetime.now()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='exam_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('ExamMonitor')
        
    def process_frame(self, frame):
        try:
            # Extract iris data
            iris_data = self.iris_recognition.extract_iris(frame)
            
            # Verify iris if data is available
            iris_verified = self.iris_recognition.verify_iris(iris_data)
            
            # Get current face position
            current_face_position = (
                iris_data[0]['face_position'] if iris_data else None
            )
            
            # Analyze behavior
            movement_score = self.behavior_analysis.analyze_movement(
                current_face_position, 
                self.previous_face_position
            )
            
            gaze_score = self.behavior_analysis.analyze_gaze(
                [data['left_iris'] for data in iris_data] if iris_data else []
            )
            
            attention_score = self.behavior_analysis.calculate_attention_score(
                movement_score, 
                gaze_score
            )
            
            # Detect suspicious activity
            suspicious_activity = self.activity_detection.detect_suspicious_activity(
                movement_score,
                gaze_score,
                attention_score
            )
            
            # Update previous face position
            self.previous_face_position = current_face_position
            
            # Generate monitoring results
            results = {
                'timestamp': datetime.now(),
                'iris_verified': iris_verified,
                'movement_score': movement_score,
                'gaze_score': gaze_score,
                'attention_score': attention_score,
                'suspicious_activity': suspicious_activity
            }
            
            # Log violations if any
            if suspicious_activity or not iris_verified:
                self.log_violation(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing frame: {str(e)}")
            return None
            
    def log_violation(self, results):
        self.violation_count += 1
        self.logger.warning(
            f"Violation detected: {results}"
        )

# analytics/real_time_analytics.py
class RealTimeAnalytics:
    def __init__(self):
        self.metrics_history = []
        self.violation_history = []
        self.attention_threshold = 0.7
        self.violation_threshold = 3
        
    def update_metrics(self, monitoring_results):
        if monitoring_results is None:
            return
            
        self.metrics_history.append(monitoring_results)
        if len(self.metrics_history) > 1800:  # 30 minutes history
            self.metrics_history.pop(0)
            
        if not monitoring_results['iris_verified'] or monitoring_results['suspicious_activity']:
            self.violation_history.append(monitoring_results)
            
        return self.generate_analytics_report()
        
    def generate_analytics_report(self):
        if not self.metrics_history:
            return None
            
        recent_metrics = self.metrics_history[-60:]  # Last minute
        
        report = {
            'attention_level': self._calculate_average_attention(recent_metrics),
            'violation_count': len(self.violation_history),
            'risk_score': self._calculate_risk_score(recent_metrics),
            'session_summary': self._generate_session_summary()
        }
        
        return report
        
    def _calculate_average_attention(self, metrics):
        attention_scores = [m['attention_score'] for m in metrics]
        return np.mean(attention_scores)
        
    def _calculate_risk_score(self, metrics):
        # Weighted risk calculation
        weights = {
            'attention': 0.3,
            'suspicious_activity': 0.4,
            'iris_verification': 0.3
        }
        
        attention_score = np.mean([m['attention_score'] for m in metrics])
        suspicious_ratio = np.mean([1 if m['suspicious_activity'] else 0 for m in metrics])
        iris_ratio = np.mean([1 if m['iris_verified'] else 0 for m in metrics])
        
        risk_score = (
            weights['attention'] * (1 - attention_score) +
            weights['suspicious_activity'] * suspicious_ratio +
            weights['iris_verification'] * (1 - iris_ratio)
        )
        
        return risk_score
        
    def _generate_session_summary(self):
        return {
            'total_violations': len(self.violation_history),
            'average_attention': np.mean([m['attention_score'] for m in self.metrics_history]),
            'suspicious_activity_ratio': np.mean(
                [1 if m['suspicious_activity'] else 0 for m in self.metrics_history]
            )
        }

class SecureTransmission:
    def __init__(self, server_url, encryption_key):
        self.server_url = server_url
        self.fernet = Fernet(encryption_key)  # Fix initialization

    async def send_data(self, data):
        async with websockets.connect(self.server_url, ssl=ssl.SSLContext()) as websocket:
            encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
            await websocket.send(encrypted_data)

    async def receive_data(self):
        async with websockets.connect(self.server_url, ssl=ssl.SSLContext()) as websocket:
            encrypted_data = await websocket.recv()
            data = json.loads(self.fernet.decrypt(encrypted_data).decode())
            return data