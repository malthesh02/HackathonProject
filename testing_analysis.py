class TestingAnalyzer:
    """Analyze testing practices"""
    
    def __init__(self, contents, repo_data):
        self.contents = contents
        self.repo_data = repo_data
    
    def analyze(self):
        """
        Analyze testing quality
        
        Returns:
            dict: Testing analysis with score
        """
        scores = []
        details = {}
        
        # 1. Has test directory (40%)
        has_tests = self._has_test_directory()
        test_score = 100 if has_tests else 20
        scores.append(test_score * 0.40)
        details['has_test_directory'] = has_tests
        
        # 2. CI/CD configuration (30%)
        has_ci = self._has_ci_config()
        ci_score = 100 if has_ci else 30
        scores.append(ci_score * 0.30)
        details['has_ci_config'] = has_ci
        
        # 3. Test file indicators (30%)
        test_file_score = self._check_test_files()
        scores.append(test_file_score * 0.30)
        details['test_file_score'] = test_file_score
        
        final_score = sum(scores)
        
        return {
            'score': round(final_score, 2),
            'details': details
        }
    
    def _has_test_directory(self):
        """Check if repository has test directory"""
        file_names = [item.get('name', '').lower() for item in self.contents]
        return any('test' in name for name in file_names)
    
    def _has_ci_config(self):
        """Check for CI/CD configuration files"""
        file_names = [item.get('name', '').lower() for item in self.contents]
        
        ci_indicators = [
            '.github',
            '.travis.yml',
            '.circleci',
            'jenkinsfile',
            '.gitlab-ci.yml',
            'azure-pipelines.yml'
        ]
        
        return any(indicator in file_names for indicator in ci_indicators)
    
    def _check_test_files(self):
        """Check for test-related files"""
        file_names = [item.get('name', '').lower() for item in self.contents]
        
        score = 30
        
        # Common test file patterns
        test_patterns = ['test_', '_test.', 'spec.', '.test.']
        
        if any(any(pattern in name for pattern in test_patterns) for name in file_names):
            score += 40
        
        # Test configuration files
        if any(name in file_names for name in ['pytest.ini', 'jest.config.js', '.coveragerc']):
            score += 30
        
        return min(100, score)