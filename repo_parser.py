class RepoParser:
    """Parse and validate GitHub repository URLs"""
    
    @staticmethod
    def parse_url(repo_url):
        """
        Extract owner and repo name from GitHub URL
        
        Args:
            repo_url (str): GitHub repository URL
            
        Returns:
            tuple: (owner, repo_name)
            
        Raises:
            ValueError: If URL is invalid
        """
        if not repo_url:
            raise ValueError("Repository URL is required")
        
        # Remove trailing slashes and .git
        repo_url = repo_url.rstrip('/').replace('.git', '')
        
        # Handle different URL formats
        if 'github.com/' in repo_url:
            parts = repo_url.split('github.com/')[-1].split('/')
        else:
            parts = repo_url.split('/')
        
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL format. Expected: github.com/owner/repo")
        
        owner = parts[0]
        repo_name = parts[1]
        
        if not owner or not repo_name:
            raise ValueError("Could not extract owner and repository name")
        
        return owner, repo_name
    
    @staticmethod
    def validate_repo_name(name):
        """Validate repository name"""
        if not name or len(name) > 100:
            return False
        return True