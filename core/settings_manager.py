"""Settings management"""
import json
from pathlib import Path


class SettingsManager:
    """Manages application settings"""
    
    def __init__(self):
        self.settings_file = Path.home() / ".papas_launcher" / "settings.json"
        self.settings_file.parent.mkdir(exist_ok=True)
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            'theme': 'light',
            'check_updates': True,
            'sound_enabled': True,
            'notifications_enabled': True,
            'play_reminder_minutes': 60,
            'volume': 50,
            'auto_save': True,
            'show_tips': True,
            'performance_mode': False,
            'welcomed': False,
            'username': 'Player',
            'user_level': 1,
            'total_xp': 0,
            'download_games_locally': False,  # New setting for local downloads
            'cache_dir': str(self.settings_file.parent / "cache"),
            'auto_download_on_play': False,  # Auto-download when playing
            'show_notifications': True,  # Show system notifications
            'minimize_to_tray': True,  # Minimize to system tray
            'start_minimized': False,  # Start application minimized
            'remember_window_size': True,  # Remember window size
            'window_width': 1700,  # Default window width
            'window_height': 1000,  # Default window height
            'game_auto_save_interval': 60,  # Auto-save interval in seconds
            'enable_sound_effects': True,  # Enable sound effects
            'enable_animations': True,  # Enable UI animations
            'compact_mode': False,  # Compact UI mode
            'show_game_preview': True,  # Show game preview in list
            'default_view_mode': 'list',  # Default view mode: list or grid
            'auto_download_updates': False  # Auto-download updates when available
        }
        
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    return {**default_settings, **loaded}
            else:
                settings = default_settings.copy()
                self.save_settings(settings)
                return settings
        except:
            return default_settings.copy()
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        if settings is None:
            settings = self.settings
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except:
            pass
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def get_cache_dir(self):
        """Get cache directory path"""
        cache_dir = Path(self.get('cache_dir', str(self.settings_file.parent / "cache")))
        cache_dir.mkdir(exist_ok=True, parents=True)
        return cache_dir

