"""Game item model"""
from datetime import datetime


class GameItem:
    """Represents a game in the launcher"""
    
    def __init__(self, name, url, icon_url, category, description, difficulty):
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.category = category
        self.description = description
        self.difficulty = difficulty
        self.icon = None
        self.favorite = False
        self.play_count = 0
        self.total_time = 0
        self.last_played = None
        self.rating = 0
        self.notes = ""
        self.achievements_unlocked = []
        self.best_score = 0
        self.streak = 0
        self.local_path = None  # Path to downloaded local files
        self.is_downloaded = False  # Whether game is downloaded locally
        self.tags = []  # User-defined tags
        self.custom_name = None  # Custom name for the game
        self.play_sessions = []  # List of play session timestamps
        self.last_completed_date = None  # Last date game was completed
        self.completion_count = 0  # Number of times game was completed
        self.high_score = 0  # High score (if applicable)
        self.favorite_date = None  # Date when marked as favorite
        self.download_date = None  # Date when downloaded
        self.download_size = 0  # Size of downloaded files in bytes

