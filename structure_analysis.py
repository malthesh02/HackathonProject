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