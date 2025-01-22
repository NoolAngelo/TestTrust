# ml_components/iris_recognition.py
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import dlib
import os

class IrisRecognition:
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
        self.iris_model = self._create_iris_model()
        
    def _create_iris_model(self):
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam',
                     loss='binary_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def extract_iris(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray)
        
        iris_data = []
        for face in faces:
            landmarks = self.landmark_predictor(gray, face)
            
            # Get eye regions
            left_eye = self._get_eye_region(landmarks, 36, 41)
            right_eye = self._get_eye_region(landmarks, 42, 47)
            
            # Process eye regions
            left_iris = self._process_eye_region(frame, left_eye)
            right_iris = self._process_eye_region(frame, right_eye)
            
            if left_iris is not None and right_iris is not None:
                iris_data.append({
                    'left_iris': left_iris,
                    'right_iris': right_iris,
                    'face_position': (face.left(), face.top(), face.right(), face.bottom())
                })
        
        return iris_data
    
    def _get_eye_region(self, landmarks, start_point, end_point):
        points = []
        for i in range(start_point, end_point + 1):
            point = landmarks.part(i)
            points.append((point.x, point.y))
        return np.array(points)
    
    def _process_eye_region(self, frame, eye_points):
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [eye_points], 255)
        eye = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Get bounding box of eye region
        x, y = np.min(eye_points, axis=0)
        w = np.max(eye_points[:, 0]) - x
        h = np.max(eye_points[:, 1]) - y
        
        # Extract eye ROI
        eye_roi = eye[y:y+h, x:x+w]
        if eye_roi.size == 0:
            return None
            
        # Resize to standard size
        eye_roi = cv2.resize(eye_roi, (64, 64))
        return eye_roi

    def verify_iris(self, iris_data):
        if not iris_data:
            return False
            
        results = []
        for data in iris_data:
            left_score = self.iris_model.predict(
                np.expand_dims(data['left_iris'], axis=0)
            )[0][0]
            right_score = self.iris_model.predict(
                np.expand_dims(data['right_iris'], axis=0)
            )[0][0]
            
            # Average the scores
            avg_score = (left_score + right_score) / 2
            results.append(avg_score)
        
        # Return True if any iris pair matches
        return max(results) > 0.8 if results else False

# ml_components/behavior_analysis.py
class BehaviorAnalysis:
    def __init__(self):
        self.movement_history = []
        self.gaze_history = []
        self.attention_threshold = 0.7
        
    def analyze_movement(self, face_position, previous_position=None):
        if previous_position is None:
            return 0.0
            
        # Calculate movement distance
        current_center = (
            (face_position[0] + face_position[2]) / 2,
            (face_position[1] + face_position[3]) / 2
        )
        previous_center = (
            (previous_position[0] + previous_position[2]) / 2,
            (previous_position[1] + previous_position[3]) / 2
        )
        
        distance = np.sqrt(
            (current_center[0] - previous_center[0])**2 +
            (current_center[1] - previous_center[1])**2
        )
        
        self.movement_history.append(distance)
        if len(self.movement_history) > 30:  # Keep last 30 frames
            self.movement_history.pop(0)
            
        return self._calculate_movement_score()
    
    def _calculate_movement_score(self):
        if not self.movement_history:
            return 0.0
            
        avg_movement = np.mean(self.movement_history)
        max_acceptable_movement = 100  # pixels
        
        movement_score = 1.0 - min(avg_movement / max_acceptable_movement, 1.0)
        return movement_score
    
    def analyze_gaze(self, eye_positions):
        # Calculate gaze direction based on eye positions
        gaze_score = self._calculate_gaze_score(eye_positions)
        self.gaze_history.append(gaze_score)
        
        if len(self.gaze_history) > 30:
            self.gaze_history.pop(0)
            
        return np.mean(self.gaze_history)
    
    def _calculate_gaze_score(self, eye_positions):
        if not eye_positions:
            return 0.0
            
        # Simple gaze score based on eye position relative to face
        # More sophisticated gaze estimation could be implemented here
        return 0.8  # Placeholder score
    
    def calculate_attention_score(self, movement_score, gaze_score):
        # Combine movement and gaze scores for overall attention
        attention_score = 0.6 * gaze_score + 0.4 * movement_score
        return attention_score

# ml_components/activity_detection.py
class ActivityDetection:
    def __init__(self):
        self.activity_history = []
        self.suspicious_threshold = 0.8
        
    def detect_suspicious_activity(self, movement_score, gaze_score, attention_score):
        activity_score = self._calculate_activity_score(
            movement_score, gaze_score, attention_score
        )
        
        self.activity_history.append(activity_score)
        if len(self.activity_history) > 60:  # 1 minute history
            self.activity_history.pop(0)
            
        return self._evaluate_activity_pattern()
    
    def _calculate_activity_score(self, movement_score, gaze_score, attention_score):
        # Weighted combination of different metrics
        weights = {
            'movement': 0.3,
            'gaze': 0.3,
            'attention': 0.4
        }
        
        activity_score = (
            weights['movement'] * movement_score +
            weights['gaze'] * gaze_score +
            weights['attention'] * attention_score
        )
        
        return activity_score
    
    def _evaluate_activity_pattern(self):
        if not self.activity_history:
            return False
            
        recent_activity = np.mean(self.activity_history[-10:])
        return recent_activity > self.suspicious_threshold
