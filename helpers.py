import re
from datetime import datetime, timedelta

class Helpers:
    """Utility helper functions"""
    
    @staticmethod
    def calculate_percentage(value, max_value):
        """Calculate percentage with bounds checking"""
        if max_value == 0:
            return 0
        return min(100, (value / max_value) * 100)
    
    @staticmethod
    def normalize_score(score, min_val=0, max_val=100):
        """Normalize score to 0-100 range"""
        return max(min_val, min(max_val, score))
    
    @staticmethod
    def is_commit_message_good(message):
        """
        Check if commit message follows good practices
        Good practices:
        - At least 10 characters
        - Starts with capital letter
        - Not generic (fix, update, etc.)
        """
        if not message or len(message) < 10:
            return False
        
        generic_messages = ['fix', 'update', 'changes', 'minor', 'test', 'wip']
        message_lower = message.lower()
        
        if any(msg == message_lower for msg in generic_messages):
            return False
        
        return message[0].isupper()
    
    @staticmethod
    def calculate_commit_frequency(commits):
        """Calculate average commits per week"""
        if not commits or len(commits) < 2:
            return 0
        
        try:
            first_commit = datetime.strptime(commits[-1]['commit']['author']['date'], 
                                            '%Y-%m-%dT%H:%M:%SZ')
            last_commit = datetime.strptime(commits[0]['commit']['author']['date'], 
                                           '%Y-%m-%dT%H:%M:%SZ')
            
            days_diff = (last_commit - first_commit).days
            if days_diff == 0:
                return len(commits)
            
            weeks = days_diff / 7
            return len(commits) / max(weeks, 1)
        except:
            return 0
    
    @staticmethod
    def extract_links_from_readme(readme_content):
        """Extract URLs from README"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, readme_content)
    
    @staticmethod
    def get_file_extension(filename):
        """Get file extension"""
        if '.' not in filename:
            return ''
        return filename.split('.')[-1].lower()