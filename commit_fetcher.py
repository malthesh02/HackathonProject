import requests
from config import Config

class CommitFetcher:
    """Fetch commit history from GitHub API"""
    
    def __init__(self):
        self.base_url = Config.GITHUB_API_BASE
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if Config.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {Config.GITHUB_TOKEN}'
    
    def fetch_commits(self, owner, repo, max_commits=None):
        """
        Fetch commit history
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            max_commits (int): Maximum number of commits to fetch
            
        Returns:
            list: List of commit objects
        """
        if max_commits is None:
            max_commits = Config.MAX_COMMITS_TO_ANALYZE
        
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'per_page': min(max_commits, 100)}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return []
    
    def fetch_contributors(self, owner, repo):
        """
        Fetch repository contributors
        
        Returns:
            list: List of contributors
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return []