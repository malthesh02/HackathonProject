import requests
from config import Config

class RepoFetcher:
    """Fetch repository data from GitHub API"""
    
    def __init__(self):
        self.base_url = Config.GITHUB_API_BASE
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if Config.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {Config.GITHUB_TOKEN}'
    
    def fetch_repo_info(self, owner, repo):
        """
        Fetch basic repository information
        
        Returns:
            dict: Repository data including stars, forks, description, etc.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch repository: {str(e)}")
    
    def fetch_readme(self, owner, repo):
        """
        Fetch repository README
        
        Returns:
            dict: README content and metadata
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            
            data = response.json()
            # Decode base64 content
            import base64
            content = base64.b64decode(data['content']).decode('utf-8')
            
            return {
                'name': data['name'],
                'size': data['size'],
                'content': content
            }
        except:
            return None
    
    def fetch_contents(self, owner, repo, path=''):
        """
        Fetch repository contents at given path
        
        Returns:
            list: List of files and directories
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            return response.json()
        except:
            return []