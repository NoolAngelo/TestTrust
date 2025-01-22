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
