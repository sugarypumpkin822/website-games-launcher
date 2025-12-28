"""Daily challenge generator"""
import random
from datetime import datetime
from models.daily_challenge import DailyChallenge


class DailyChallengeGenerator:
    """Generates daily challenges"""
    
    @staticmethod
    def generate(game_manager):
        """Generate a daily challenge"""
        today = datetime.now().date()
        
        # Use date as seed for consistent daily challenge
        random.seed(today.toordinal())
        
        game = random.choice(game_manager.games)
        
        challenges = [
            f"Play {game.name} and serve 10 perfect orders!",
            f"Beat your best score in {game.name}!",
            f"Play {game.name} for at least 15 minutes!",
            f"Try {game.name} if you haven't played it yet!",
            f"Get a 5-star rating on 3 orders in {game.name}!",
        ]
        
        challenge_text = random.choice(challenges)
        
        # Reset random seed
        random.seed()
        
        return DailyChallenge(today, game, challenge_text)

