from flask import Flask, render_template, request, jsonify
from config import Config
from utils.repo_parser import RepoParser
from github.repo_fetcher import RepoFetcher
from github.commit_fetcher import CommitFetcher
from github.language_fetcher import LanguageFetcher
from analysis.code_quality import CodeQualityAnalyzer
from analysis.structure_analysis import StructureAnalyzer
from analysis.documentation import DocumentationAnalyzer
from analysis.testing_analysis import TestingAnalyzer
from analysis.git_behavior import GitBehaviorAnalyzer
from scoring.score_calculator import ScoreCalculator
from intelligence.summary_generator import SummaryGenerator
from intelligence.roadmap_generator import RoadmapGenerator

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """
    Main endpoint to analyze a GitHub repository
    
    Request body:
        {
            "repo_url": "https://github.com/owner/repo"
        }
    
    Returns:
        JSON with analysis results, scores, summary, and roadmap
    """
    try:
        data = request.get_json()
        repo_url = data.get('repo_url', '').strip()
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Parse repository URL
        try:
            owner, repo = RepoParser.parse_url(repo_url)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Initialize fetchers
        repo_fetcher = RepoFetcher()
        commit_fetcher = CommitFetcher()
        language_fetcher = LanguageFetcher()
        
        # Fetch all data
        print(f"Fetching data for {owner}/{repo}...")
        
        repo_data = repo_fetcher.fetch_repo_info(owner, repo)
        readme_data = repo_fetcher.fetch_readme(owner, repo)
        contents = repo_fetcher.fetch_contents(owner, repo)
        commits = commit_fetcher.fetch_commits(owner, repo)
        contributors = commit_fetcher.fetch_contributors(owner, repo)
        languages = language_fetcher.fetch_languages(owner, repo)
        
        # Run all analyses
        print("Running analyses...")
        
        code_quality = CodeQualityAnalyzer(repo_data, languages, contents).analyze()
        structure = StructureAnalyzer(repo_data, contents).analyze()
        documentation = DocumentationAnalyzer(readme_data, repo_data).analyze()
        testing = TestingAnalyzer(contents, repo_data).analyze()
        git_behavior = GitBehaviorAnalyzer(commits, contributors, repo_data).analyze()
        
        # Calculate real-world value score
        real_world_value = calculate_real_world_value(repo_data)
        
        # Compile all results
        analysis_results = {
            'code_quality': code_quality,
            'structure': structure,
            'documentation': documentation,
            'testing': testing,
            'git_behavior': git_behavior,
            'real_world_value': real_world_value
        }
        
        # Calculate final scores
        calculator = ScoreCalculator(analysis_results)
        scores = calculator.calculate_final_score()
        
        # Generate intelligence
        summary_gen = SummaryGenerator(repo_data, scores, analysis_results)
        summary = summary_gen.generate()
        
        roadmap_gen = RoadmapGenerator(scores, analysis_results)
        roadmap = roadmap_gen.generate()
        
        # Compile response
        response = {
            'repository': {
                'name': repo_data.get('name'),
                'full_name': repo_data.get('full_name'),
                'description': repo_data.get('description'),
                'url': repo_data.get('html_url'),
                'stars': repo_data.get('stargazers_count'),
                'forks': repo_data.get('forks_count'),
                'watchers': repo_data.get('watchers_count'),
                'open_issues': repo_data.get('open_issues_count'),
                'language': repo_data.get('language'),
                'created_at': repo_data.get('created_at'),
                'updated_at': repo_data.get('updated_at')
            },
            'scores': scores,
            'analysis': analysis_results,
            'summary': summary,
            'roadmap': roadmap,
            'metadata': {
                'total_commits': len(commits),
                'total_contributors': len(contributors),
                'languages': languages
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def calculate_real_world_value(repo_data):
    """Calculate real-world value score"""
    stars = repo_data.get('stargazers_count', 0)
    forks = repo_data.get('forks_count', 0)
    watchers = repo_data.get('watchers_count', 0)
    
    # Weighted calculation
    star_score = min(100, stars * 5)
    fork_score = min(100, forks * 10)
    watcher_score = min(100, watchers * 5)
    
    final = (star_score * 0.5 + fork_score * 0.3 + watcher_score * 0.2)
    
    return round(final, 2)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'RepoMirror API'})

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)