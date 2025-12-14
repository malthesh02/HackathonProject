from config import Config

class WeightConfig:
    """Centralized scoring weight configuration"""
    
    @staticmethod
    def get_weights():
        """Get scoring weights"""
        return Config.WEIGHTS
    
    @staticmethod
    def get_weight(category):
        """Get weight for specific category"""
        return Config.WEIGHTS.get(category, 0)
    
    @staticmethod
    def validate_weights():
        """Validate that weights sum to 1.0"""
        total = sum(Config.WEIGHTS.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        return True
