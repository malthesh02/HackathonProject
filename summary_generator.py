class SummaryGenerator:
    """Generate AI-style summary of repository"""
    
    def __init__(self, repo_data, scores, analysis_results):
        self.repo = repo_data
        self.scores = scores
        self.results = analysis_results
    
    def generate(self):
        """
        Generate comprehensive summary
        
        Returns:
            dict: Summary with tone, strengths, and weaknesses
        """
        final_score = self.scores['final_score']
        
        # Determine overall tone
        tone = self._generate_tone(final_score)
        
        # Identify strengths and weaknesses
        strengths = self._identify_strengths()
        weaknesses = self._identify_weaknesses()
        
        # Generate recruiter perspective
        recruiter_view = self._generate_recruiter_view(final_score, strengths, weaknesses)
        
        return {
            'tone': tone,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recruiter_perspective': recruiter_view,
            'one_liner': self._generate_one_liner(final_score)
        }
    
    def _generate_tone(self, score):
        """Generate overall assessment tone"""
        if score >= 85:
            return f"Outstanding repository demonstrating professional-grade development practices. This project stands out with a score of {score}/100."
        elif score >= 70:
            return f"Strong repository with solid fundamentals. With a score of {score}/100, this project shows good engineering practices."
        elif score >= 55:
            return f"Developing project with potential. Scoring {score}/100, there are clear areas for improvement to make this production-ready."
        elif score >= 40:
            return f"Early-stage project needing significant development. At {score}/100, focus on foundational improvements."
        else:
            return f"Project in initial stages requiring substantial work. Current score of {score}/100 indicates need for comprehensive improvements."
    
    def _identify_strengths(self):
        """Identify top 3 strengths"""
        category_scores = self.scores['category_scores']
        
        # Sort categories by score
        sorted_categories = sorted(
            category_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        strengths = []
        for category, score in sorted_categories[:3]:
            if score >= 70:
                strength_text = self._get_strength_description(category, score)
                strengths.append(strength_text)
        
        return strengths if strengths else ["Basic project setup"]
    
    def _identify_weaknesses(self):
        """Identify top 3 weaknesses"""
        category_scores = self.scores['category_scores']
        
        # Sort categories by score (ascending)
        sorted_categories = sorted(
            category_scores.items(), 
            key=lambda x: x[1]
        )
        
        weaknesses = []
        for category, score in sorted_categories[:3]:
            if score < 70:
                weakness_text = self._get_weakness_description(category, score)
                weaknesses.append(weakness_text)
        
        return weaknesses if weaknesses else ["Minor refinements needed"]
    
    def _get_strength_description(self, category, score):
        """Get human-readable strength description"""
        descriptions = {
            'code_quality': f'Excellent code quality with score of {score}/100',
            'project_structure': f'Well-organized project structure ({score}/100)',
            'documentation': f'Comprehensive documentation ({score}/100)',
            'testing': f'Strong testing practices ({score}/100)',
            'git_behavior': f'Consistent Git workflow ({score}/100)',
            'real_world_value': f'High real-world impact ({score}/100)'
        }
        return descriptions.get(category, f'{category}: {score}/100')
    
    def _get_weakness_description(self, category, score):
        """Get human-readable weakness description"""
        descriptions = {
            'code_quality': f'Code quality needs improvement (currently {score}/100)',
            'project_structure': f'Project organization could be better ({score}/100)',
            'documentation': f'Documentation is lacking ({score}/100)',
            'testing': f'Testing coverage is insufficient ({score}/100)',
            'git_behavior': f'Git practices need work ({score}/100)',
            'real_world_value': f'Limited real-world traction ({score}/100)'
        }
        return descriptions.get(category, f'{category}: {score}/100')
    
    def _generate_recruiter_view(self, score, strengths, weaknesses):
        """Generate what a recruiter would think"""
        if score >= 80:
            return "This candidate demonstrates strong technical skills and attention to professional standards. The project shows production-ready thinking."
        elif score >= 65:
            return "This candidate shows good potential with solid fundamentals. Some areas need refinement for production environments."
        elif score >= 50:
            return "This candidate is developing their skills. The project shows promise but needs more professional polish."
        else:
            return "This candidate is early in their development journey. Significant growth needed to meet professional standards."
    
    def _generate_one_liner(self, score):
        """Generate catchy one-liner"""
        if score >= 85:
            return "🌟 Production-ready project with professional standards"
        elif score >= 70:
            return "✅ Solid project ready for portfolio showcase"
        elif score >= 55:
            return "🔨 Good foundation, needs polish for production"
        elif score >= 40:
            return "🌱 Growing project with room for improvement"
        else:
            return "🚧 Early-stage project requiring development"