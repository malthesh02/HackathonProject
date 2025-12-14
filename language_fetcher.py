import requests
from config import Config

class LanguageFetcher:
    """Fetch language statistics from GitHub API"""
    
    def __init__(self):
        self.base_url = Config.GITHUB_API_BASE
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if Config.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {Config.GITHUB_TOKEN}'
    
    def fetch_languages(self, owner, repo):
        """
        Fetch language breakdown
        
        Returns:
            dict: Language name -> bytes of code
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return {}
    
    def get_primary_language(self, languages):
        """
        Get the primary language (most bytes)
        
        Returns:
            str: Primary language name
        """
        if not languages:
            return None
        return max(languages.items(), key=lambda x: x[1])[0]
    
    def get_language_diversity_score(self, languages):
        """
        Calculate language diversity score
        More languages = better (up to a point)
        
        Returns:
            int: Score 0-100
        """
        num_languages = len(languages)
        
        if num_languages == 0:
            return 0
        elif num_languages == 1:
            return 40
        elif num_languages == 2:
            return 70
        elif num_languages >= 3:
            return min(100, 70 + (num_languages - 2) * 10)
        
        return 0