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
