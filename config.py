import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # GitHub API
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Optional: increases rate limit
    GITHUB_API_BASE = 'https://api.github.com'
    
    # Analysis Settings
    MAX_COMMITS_TO_ANALYZE = 100
    MIN_README_LENGTH = 200
    IDEAL_README_LENGTH = 1000
    
    # Scoring Weights
    WEIGHTS = {
        'code_quality': 0.30,
        'project_structure': 0.20,
        'documentation': 0.15,
        'testing': 0.15,
        'git_behavior': 0.10,
        'real_world_value': 0.10
    }