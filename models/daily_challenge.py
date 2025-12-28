"""Daily challenge model"""
from datetime import datetime


class DailyChallenge:
    """Represents a daily challenge"""
    
    def __init__(self, date, game, challenge_text):
        self.date = date
        self.game = game
        self.challenge_text = challenge_text
        self.completed = False

