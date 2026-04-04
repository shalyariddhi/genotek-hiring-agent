import json

class HiringBrain:
    def __init__(self, data_path="data/candidates.json"):
        with open(data_path, "r") as f:
            self.candidates = json.load(f)

    def is_ai_generated(self, text):
        # ANTI-CHEAT: GPT answers usually lack "Personal Scars"
        markers = ["delighted to apply", "extensive experience", "passionate about"]
        score = sum(1 for m in markers if m in text.lower())
        return score >= 2

    def score_candidate(self, c):
        score = 0
        # HEURISTIC 1: Technical Depth (Checks for specific tool mentions)
        if any(tech in c['technical_answer'].lower() for tech in ['fastapi', 'sqlalchemy', 'playwright']):
            score += 50
        
        # HEURISTIC 2: Hunger (Recent GitHub Activity)
        if c.get('github_commits_last_30d', 0) > 20:
            score += 30

        # HEURISTIC 3: AI Penalty
        if self.is_ai_generated(c['technical_answer']):
            score -= 60
            
        return score

    def get_top_picks(self):
        return sorted(self.candidates, key=self.score_candidate, reverse=True)[:2]