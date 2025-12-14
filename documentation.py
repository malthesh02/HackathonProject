from config import Config
from utils.helpers import Helpers

class DocumentationAnalyzer:
    """Analyze repository documentation quality"""
    
    def __init__(self, readme_data, repo_data):
        self.readme = readme_data
        self.repo_data = repo_data
    
    def analyze(self):
        """
        Analyze documentation quality
        
        Returns:
            dict: Documentation analysis with score
        """
        if not self.readme:
            return {
                'score': 20,
                'details': {
                    'has_readme': False,
                    'length': 0,
                    'quality': 'none'
                }
            }
        
        content = self.readme.get('content', '')
        length = len(content)
        
        scores = []
        details = {}
        
        # 1. README exists (25%)
        scores.append(100 * 0.25)
        details['has_readme'] = True
        
        # 2. Length quality (25%)
        length_score = self._analyze_length(length)
        scores.append(length_score * 0.25)
        details['length'] = length
        details['length_score'] = length_score
        
        # 3. Content quality (30%)
        content_score = self._analyze_content(content)
        scores.append(content_score * 0.30)
        details['content_score'] = content_score
        
        # 4. Structure quality (20%)
        structure_score = self._analyze_structure(content)
        scores.append(structure_score * 0.20)
        details['structure_score'] = structure_score
        
        final_score = sum(scores)
        
        return {
            'score': round(final_score, 2),
            'details': details
        }
    
    def _analyze_length(self, length):
        """Score README based on length"""
        if length < Config.MIN_README_LENGTH:
            return 30
        elif length < Config.IDEAL_README_LENGTH:
            return 30 + (length / Config.IDEAL_README_LENGTH) * 50
        else:
            return min(100, 80 + (length / (Config.IDEAL_README_LENGTH * 2)) * 20)
    
    def _analyze_content(self, content):
        """Score README content quality"""
        content_lower = content.lower()
        score = 40  # Base score
        
        # Check for key sections
        if 'installation' in content_lower or 'install' in content_lower:
            score += 15
        if 'usage' in content_lower or 'example' in content_lower:
            score += 15
        if 'contributing' in content_lower:
            score += 10
        if 'license' in content_lower:
            score += 10
        if any(word in content_lower for word in ['screenshot', 'demo', 'example']):
            score += 10
        
        return min(100, score)
    
    def _analyze_structure(self, content):
        """Score README structure (headers, lists, code blocks)"""
        score = 40
        
        # Check for markdown elements
        if '##' in content or '###' in content:
            score += 20  # Has sections
        if '```' in content:
            score += 20  # Has code blocks
        if '- ' in content or '* ' in content:
            score += 10  # Has lists
        if '[' in content and '](' in content:
            score += 10  # Has links
        
        return min(100, score)
