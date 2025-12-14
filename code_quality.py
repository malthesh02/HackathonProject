class CodeQualityAnalyzer:
    """Analyze code quality metrics"""
    
    def __init__(self, repo_data, languages, contents):
        self.repo_data = repo_data
        self.languages = languages
        self.contents = contents
    
    def analyze(self):
        """
        Perform comprehensive code quality analysis
        
        Returns:
            dict: Analysis results with score and details
        """
        scores = []
        details = {}
        
        # 1. Language diversity (25%)
        lang_score = self._analyze_language_diversity()
        scores.append(lang_score * 0.25)
        details['language_diversity'] = lang_score
        
        # 2. Repository maturity (25%)
        maturity_score = self._analyze_maturity()
        scores.append(maturity_score * 0.25)
        details['maturity'] = maturity_score
        
        # 3. Community engagement (25%)
        engagement_score = self._analyze_engagement()
        scores.append(engagement_score * 0.25)
        details['engagement'] = engagement_score
        
        # 4. Code organization (25%)
        organization_score = self._analyze_organization()
        scores.append(organization_score * 0.25)
        details['organization'] = organization_score
        
        final_score = sum(scores)
        
        return {
            'score': round(final_score, 2),
            'details': details,
            'breakdown': {
                'language_diversity': round(lang_score, 2),
                'maturity': round(maturity_score, 2),
                'engagement': round(engagement_score, 2),
                'organization': round(organization_score, 2)
            }
        }
    
    def _analyze_language_diversity(self):
        """Score based on number and distribution of languages"""
        num_languages = len(self.languages)
        
        if num_languages == 0:
            return 20
        elif num_languages == 1:
            return 50
        elif num_languages == 2:
            return 75
        else:
            return min(100, 75 + (num_languages - 2) * 8)
    
    def _analyze_maturity(self):
        """Score based on stars, forks, and age"""
        stars = self.repo_data.get('stargazers_count', 0)
        forks = self.repo_data.get('forks_count', 0)
        
        star_score = min(100, stars * 5) if stars < 20 else 100
        fork_score = min(100, forks * 10) if forks < 10 else 100
        
        return (star_score * 0.6 + fork_score * 0.4)
    
    def _analyze_engagement(self):
        """Score based on watchers and open issues"""
        watchers = self.repo_data.get('watchers_count', 0)
        open_issues = self.repo_data.get('open_issues_count', 0)
        
        watcher_score = min(100, watchers * 5)
        
        # Some issues are good (shows usage), too many might be bad
        if open_issues == 0:
            issue_score = 50
        elif open_issues <= 10:
            issue_score = 80
        elif open_issues <= 30:
            issue_score = 60
        else:
            issue_score = 40
        
        return (watcher_score * 0.5 + issue_score * 0.5)
    
    def _analyze_organization(self):
        """Score based on repository structure"""
        score = 50  # Base score
        
        # Check for common organizational files
        file_names = [item.get('name', '').lower() for item in self.contents]
        
        if any('src' in name or 'lib' in name for name in file_names):
            score += 15
        if any('test' in name for name in file_names):
            score += 15
        if any('doc' in name for name in file_names):
            score += 10
        if any('.gitignore' in name for name in file_names):
            score += 10
        
        return min(100, score)

# ============================================
# FILE: analysis/structure_analysis.py
# ============================================
class StructureAnalyzer:
    """Analyze project structure and organization"""
    
    def __init__(self, repo_data, contents):
        self.repo_data = repo_data
        self.contents = contents
    
    def analyze(self):
        """
        Analyze project structure
        
        Returns:
            dict: Structure analysis with score
        """
        scores = []
        details = {}
        
        # 1. Has description (20%)
        has_description = bool(self.repo_data.get('description'))
        desc_score = 100 if has_description else 30
        scores.append(desc_score * 0.20)
        details['has_description'] = has_description
        
        # 2. Has license (25%)
        has_license = self.repo_data.get('license') is not None
        license_score = 100 if has_license else 0
        scores.append(license_score * 0.25)
        details['has_license'] = has_license
        
        # 3. File organization (30%)
        org_score = self._check_organization()
        scores.append(org_score * 0.30)
        details['organization_score'] = org_score
        
        # 4. Essential files (25%)
        essential_score = self._check_essential_files()
        scores.append(essential_score * 0.25)
        details['essential_files_score'] = essential_score
        
        final_score = sum(scores)
        
        return {
            'score': round(final_score, 2),
            'details': details
        }
    
    def _check_organization(self):
        """Check for organized folder structure"""
        file_names = [item.get('name', '').lower() for item in self.contents]
        
        score = 40  # Base score
        
        # Check for common directories
        if any('src' in name or 'source' in name for name in file_names):
            score += 20
        if any('test' in name for name in file_names):
            score += 20
        if any('docs' in name or 'documentation' in name for name in file_names):
            score += 10
        if any('examples' in name for name in file_names):
            score += 10
        
        return min(100, score)
    
    def _check_essential_files(self):
        """Check for essential project files"""
        file_names = [item.get('name', '').lower() for item in self.contents]
        
        score = 0
        
        # README
        if any('readme' in name for name in file_names):
            score += 30
        
        # .gitignore
        if '.gitignore' in file_names:
            score += 20
        
        # License
        if any('license' in name or 'licence' in name for name in file_names):
            score += 20
        
        # Contributing guide
        if any('contributing' in name for name in file_names):
            score += 15
        
        # Package/dependency file
        if any(name in file_names for name in ['package.json', 'requirements.txt', 'pom.xml', 'cargo.toml']):
            score += 15
        
        return min(100, score)