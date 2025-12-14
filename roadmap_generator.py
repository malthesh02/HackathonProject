class RoadmapGenerator:
    """Generate personalized improvement roadmap"""
    
    def __init__(self, scores, analysis_results):
        self.scores = scores
        self.results = analysis_results
    
    def generate(self):
        """
        Generate prioritized roadmap
        
        Returns:
            list: Prioritized action items
        """
        roadmap = []
        category_scores = self.scores['category_scores']
        
        # Sort by priority (lowest scores first)
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1]
        )
        
        for category, score in sorted_categories:
            if score < 80:  # Room for improvement
                items = self._generate_category_roadmap(category, score)
                roadmap.extend(items)
        
        # If everything is good, suggest advanced improvements
        if not roadmap:
            roadmap = self._generate_advanced_roadmap()
        
        return roadmap[:6]  # Return top 6 items
    
    def _generate_category_roadmap(self, category, score):
        """Generate roadmap items for specific category"""
        
        roadmaps = {
            'code_quality': [
                {
                    'category': 'Code Quality',
                    'priority': 'High' if score < 50 else 'Medium',
                    'action': 'Implement code linting (ESLint, Pylint, etc.) to maintain code standards',
                    'why': 'Clean, consistent code is the first thing recruiters notice',
                    'impact': 'High'
                },
                {
                    'category': 'Code Quality',
                    'priority': 'Medium',
                    'action': 'Add inline comments explaining complex logic',
                    'why': 'Shows communication skills and consideration for other developers',
                    'impact': 'Medium'
                }
            ],
            'project_structure': [
                {
                    'category': 'Project Structure',
                    'priority': 'High' if score < 50 else 'Medium',
                    'action': 'Add LICENSE file and choose appropriate open source license',
                    'why': 'Demonstrates understanding of legal aspects of software development',
                    'impact': 'Medium'
                },
                {
                    'category': 'Project Structure',
                    'priority': 'Medium',
                    'action': 'Organize code into logical directories (src/, tests/, docs/)',
                    'why': 'Professional structure makes projects easier to navigate',
                    'impact': 'High'
                }
            ],
            'documentation': [
                {
                    'category': 'Documentation',
                    'priority': 'High',
                    'action': 'Create comprehensive README with installation, usage, and examples',
                    'why': 'Documentation is often the first impression - make it count',
                    'impact': 'Very High'
                },
                {
                    'category': 'Documentation',
                    'priority': 'Medium',
                    'action': 'Add inline code documentation and API references',
                    'why': 'Shows thoroughness and makes your code more maintainable',
                    'impact': 'Medium'
                }
            ],
            'testing': [
                {
                    'category': 'Testing',
                    'priority': 'High',
                    'action': 'Write unit tests for core functionality (aim for 70%+ coverage)',
                    'why': 'Tests prove your code works and shows professional development practices',
                    'impact': 'Very High'
                },
                {
                    'category': 'Testing',
                    'priority': 'Medium',
                    'action': 'Set up CI/CD pipeline (GitHub Actions, Travis CI)',
                    'why': 'Automated testing shows understanding of modern DevOps practices',
                    'impact': 'High'
                }
            ],
            'git_behavior': [
                {
                    'category': 'Git Practices',
                    'priority': 'Medium',
                    'action': 'Write clear, descriptive commit messages (use conventional commits)',
                    'why': 'Good commit history shows attention to detail and professionalism',
                    'impact': 'Medium'
                },
                {
                    'category': 'Git Practices',
                    'priority': 'Low',
                    'action': 'Make regular commits showing iterative development',
                    'why': 'Consistent commits prove active development vs. single dump',
                    'impact': 'Medium'
                }
            ],
            'real_world_value': [
                {
                    'category': 'Impact',
                    'priority': 'Low',
                    'action': 'Add screenshots, demos, or live deployment links',
                    'why': 'Visual proof makes your project more impressive and shareable',
                    'impact': 'High'
                },
                {
                    'category': 'Impact',
                    'priority': 'Low',
                    'action': 'Write blog post or create video demo of your project',
                    'why': 'Shows communication skills and increases project visibility',
                    'impact': 'Medium'
                }
            ]
        }
        
        return roadmaps.get(category, [])
    
    def _generate_advanced_roadmap(self):
        """Generate roadmap for already-strong projects"""
        return [
            {
                'category': 'Enhancement',
                'priority': 'Low',
                'action': 'Add contribution guidelines (CONTRIBUTING.md)',
                'why': 'Shows readiness for collaborative development',
                'impact': 'Medium'
            },
            {
                'category': 'Enhancement',
                'priority': 'Low',
                'action': 'Implement automated code quality checks',
                'why': 'Demonstrates commitment to maintaining high standards',
                'impact': 'Medium'
            },
            {
                'category': 'Enhancement',
                'priority': 'Low',
                'action': 'Create comprehensive architecture documentation',
                'why': 'Shows system design thinking',
                'impact': 'High'
            }
        ]
