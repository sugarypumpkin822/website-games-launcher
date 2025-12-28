"""Achievement management"""
from datetime import datetime
from models.achievement import Achievement


class AchievementManager:
    """Manages achievements"""
    
    def __init__(self, game_manager, settings_manager):
        self.game_manager = game_manager
        self.settings_manager = settings_manager
        self.achievements = self._initialize_achievements()
    
    def _initialize_achievements(self):
        """Initialize achievements"""
        return [
            Achievement("first_play", "First Steps", "Play your first game", "🎮", 
                      lambda: self.game_manager.total_games_played() >= 1),
            Achievement("play_10", "Getting Started", "Play 10 games total", "🏆", 
                      lambda: self.game_manager.total_games_played() >= 10),
            Achievement("play_50", "Dedicated Player", "Play 50 games total", "🌟", 
                      lambda: self.game_manager.total_games_played() >= 50),
            Achievement("play_100", "Century Club", "Play 100 games total", "💯", 
                      lambda: self.game_manager.total_games_played() >= 100),
            Achievement("hour_1", "Time Flies", "Play for 1 hour total", "⏰", 
                      lambda: self.game_manager.total_play_time() >= 3600),
            Achievement("hour_10", "Committed Gamer", "Play for 10 hours total", "⏳", 
                      lambda: self.game_manager.total_play_time() >= 36000),
            Achievement("all_games", "Completionist", "Play all games at least once", "🎯", 
                      lambda: all(g.play_count > 0 for g in self.game_manager.games)),
            Achievement("favorite_5", "Curator", "Mark 5 games as favorites", "⭐", 
                      lambda: sum(1 for g in self.game_manager.games if g.favorite) >= 5),
            Achievement("rate_all", "Critic", "Rate all games", "📝", 
                      lambda: all(g.rating > 0 for g in self.game_manager.games)),
            Achievement("streak_7", "Week Warrior", "Play for 7 days in a row", "🔥", 
                      lambda: max((g.streak for g in self.game_manager.games), default=0) >= 7),
            Achievement("master", "Papa's Master", "Reach level 20", "👑", 
                      lambda: self.settings_manager.get('user_level', 1) >= 20),
        ]
    
    def load_achievements(self, data):
        """Load achievements from data"""
        achievements_data = data.get('achievements', {})
        for achievement in self.achievements:
            ach_data = achievements_data.get(achievement.id, {})
            achievement.unlocked = ach_data.get('unlocked', False)
            if ach_data.get('unlock_date'):
                achievement.unlock_date = datetime.fromisoformat(ach_data['unlock_date'])
    
    def save_achievements(self):
        """Save achievements to data structure"""
        data = {}
        for achievement in self.achievements:
            data[achievement.id] = {
                'unlocked': achievement.unlocked,
                'unlock_date': achievement.unlock_date.isoformat() if achievement.unlock_date else None
            }
        return data
    
    def check_achievements(self):
        """Check and unlock achievements"""
        newly_unlocked = []
        
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.requirement():
                achievement.unlocked = True
                achievement.unlock_date = datetime.now()
                newly_unlocked.append(achievement)
        
        return newly_unlocked

