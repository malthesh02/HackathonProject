from scoring.weight_config import WeightConfig

class ScoreCalculator:
    """Calculate final repository score"""
    
    def __init__(self, analysis_results):
        """
        Initialize with analysis results
        
        Args:
            analysis_results (dict): Results from all analyzers
        """
        self.results = analysis_results
        self.weights = WeightConfig.get_weights()
    
    def calculate_final_score(self):
        """
        Calculate weighted final score
        
        Returns:
            dict: Final score and breakdown
        """
        scores = {
            'code_quality': self.results.get('code_quality', {}).get('score', 0),
            'project_structure': self.results.get('structure', {}).get('score', 0),
            'documentation': self.results.get('documentation', {}).get('score', 0),
            'testing': self.results.get('testing', {}).get('score', 0),
            'git_behavior': self.results.get('git_behavior', {}).get('score', 0),
            'real_world_value': self.results.get('real_world_value', 0)
        }
        
        # Calculate weighted score
        final_score = sum(
            scores[category] * weight 
            for category, weight in self.weights.items()
        )
        
        return {
            'final_score': round(final_score, 2),
            'category_scores': scores,
            'weights': self.weights,
            'grade': self._get_grade(final_score)
        }
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        else:
            return 'D'