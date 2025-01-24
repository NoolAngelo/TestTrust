class BehaviorAnalysis:
    def __init__(self):
        # ...existing code...
        
    def analyze_movement(self, face_position, previous_position=None):
        # ...existing code...
        return self._calculate_movement_score()
    
    def _calculate_movement_score(self):
        # ...existing code...
        return movement_score
    
    def analyze_gaze(self, eye_positions):
        # ...existing code...
        return np.mean(self.gaze_history)
    
    def _calculate_gaze_score(self, eye_positions):
        # ...existing code...
        return 0.8
    
    def calculate_attention_score(self, movement_score, gaze_score):
        # ...existing code...
        return attention_score
