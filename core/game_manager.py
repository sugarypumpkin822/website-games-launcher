"""Game management"""
import json
from datetime import datetime
from pathlib import Path
from models.game_item import GameItem


class GameManager:
    """Manages game data and statistics"""
    
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.games = self._initialize_games()
        self.data_file = self.settings_manager.settings_file.parent / "game_data.json"
        self.load_game_data()
    
    def _initialize_games(self):
        """Initialize the list of games"""
        return [
            GameItem("PAPA'S WINGERIA", "https://poki.com/en/g/papas-wingeria", 
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/8c233a966eb3e3f5b14edab1fe14e1b8.png",
                    "Restaurant", "Serve delicious chicken wings to hungry customers!", "Medium"),
            GameItem("PAPA'S FREEZERIA", "https://poki.com/en/g/papas-freezeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/72db30c0d3584e29927cd2c8c0beb0db.png",
                    "Dessert", "Mix and serve ice cream sundaes on a tropical island!", "Easy"),
            GameItem("PAPA'S SUSHIRIA", "https://poki.com/en/g/papas-sushiria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/5c8ebb0e1f33d5f3f88f57e3f16df6e1.png",
                    "Restaurant", "Prepare authentic sushi rolls for demanding customers!", "Hard"),
            GameItem("PAPA'S PASTARIA", "https://poki.com/en/g/papas-pastaria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/398c96ccdda9a6e4f5e8e6b0cd23fb83.png",
                    "Restaurant", "Cook perfect pasta dishes in this Italian restaurant!", "Medium"),
            GameItem("PAPA'S PANCAKERIA", "https://poki.com/en/g/papas-pancakeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/b0a624f8c4ff7c91f0d7e9fbb5c0f9f3.png",
                    "Breakfast", "Flip pancakes and serve breakfast combos!", "Easy"),
            GameItem("PAPA'S DONUTERIA", "https://poki.com/en/g/papas-donuteria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/d9aa1c8ec8f7f8b7c17ae9c7e5c4b5c8.png",
                    "Dessert", "Fry and decorate delicious donuts!", "Medium"),
            GameItem("PAPA'S BAKERIA", "https://poki.com/en/g/papas-bakeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/e7e1f8c89c8e8e8e8e8e8e8e8e8e8e8e.png",
                    "Bakery", "Bake fresh pies and artisan breads!", "Medium"),
            GameItem("PAPA'S TACO MIA", "https://poki.com/en/g/papas-taco-mia",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.png",
                    "Mexican", "Create amazing tacos with custom toppings!", "Medium"),
            GameItem("PAPA'S CUPCAKERIA", "https://poki.com/en/g/papas-cupcakeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/f6e5d4c3b2a1f9e8d7c6b5a4f3e2d1c0.png",
                    "Dessert", "Bake and decorate beautiful cupcakes!", "Easy"),
            GameItem("PAPA'S HOTDOGGERIA", "https://poki.com/en/g/papas-hot-doggeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4.png",
                    "Fast Food", "Grill hot dogs at a bustling baseball stadium!", "Hard"),
            GameItem("PAPA'S BURGERIA", "https://poki.com/en/g/papas-burgeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/d4c5b6a7f8e9d0c1b2a3f4e5d6c7b8a9.png",
                    "Fast Food", "Build perfect burgers for hungry customers!", "Medium"),
            GameItem("PAPA'S PIZZERIA", "https://poki.com/en/g/papas-pizzeria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3.png",
                    "Italian", "The classic! Make pizzas and manage the restaurant!", "Easy"),
            GameItem("PAPA'S CHEESERIA", "https://poki.com/en/g/papas-cheeseria",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7.png",
                    "Fast Food", "Create gourmet grilled cheese sandwiches!", "Medium"),
            GameItem("PAPA LOUIE: WHEN PIZZAS ATTACK", "https://poki.com/en/g/papa-louie-when-pizzas-attack",
                    "https://img.poki.com/cdn-cgi/image/quality=78,width=204,height=204,fit=cover,f=auto/e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4.png",
                    "Adventure", "Action platformer - fight evil pizza monsters!", "Hard"),
        ]
    
    def load_game_data(self):
        """Load game data from file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for game in self.games:
                        game_data = data.get(game.name, {})
                        game.favorite = game_data.get('favorite', False)
                        game.play_count = game_data.get('play_count', 0)
                        game.total_time = game_data.get('total_time', 0)
                        game.rating = game_data.get('rating', 0)
                        game.notes = game_data.get('notes', '')
                        game.achievements_unlocked = game_data.get('achievements_unlocked', [])
                        game.best_score = game_data.get('best_score', 0)
                        game.streak = game_data.get('streak', 0)
                        game.local_path = game_data.get('local_path')
                        game.is_downloaded = game_data.get('is_downloaded', False)
                        last_played = game_data.get('last_played')
                        if last_played:
                            game.last_played = datetime.fromisoformat(last_played)
        except:
            pass
    
    def save_game_data(self):
        """Save game data to file"""
        try:
            data = {}
            for game in self.games:
                data[game.name] = {
                    'favorite': game.favorite,
                    'play_count': game.play_count,
                    'total_time': game.total_time,
                    'rating': game.rating,
                    'notes': game.notes,
                    'achievements_unlocked': game.achievements_unlocked,
                    'best_score': game.best_score,
                    'streak': game.streak,
                    'local_path': game.local_path,
                    'is_downloaded': game.is_downloaded,
                    'last_played': game.last_played.isoformat() if game.last_played else None
                }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def total_games_played(self):
        """Get total number of games played"""
        return sum(g.play_count for g in self.games)
    
    def total_play_time(self):
        """Get total play time in seconds"""
        return sum(g.total_time for g in self.games)
    
    def get_most_played_game(self):
        """Get the most played game"""
        if not self.games:
            return None
        return max(self.games, key=lambda g: g.play_count)
    
    def get_longest_play_time_game(self):
        """Get game with longest play time"""
        if not self.games:
            return None
        return max(self.games, key=lambda g: g.total_time)
    
    def get_highest_rated_game(self):
        """Get highest rated game"""
        if not self.games:
            return None
        rated_games = [g for g in self.games if g.rating > 0]
        if not rated_games:
            return None
        return max(rated_games, key=lambda g: g.rating)
    
    def get_favorite_games(self):
        """Get list of favorite games"""
        return [g for g in self.games if g.favorite]
    
    def get_downloaded_games(self):
        """Get list of downloaded games"""
        return [g for g in self.games if g.is_downloaded]
    
    def get_unplayed_games(self):
        """Get list of unplayed games"""
        return [g for g in self.games if g.play_count == 0]
    
    def get_games_by_category(self, category):
        """Get games by category"""
        return [g for g in self.games if g.category == category]
    
    def get_games_by_difficulty(self, difficulty):
        """Get games by difficulty"""
        return [g for g in self.games if g.difficulty == difficulty]
    
    def get_average_rating(self):
        """Get average rating of all rated games"""
        rated_games = [g for g in self.games if g.rating > 0]
        if not rated_games:
            return 0.0
        return sum(g.rating for g in rated_games) / len(rated_games)
    
    def get_total_streak(self):
        """Get total streak across all games"""
        return sum(g.streak for g in self.games)
    
    def get_longest_streak(self):
        """Get longest streak"""
        if not self.games:
            return 0
        return max((g.streak for g in self.games), default=0)

