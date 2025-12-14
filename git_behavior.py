from utils.helpers import Helpers

class GitBehaviorAnalyzer:
    """Analyze Git usage and commit practices"""
    
    def __init__(self, commits, contributors, repo_data):
        self.commits = commits
        self.contributors = contributors
        self.repo_data = repo_data
    
    def analyze(self):
        """
        Analyze Git behavior
        
        Returns:
            dict: Git behavior analysis with score
        """
        scores = []
        details = {}
        
        # 1. Commit frequency (30%)
        frequency_score = self._analyze_commit_frequency()
        scores.append(frequency_score * 0.30)
        details['commit_frequency_score'] = frequency_score
        
        # 2. Commit message quality (35%)
        message_score = self._analyze_commit_messages()
        scores.append(message_score * 0.35)
        details['commit_message_score'] = message_score
        
        # 3. Number of commits (20%)
        count_score = self._analyze_commit_count()
        scores.append(count_score * 0.20)
        details['commit_count_score'] = count_score
        details['total_commits'] = len(self.commits)
        
        # 4. Collaboration (15%)
        collab_score = self._analyze_collaboration()
        scores.append(collab_score * 0.15)
        details['collaboration_score'] = collab_score
        details['total_contributors'] = len(self.contributors)
        
        final_score = sum(scores)
        
        return {
            'score': round(final_score, 2),
            'details': details
        }
    
    def _analyze_commit_frequency(self):
        """Score based on commit frequency"""
        if not self.commits:
            return 0
        
        frequency = Helpers.calculate_commit_frequency(self.commits)
        
        if frequency >= 3:  # 3+ commits per week
            return 100
        elif frequency >= 1:  # 1-3 commits per week
            return 80
        elif frequency >= 0.5:  # ~2 commits per month
            return 60
        elif frequency > 0:
            return 40
        else:
            return 20
    
    def _analyze_commit_messages(self):
        """Score commit message quality"""
        if not self.commits:
            return 0
        
        good_messages = 0
        for commit in self.commits[:20]:  # Check first 20
            message = commit.get('commit', {}).get('message', '')
            if Helpers.is_commit_message_good(message):
                good_messages += 1
        
        percentage = (good_messages / min(20, len(self.commits))) * 100
        return percentage
    
    def _analyze_commit_count(self):
        """Score based on total commits"""
        count = len(self.commits)
        
        if count >= 50:
            return 100
        elif count >= 20:
            return 80
        elif count >= 10:
            return 60
        elif count >= 5:
            return 40
        else:
            return max(20, count * 4)
    
    def _analyze_collaboration(self):
        """Score based on number of contributors"""
        count = len(self.contributors)
        
        if count >= 5:
            return 100
        elif count >= 3:
            return 80
        elif count >= 2:
            return 60
        elif count == 1:
            return 40
        else:
            return 20
