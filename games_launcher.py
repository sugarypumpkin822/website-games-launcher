import sys
import json
import os
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QLabel, QLineEdit, QSplitter, QMessageBox, QTabWidget,
                             QTextEdit, QProgressBar, QComboBox, QCheckBox, QDialog,
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                             QSlider, QSystemTrayIcon, QMenu, QScrollArea, QGridLayout,
                             QFileDialog, QInputDialog, QCalendarWidget, QGroupBox,
                             QRadioButton, QSpinBox, QDialogButtonBox, QToolButton)
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PyQt6.QtGui import QPixmap, QIcon, QImage, QPalette, QColor, QFont, QAction, QPainter, QLinearGradient, QBrush, QPen, QShortcut, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str)
    
    def __init__(self, current_version, repo_url):
        super().__init__()
        self.current_version = current_version
        self.repo_url = repo_url
    
    def run(self):
        try:
            parts = self.repo_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                api_url = f"https://api.github.com/repos/{parts[0]}/{parts[1]}/releases/latest"
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data.get('tag_name', '').replace('v', '')
                    if latest_version and latest_version > self.current_version:
                        self.update_available.emit(latest_version, data.get('html_url', ''))
        except:
            pass

class GameItem:
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

class Achievement:
    def __init__(self, id, name, description, icon, requirement):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.requirement = requirement
        self.unlocked = False
        self.unlock_date = None

class DailyChallenge:
    def __init__(self, date, game, challenge_text):
        self.date = date
        self.game = game
        self.challenge_text = challenge_text
        self.completed = False

class PapasGamesLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # App metadata
        self.version = "2.0.0"
        self.github_repo = "https://github.com/sugarypumpkin822/papas-games-launcher"
        
        self.setWindowTitle(f"🎮 Papa's Games Launcher v{self.version}")
        self.setGeometry(100, 100, 1700, 1000)
        
        # User profile
        self.username = "Player"
        self.user_level = 1
        self.total_xp = 0
        
        # Settings
        self.settings_file = Path.home() / ".papas_launcher" / "settings.json"
        self.settings_file.parent.mkdir(exist_ok=True)
        self.load_settings()
        
        # Games data with difficulty levels
        self.games = [
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
        
        # Achievements
        self.achievements = [
            Achievement("first_play", "First Steps", "Play your first game", "🎮", lambda: self.total_games_played() >= 1),
            Achievement("play_10", "Getting Started", "Play 10 games total", "🏆", lambda: self.total_games_played() >= 10),
            Achievement("play_50", "Dedicated Player", "Play 50 games total", "🌟", lambda: self.total_games_played() >= 50),
            Achievement("play_100", "Century Club", "Play 100 games total", "💯", lambda: self.total_games_played() >= 100),
            Achievement("hour_1", "Time Flies", "Play for 1 hour total", "⏰", lambda: self.total_play_time() >= 3600),
            Achievement("hour_10", "Committed Gamer", "Play for 10 hours total", "⏳", lambda: self.total_play_time() >= 36000),
            Achievement("all_games", "Completionist", "Play all games at least once", "🎯", lambda: all(g.play_count > 0 for g in self.games)),
            Achievement("favorite_5", "Curator", "Mark 5 games as favorites", "⭐", lambda: sum(1 for g in self.games if g.favorite) >= 5),
            Achievement("rate_all", "Critic", "Rate all games", "📝", lambda: all(g.rating > 0 for g in self.games)),
            Achievement("streak_7", "Week Warrior", "Play for 7 days in a row", "🔥", lambda: max((g.streak for g in self.games), default=0) >= 7),
            Achievement("master", "Papa's Master", "Reach level 20", "👑", lambda: self.user_level >= 20),
        ]
        
        self.daily_challenge = None
        self.current_game = None
        self.game_start_time = None
        
        # Themes
        self.available_themes = {
            'light': {'name': 'Light', 'emoji': '☀️'},
            'dark': {'name': 'Dark', 'emoji': '🌙'},
            'ocean': {'name': 'Ocean Blue', 'emoji': '🌊'},
            'forest': {'name': 'Forest Green', 'emoji': '🌲'},
            'sunset': {'name': 'Sunset Orange', 'emoji': '🌅'},
            'purple': {'name': 'Royal Purple', 'emoji': '👑'},
        }
        
        # Networking
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_icon_downloaded)
        self.pending_requests = {}
        
        # Timers
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.update_play_time)
        
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.show_play_reminder)
        
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(100)
        
        # System tray
        self.setup_system_tray()
        
        # Shortcuts
        self.setup_shortcuts()
        
        self.init_ui()
        self.load_icons()
        self.load_game_data()
        self.generate_daily_challenge()
        self.check_achievements()
        
        # Check for updates on startup
        if self.settings.get('check_updates', True):
            self.check_for_updates()
        
        # Show welcome message for first time users
        if not self.settings.get('welcomed', False):
            self.show_welcome_dialog()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        QShortcut(QKeySequence("Ctrl+F"), self, self.focus_search)
        QShortcut(QKeySequence("Ctrl+H"), self, self.go_home)
        QShortcut(QKeySequence("F11"), self, self.toggle_fullscreen)
        QShortcut(QKeySequence("Ctrl+S"), self, self.show_settings)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
    
    def focus_search(self):
        """Focus on search box"""
        self.tabs.setCurrentIndex(0)
        self.search_box.setFocus()
        self.search_box.selectAll()
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(52, 152, 219))
        self.tray_icon.setIcon(QIcon(pixmap))
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        
        random_game_action = QAction("Play Random Game", self)
        random_game_action.triggered.connect(self.play_random_game)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(random_game_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
    
    def load_settings(self):
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
            'total_xp': 0
        }
        
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    self.settings = {**default_settings, **loaded}
            else:
                self.settings = default_settings
                self.save_settings()
        except:
            self.settings = default_settings
        
        self.username = self.settings.get('username', 'Player')
        self.user_level = self.settings.get('user_level', 1)
        self.total_xp = self.settings.get('total_xp', 0)
    
    def save_settings(self):
        try:
            self.settings['username'] = self.username
            self.settings['user_level'] = self.user_level
            self.settings['total_xp'] = self.total_xp
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def load_game_data(self):
        data_file = self.settings_file.parent / "game_data.json"
        try:
            if data_file.exists():
                with open(data_file, 'r') as f:
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
                        last_played = game_data.get('last_played')
                        if last_played:
                            game.last_played = datetime.fromisoformat(last_played)
                    
                    # Load achievements
                    achievements_data = data.get('achievements', {})
                    for achievement in self.achievements:
                        ach_data = achievements_data.get(achievement.id, {})
                        achievement.unlocked = ach_data.get('unlocked', False)
                        if ach_data.get('unlock_date'):
                            achievement.unlock_date = datetime.fromisoformat(ach_data['unlock_date'])
        except:
            pass
    
    def save_game_data(self):
        data_file = self.settings_file.parent / "game_data.json"
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
                    'last_played': game.last_played.isoformat() if game.last_played else None
                }
            
            # Save achievements
            data['achievements'] = {}
            for achievement in self.achievements:
                data['achievements'][achievement.id] = {
                    'unlocked': achievement.unlocked,
                    'unlock_date': achievement.unlock_date.isoformat() if achievement.unlock_date else None
                }
            
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top toolbar with profile
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel("🎮 Papa's Games Launcher")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        toolbar_layout.addWidget(title_label)
        
        # User profile section
        self.profile_label = QLabel(f"👤 {self.username} | Level {self.user_level}")
        self.profile_label.setFont(QFont("Arial", 12))
        toolbar_layout.addWidget(self.profile_label)
        
        # XP Progress bar
        self.xp_progress = QProgressBar()
        self.xp_progress.setMaximum(self.xp_for_next_level())
        self.xp_progress.setValue(self.total_xp % self.xp_for_next_level())
        self.xp_progress.setFormat(f"{self.total_xp % self.xp_for_next_level()}/{self.xp_for_next_level()} XP")
        self.xp_progress.setFixedWidth(200)
        toolbar_layout.addWidget(self.xp_progress)
        
        toolbar_layout.addStretch()
        
        # Quick action buttons
        random_btn = QPushButton("🎲 Random")
        random_btn.setToolTip("Play a random game")
        random_btn.clicked.connect(self.play_random_game)
        toolbar_layout.addWidget(random_btn)
        
        export_btn = QPushButton("📊 Export")
        export_btn.setToolTip("Export your statistics")
        export_btn.clicked.connect(self.export_statistics)
        toolbar_layout.addWidget(export_btn)
        
        self.theme_btn = QPushButton("🌙 Theme")
        self.theme_btn.clicked.connect(self.show_theme_selector)
        toolbar_layout.addWidget(self.theme_btn)
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.show_settings)
        toolbar_layout.addWidget(settings_btn)
        
        update_btn = QPushButton("🔄 Update")
        update_btn.clicked.connect(self.check_for_updates)
        toolbar_layout.addWidget(update_btn)
        
        self.apply_toolbar_style(toolbar)
        main_layout.addWidget(toolbar)
        
        # Main content with tabs
        self.tabs = QTabWidget()
        
        # Games tab
        games_tab = self.create_games_tab()
        self.tabs.addTab(games_tab, "🎮 Games")
        
        # Favorites tab
        favorites_tab = self.create_favorites_tab()
        self.tabs.addTab(favorites_tab, "⭐ Favorites")
        
        # Statistics tab
        stats_tab = self.create_stats_tab()
        self.tabs.addTab(stats_tab, "📊 Statistics")
        
        # Achievements tab
        achievements_tab = self.create_achievements_tab()
        self.tabs.addTab(achievements_tab, "🏆 Achievements")
        
        # Daily Challenge tab
        challenge_tab = self.create_challenge_tab()
        self.tabs.addTab(challenge_tab, "🎯 Daily Challenge")
        
        # Recommendations tab
        recommendations_tab = self.create_recommendations_tab()
        self.tabs.addTab(recommendations_tab, "💡 For You")
        
        # About tab
        about_tab = self.create_about_tab()
        self.tabs.addTab(about_tab, "ℹ️ About")
        
        main_layout.addWidget(self.tabs)
        
        self.apply_theme()
    
    def create_games_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        # Filters
        filter_group = QGroupBox("🔍 Filters")
        filter_group_layout = QVBoxLayout()
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All", "Restaurant", "Fast Food", "Dessert", "Italian", "Mexican", "Breakfast", "Bakery", "Adventure"])
        self.category_filter.currentTextChanged.connect(self.filter_games)
        category_layout.addWidget(self.category_filter)
        filter_group_layout.addLayout(category_layout)
        
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_filter = QComboBox()
        self.difficulty_filter.addItems(["All", "Easy", "Medium", "Hard"])
        self.difficulty_filter.currentTextChanged.connect(self.filter_games)
        difficulty_layout.addWidget(self.difficulty_filter)
        filter_group_layout.addLayout(difficulty_layout)
        
        filter_group.setLayout(filter_group_layout)
        left_layout.addWidget(filter_group)
        
        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search games... (Ctrl+F)")
        self.search_box.textChanged.connect(self.filter_games)
        left_layout.addWidget(self.search_box)
        
        # Sort options
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(QLabel("Sort:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Most Played", "Recently Played", "Highest Rated", "Difficulty"])
        self.sort_combo.currentTextChanged.connect(self.sort_games)
        sort_layout.addWidget(self.sort_combo)
        left_layout.addLayout(sort_layout)
        
        # View options
        view_layout = QHBoxLayout()
        self.show_unplayed = QCheckBox("Show only unplayed")
        self.show_unplayed.stateChanged.connect(self.filter_games)
        view_layout.addWidget(self.show_unplayed)
        left_layout.addLayout(view_layout)
        
        # Game list
        self.game_list = QListWidget()
        self.game_list.setIconSize(QSize(64, 64))
        self.game_list.setSpacing(5)
        self.game_list.itemClicked.connect(self.on_game_selected)
        left_layout.addWidget(self.game_list)
        
        # Game info panel
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        
        self.game_title_label = QLabel("No game selected")
        self.game_title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        info_layout.addWidget(self.game_title_label)
        
        self.game_desc_label = QLabel("")
        self.game_desc_label.setWordWrap(True)
        info_layout.addWidget(self.game_desc_label)
        
        self.game_stats_label = QLabel("")
        info_layout.addWidget(self.game_stats_label)
        
        # Notes section
        notes_label = QLabel("📝 Notes:")
        info_layout.addWidget(notes_label)
        
        self.game_notes = QTextEdit()
        self.game_notes.setMaximumHeight(60)
        self.game_notes.setPlaceholderText("Add your notes about this game...")
        self.game_notes.textChanged.connect(self.save_game_notes)
        info_layout.addWidget(self.game_notes)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶️ Play")
        self.play_btn.clicked.connect(self.play_selected_game)
        action_layout.addWidget(self.play_btn)
        
        self.favorite_btn = QPushButton("⭐ Favorite")
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.clicked.connect(self.toggle_favorite)
        action_layout.addWidget(self.favorite_btn)
        
        info_layout.addLayout(action_layout)
        
        # Rating
        rating_layout = QHBoxLayout()
        rating_layout.addWidget(QLabel("Rating:"))
        self.rating_slider = QSlider(Qt.Orientation.Horizontal)
        self.rating_slider.setMinimum(0)
        self.rating_slider.setMaximum(5)
        self.rating_slider.valueChanged.connect(self.rate_game)
        rating_layout.addWidget(self.rating_slider)
        self.rating_label = QLabel("0/5")
        rating_layout.addWidget(self.rating_label)
        info_layout.addLayout(rating_layout)
        
        left_layout.addWidget(info_frame)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.home_btn = QPushButton("🏠 Home")
        self.home_btn.clicked.connect(self.go_home)
        control_layout.addWidget(self.home_btn)
        
        self.fullscreen_btn = QPushButton("⛶ Full")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        control_layout.addWidget(self.fullscreen_btn)
        
        screenshot_btn = QPushButton("📷 Screenshot")
        screenshot_btn.clicked.connect(self.take_screenshot)
        control_layout.addWidget(screenshot_btn)
        
        left_layout.addLayout(control_layout)
        
        self.status_label = QLabel("Ready")
        left_layout.addWidget(self.status_label)
        
        # Right panel - web view
        self.web_view = QWebEngineView()
        self.show_welcome_screen()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.web_view)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([450, 1250])
        
        layout.addWidget(splitter)
        
        self.populate_game_list()
        
        return widget
    
    def create_favorites_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("⭐ Your Favorite Games")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.favorites_list = QListWidget()
        self.favorites_list.setIconSize(QSize(64, 64))
        self.favorites_list.setSpacing(5)
        self.favorites_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.favorites_list.setGridSize(QSize(150, 150))
        self.favorites_list.itemDoubleClicked.connect(self.play_favorite)
        layout.addWidget(self.favorites_list)
        
        return widget
    
    def create_stats_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📊 Your Gaming Statistics")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Stats summary with cards
        cards_layout = QHBoxLayout()
        
        # Total plays card
        plays_card = self.create_stat_card("🎮 Total Plays", str(self.total_games_played()))
        cards_layout.addWidget(plays_card)
        
        # Total time card
        total_time = self.total_play_time()
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        time_card = self.create_stat_card("⏱️ Total Time", f"{hours}h {minutes}m")
        cards_layout.addWidget(time_card)
        
        # Favorites card
        fav_card = self.create_stat_card("⭐ Favorites", str(sum(1 for g in self.games if g.favorite)))
        cards_layout.addWidget(fav_card)
        
        # Achievement card
        unlocked = sum(1 for a in self.achievements if a.unlocked)
        ach_card = self.create_stat_card("🏆 Achievements", f"{unlocked}/{len(self.achievements)}")
        cards_layout.addWidget(ach_card)
        
        layout.addLayout(cards_layout)
        
        # Stats table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(6)
        self.stats_table.setHorizontalHeaderLabels(["Game", "Plays", "Time", "Last Played", "Rating", "Streak"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.stats_table)
        
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.update_statistics)
        btn_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def create_stat_card(self, title, value):
        """Create a statistic card"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(100)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return card
    
    def create_achievements_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("🏆 Achievements")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        unlocked = sum(1 for a in self.achievements if a.unlocked)
        progress_label = QLabel(f"Unlocked: {unlocked}/{len(self.achievements)}")
        progress_label.setFont(QFont("Arial", 14))
        layout.addWidget(progress_label)
        
        # Achievements list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        for achievement in self.achievements:
            ach_frame = QFrame()
            ach_frame.setFrameShape(QFrame.Shape.StyledPanel)
            ach_layout = QHBoxLayout(ach_frame)
            
            icon_label = QLabel(achievement.icon)
            icon_label.setFont(QFont("Arial", 32))
            ach_layout.addWidget(icon_label)
            
            info_layout = QVBoxLayout()
            name_label = QLabel(achievement.name)
            name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            info_layout.addWidget(name_label)
            
            desc_label = QLabel(achievement.description)
            info_layout.addWidget(desc_label)
            
            if achievement.unlocked:
                unlock_label = QLabel(f"✅ Unlocked: {achievement.unlock_date.strftime('%Y-%m-%d')}")
                unlock_label.setStyleSheet("color: green;")
                info_layout.addWidget(unlock_label)
            else:
                lock_label = QLabel("🔒 Locked")
                lock_label.setStyleSheet("color: gray;")
                info_layout.addWidget(lock_label)
            
            ach_layout.addLayout(info_layout)
            ach_layout.addStretch()
            
            scroll_layout.addWidget(ach_frame)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def create_challenge_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("🎯 Daily Challenge")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.challenge_frame = QFrame()
        self.challenge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        challenge_layout = QVBoxLayout(self.challenge_frame)
        
        self.challenge_date_label = QLabel()
        self.challenge_date_label.setFont(QFont("Arial", 12))
        challenge_layout.addWidget(self.challenge_date_label)
        
        self.challenge_game_label = QLabel()
        self.challenge_game_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        challenge_layout.addWidget(self.challenge_game_label)
        
        self.challenge_text_label = QLabel()
        self.challenge_text_label.setWordWrap(True)
        self.challenge_text_label.setFont(QFont("Arial", 12))
        challenge_layout.addWidget(self.challenge_text_label)
        
        self.challenge_status_label = QLabel()
        challenge_layout.addWidget(self.challenge_status_label)
        
        challenge_btn_layout = QHBoxLayout()
        
        self.play_challenge_btn = QPushButton("▶️ Play Challenge")
        self.play_challenge_btn.clicked.connect(self.play_daily_challenge)
        challenge_btn_layout.addWidget(self.play_challenge_btn)
        
        self.complete_challenge_btn = QPushButton("✅ Mark Complete")
        self.complete_challenge_btn.clicked.connect(self.complete_challenge)
        challenge_btn_layout.addWidget(self.complete_challenge_btn)
        
        challenge_layout.addLayout(challenge_btn_layout)
        
        layout.addWidget(self.challenge_frame)
        
        # Challenge history
        history_label = QLabel("📅 Challenge History")
        history_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(history_label)
        
        self.challenge_history = QTextEdit()
        self.challenge_history.setReadOnly(True)
        layout.addWidget(self.challenge_history)
        
        layout.addStretch()
        
        self.update_challenge_display()
        
        return widget
    
    def create_recommendations_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("💡 Recommended For You")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Based on your play history and preferences")
        layout.addWidget(desc)
        
        # Recommendations list
        self.recommendations_list = QListWidget()
        self.recommendations_list.setIconSize(QSize(64, 64))
        self.recommendations_list.setSpacing(5)
        self.recommendations_list.itemDoubleClicked.connect(self.play_favorite)
        layout.addWidget(self.recommendations_list)
        
        refresh_rec_btn = QPushButton("🔄 Refresh Recommendations")
        refresh_rec_btn.clicked.connect(self.update_recommendations)
        layout.addWidget(refresh_rec_btn)
        
        self.update_recommendations()
        
        return widget
    
    def create_about_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml(f"""
        <h1>🎮 Papa's Games Launcher</h1>
        <h2>Version {self.version}</h2>
        
        <h3>🌟 About</h3>
        <p>The ultimate, feature-packed launcher for all Papa's games from Poki! Enjoy all your favorite Papa Louie restaurant games with advanced tracking, achievements, and more!</p>
        
        <h3>✨ Features</h3>
        <ul>
            <li>✅ Play all 14 Papa's games in-app</li>
            <li>✅ Comprehensive statistics tracking</li>
            <li>✅ Achievements system with 11+ achievements</li>
            <li>✅ Daily challenges</li>
            <li>✅ Smart game recommendations</li>
            <li>✅ Multiple theme options (6 themes)</li>
            <li>✅ User leveling system with XP</li>
            <li>✅ Game notes and favorites</li>
            <li>✅ Screenshot capture</li>
            <li>✅ Export statistics to CSV</li>
            <li>✅ Keyboard shortcuts</li>
            <li>✅ System tray integration</li>
            <li>✅ Auto-update notifications</li>
            <li>✅ Performance mode</li>
            <li>✅ Play reminders</li>
        </ul>
        
        <h3>⌨️ Keyboard Shortcuts</h3>
        <ul>
            <li><b>Ctrl+F</b> - Focus search</li>
            <li><b>Ctrl+H</b> - Go home</li>
            <li><b>F11</b> - Toggle fullscreen</li>
            <li><b>Ctrl+S</b> - Settings</li>
            <li><b>Ctrl+Q</b> - Quit</li>
        </ul>
        
        <h3>🔗 GitHub Repository</h3>
        <p><a href="{self.github_repo}">{self.github_repo}</a></p>
        <p>⭐ Star the repo | 🐛 Report issues | 🤝 Contribute</p>
        
        <h3>👨‍💻 Developer</h3>
        <p>Created by <b>sugarypumpkin822</b></p>
        
        <h3>🎮 Credits</h3>
        <p>Games by <b>Flipline Studios</b>, hosted on <b>Poki.com</b></p>
        <p>Launcher created with PyQt6 and ❤️</p>
        
        <h3>📚 Libraries Used</h3>
        <ul>
            <li><b>PyQt6</b> - GUI framework</li>
            <li><b>PyQt6-WebEngine</b> - Embedded browser</li>
            <li><b>PyQt6-Multimedia</b> - Audio support</li>
            <li><b>requests</b> - HTTP library for updates</li>
            <li><b>json</b> - Settings and data management</li>
        </ul>
        
        <h3>📄 License</h3>
        <p>MIT License - Free and open source</p>
        """)
        layout.addWidget(about_text)
        
        button_layout = QHBoxLayout()
        
        github_btn = QPushButton("🔗 GitHub Repo")
        github_btn.clicked.connect(lambda: self.open_url(self.github_repo))
        button_layout.addWidget(github_btn)
        
        poki_btn = QPushButton("🌐 Poki.com")
        poki_btn.clicked.connect(lambda: self.open_url("https://poki.com"))
        button_layout.addWidget(poki_btn)
        
        support_btn = QPushButton("💖 Support")
        support_btn.clicked.connect(self.show_support_dialog)
        button_layout.addWidget(support_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def populate_game_list(self):
        self.game_list.clear()
        
        placeholder_pixmap = QPixmap(64, 64)
        placeholder_pixmap.fill(Qt.GlobalColor.lightGray)
        placeholder_icon = QIcon(placeholder_pixmap)
        
        for game in self.games:
            item = QListWidgetItem(placeholder_icon, game.name)
            item.setData(Qt.ItemDataRole.UserRole, game)
            self.game_list.addItem(item)
    
    def load_icons(self):
        self.status_label.setText("Loading game icons...")
        
        for i in range(self.game_list.count()):
            item = self.game_list.item(i)
            game = item.data(Qt.ItemDataRole.UserRole)
            
            request = QNetworkRequest(QUrl(game.icon_url))
            reply = self.network_manager.get(request)
            self.pending_requests[reply] = (game, item)
    
    def on_icon_downloaded(self, reply):
        if reply in self.pending_requests:
            game, item = self.pending_requests[reply]
            
            if reply.error() == QNetworkReply.NetworkError.NoError:
                image_data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(image_data):
                    scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, 
                                                  Qt.TransformationMode.SmoothTransformation)
                    icon = QIcon(scaled_pixmap)
                    item.setIcon(icon)
                    game.icon = icon
            
            del self.pending_requests[reply]
            
            if not self.pending_requests:
                self.status_label.setText(f"{len(self.games)} games ready!")
                self.update_favorites_list()
                self.update_recommendations()
        
        reply.deleteLater()
    
    def on_game_selected(self, item):
        game = item.data(Qt.ItemDataRole.UserRole)
        
        difficulty_colors = {'Easy': '🟢', 'Medium': '🟡', 'Hard': '🔴'}
        diff_emoji = difficulty_colors.get(game.difficulty, '⚪')
        
        self.game_title_label.setText(f"{game.name} {diff_emoji}")
        self.game_desc_label.setText(f"📁 {game.category} | {game.description}")
        
        stats_text = f"🎮 Played {game.play_count} times"
        if game.total_time > 0:
            hours = game.total_time // 3600
            minutes = (game.total_time % 3600) // 60
            stats_text += f" | ⏱️ {hours}h {minutes}m"
        if game.last_played:
            stats_text += f" | 📅 {game.last_played.strftime('%Y-%m-%d')}"
        if game.streak > 0:
            stats_text += f" | 🔥 {game.streak} day streak"
        
        self.game_stats_label.setText(stats_text)
        
        self.favorite_btn.setChecked(game.favorite)
        self.rating_slider.setValue(game.rating)
        self.rating_label.setText(f"{game.rating}/5")
        self.game_notes.setText(game.notes)
    
    def save_game_notes(self):
        """Save notes for current game"""
        item = self.game_list.currentItem()
        if item:
            game = item.data(Qt.ItemDataRole.UserRole)
            game.notes = self.game_notes.toPlainText()
            if self.settings.get('auto_save', True):
                self.save_game_data()
    
    def play_selected_game(self):
        item = self.game_list.currentItem()
        if item:
            game = item.data(Qt.ItemDataRole.UserRole)
            self.play_game(game)
    
    def play_game(self, game):
        self.current_game = game
        self.game_start_time = datetime.now()
        
        game.play_count += 1
        game.last_played = self.game_start_time
        
        # Update streak
        if game.last_played:
            days_diff = (datetime.now() - game.last_played).days
            if days_diff == 1:
                game.streak += 1
            elif days_diff > 1:
                game.streak = 1
        else:
            game.streak = 1
        
        # Add XP
        xp_gained = 10
        self.add_xp(xp_gained)
        
        self.status_label.setText(f"▶️ Playing: {game.name} (+{xp_gained} XP)")
        self.web_view.setUrl(QUrl(game.url))
        
        self.play_timer.start(1000)
        
        if self.settings.get('notifications_enabled', True):
            reminder_minutes = self.settings.get('play_reminder_minutes', 60)
            self.notification_timer.start(reminder_minutes * 60 * 1000)
        
        self.save_game_data()
        self.update_statistics()
        self.check_achievements()
    
    def add_xp(self, amount):
        """Add XP and check for level up"""
        self.total_xp += amount
        
        while self.total_xp >= self.xp_for_next_level():
            self.total_xp -= self.xp_for_next_level()
            self.user_level += 1
            self.show_level_up_notification()
        
        self.update_profile_display()
        self.save_settings()
    
    def xp_for_next_level(self):
        """Calculate XP needed for next level"""
        return 100 + (self.user_level * 50)
    
    def update_profile_display(self):
        """Update profile display"""
        self.profile_label.setText(f"👤 {self.username} | Level {self.user_level}")
        self.xp_progress.setMaximum(self.xp_for_next_level())
        self.xp_progress.setValue(self.total_xp % self.xp_for_next_level())
        self.xp_progress.setFormat(f"{self.total_xp % self.xp_for_next_level()}/{self.xp_for_next_level()} XP")
    
    def show_level_up_notification(self):
        """Show level up notification"""
        self.tray_icon.showMessage(
            "🎉 Level Up!",
            f"Congratulations! You reached level {self.user_level}!",
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )
        QMessageBox.information(self, "Level Up!", f"🎉 You reached level {self.user_level}!")
    
    def update_play_time(self):
        if self.current_game and self.game_start_time:
            self.current_game.total_time += 1
            if self.settings.get('auto_save', True) and self.current_game.total_time % 60 == 0:
                self.save_game_data()
    
    def show_play_reminder(self):
        if self.current_game:
            elapsed = (datetime.now() - self.game_start_time).total_seconds()
            minutes = int(elapsed / 60)
            self.tray_icon.showMessage(
                "⏰ Gaming Reminder",
                f"You've been playing {self.current_game.name} for {minutes} minutes!",
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )
    
    def toggle_favorite(self):
        item = self.game_list.currentItem()
        if item:
            game = item.data(Qt.ItemDataRole.UserRole)
            game.favorite = self.favorite_btn.isChecked()
            self.save_game_data()
            self.update_favorites_list()
            self.check_achievements()
    
    def rate_game(self, value):
        item = self.game_list.currentItem()
        if item:
            game = item.data(Qt.ItemDataRole.UserRole)
            game.rating = value
            self.rating_label.setText(f"{value}/5")
            self.save_game_data()
            self.update_statistics()
            self.check_achievements()
    
    def filter_games(self):
        category = self.category_filter.currentText()
        difficulty = self.difficulty_filter.currentText()
        search_text = self.search_box.text().lower()
        show_unplayed_only = self.show_unplayed.isChecked()
        
        for i in range(self.game_list.count()):
            item = self.game_list.item(i)
            game = item.data(Qt.ItemDataRole.UserRole)
            
            category_match = category == "All" or game.category == category
            difficulty_match = difficulty == "All" or game.difficulty == difficulty
            search_match = search_text in game.name.lower()
            unplayed_match = not show_unplayed_only or game.play_count == 0
            
            item.setHidden(not (category_match and difficulty_match and search_match and unplayed_match))
    
    def sort_games(self, sort_by):
        games = []
        for i in range(self.game_list.count()):
            item = self.game_list.item(i)
            games.append(item.data(Qt.ItemDataRole.UserRole))
        
        if sort_by == "Most Played":
            games.sort(key=lambda g: g.play_count, reverse=True)
        elif sort_by == "Recently Played":
            games.sort(key=lambda g: g.last_played if g.last_played else datetime.min, reverse=True)
        elif sort_by == "Highest Rated":
            games.sort(key=lambda g: g.rating, reverse=True)
        elif sort_by == "Difficulty":
            diff_order = {"Easy": 0, "Medium": 1, "Hard": 2}
            games.sort(key=lambda g: diff_order.get(g.difficulty, 3))
        else:
            games.sort(key=lambda g: g.name)
        
        self.games = games
        self.populate_game_list()
        self.load_icons()
    
    def update_favorites_list(self):
        self.favorites_list.clear()
        
        for game in self.games:
            if game.favorite and game.icon:
                item = QListWidgetItem(game.icon, game.name)
                item.setData(Qt.ItemDataRole.UserRole, game)
                self.favorites_list.addItem(item)
    
    def play_favorite(self, item):
        game = item.data(Qt.ItemDataRole.UserRole)
        self.tabs.setCurrentIndex(0)
        self.play_game(game)
    
    def play_random_game(self):
        """Play a random game"""
        if self.games:
            game = random.choice(self.games)
            self.tabs.setCurrentIndex(0)
            self.play_game(game)
            QMessageBox.information(self, "Random Game", f"🎲 Playing: {game.name}")
    
    def update_statistics(self):
        self.stats_table.setRowCount(len(self.games))
        
        for i, game in enumerate(self.games):
            self.stats_table.setItem(i, 0, QTableWidgetItem(game.name))
            self.stats_table.setItem(i, 1, QTableWidgetItem(str(game.play_count)))
            
            time_hours = game.total_time // 3600
            time_mins = (game.total_time % 3600) // 60
            self.stats_table.setItem(i, 2, QTableWidgetItem(f"{time_hours}h {time_mins}m"))
            
            last_played = game.last_played.strftime('%Y-%m-%d') if game.last_played else "Never"
            self.stats_table.setItem(i, 3, QTableWidgetItem(last_played))
            
            rating_text = f"{'⭐' * game.rating}" if game.rating > 0 else "-"
            self.stats_table.setItem(i, 4, QTableWidgetItem(rating_text))
            
            self.stats_table.setItem(i, 5, QTableWidgetItem(f"{game.streak} days" if game.streak > 0 else "-"))
    
    def total_games_played(self):
        return sum(g.play_count for g in self.games)
    
    def total_play_time(self):
        return sum(g.total_time for g in self.games)
    
    def clear_history(self):
        """Clear game history"""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all game history? This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for game in self.games:
                game.play_count = 0
                game.total_time = 0
                game.last_played = None
                game.streak = 0
            
            self.save_game_data()
            self.update_statistics()
            QMessageBox.information(self, "Success", "Game history cleared!")
    
    def check_achievements(self):
        """Check and unlock achievements"""
        newly_unlocked = []
        
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.requirement():
                achievement.unlocked = True
                achievement.unlock_date = datetime.now()
                newly_unlocked.append(achievement)
        
        if newly_unlocked:
            self.save_game_data()
            for ach in newly_unlocked:
                xp_reward = 50
                self.add_xp(xp_reward)
                self.tray_icon.showMessage(
                    "🏆 Achievement Unlocked!",
                    f"{ach.icon} {ach.name}\n+{xp_reward} XP",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )
    
    def generate_daily_challenge(self):
        """Generate daily challenge"""
        today = datetime.now().date()
        
        # Use date as seed for consistent daily challenge
        random.seed(today.toordinal())
        
        game = random.choice(self.games)
        
        challenges = [
            f"Play {game.name} and serve 10 perfect orders!",
            f"Beat your best score in {game.name}!",
            f"Play {game.name} for at least 15 minutes!",
            f"Try {game.name} if you haven't played it yet!",
            f"Get a 5-star rating on 3 orders in {game.name}!",
        ]
        
        challenge_text = random.choice(challenges)
        
        self.daily_challenge = DailyChallenge(today, game, challenge_text)
        
        # Reset random seed
        random.seed()
    
    def update_challenge_display(self):
        """Update daily challenge display"""
        if self.daily_challenge:
            self.challenge_date_label.setText(f"📅 {self.daily_challenge.date.strftime('%B %d, %Y')}")
            self.challenge_game_label.setText(f"🎮 {self.daily_challenge.game.name}")
            self.challenge_text_label.setText(f"🎯 {self.daily_challenge.challenge_text}")
            
            if self.daily_challenge.completed:
                self.challenge_status_label.setText("✅ Challenge Complete!")
                self.challenge_status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.challenge_status_label.setText("⏳ Challenge Pending")
                self.challenge_status_label.setStyleSheet("color: orange;")
    
    def play_daily_challenge(self):
        """Play the daily challenge game"""
        if self.daily_challenge:
            self.tabs.setCurrentIndex(0)
            self.play_game(self.daily_challenge.game)
    
    def complete_challenge(self):
        """Mark daily challenge as complete"""
        if self.daily_challenge and not self.daily_challenge.completed:
            self.daily_challenge.completed = True
            xp_reward = 100
            self.add_xp(xp_reward)
            self.update_challenge_display()
            QMessageBox.information(self, "Challenge Complete!", f"🎉 Daily Challenge Complete!\n+{xp_reward} XP")
    
    def update_recommendations(self):
        """Update game recommendations"""
        self.recommendations_list.clear()
        
        # Recommend unplayed games
        unplayed = [g for g in self.games if g.play_count == 0]
        
        # Recommend games in favorite categories
        favorite_categories = set()
        for game in self.games:
            if game.favorite:
                favorite_categories.add(game.category)
        
        recommended = []
        
        # Add unplayed games
        for game in unplayed[:3]:
            recommended.append(("Unplayed", game))
        
        # Add games from favorite categories
        for game in self.games:
            if game.category in favorite_categories and game.play_count > 0 and len(recommended) < 6:
                recommended.append(("Similar to favorites", game))
        
        # Add highly rated games
        highly_rated = sorted([g for g in self.games if g.rating >= 4], key=lambda x: x.rating, reverse=True)
        for game in highly_rated[:3]:
            if len(recommended) < 8 and game not in [r[1] for r in recommended]:
                recommended.append(("Highly rated", game))
        
        for reason, game in recommended:
            if game.icon:
                item = QListWidgetItem(game.icon, f"{game.name}\n💡 {reason}")
                item.setData(Qt.ItemDataRole.UserRole, game)
                self.recommendations_list.addItem(item)
    
    def export_statistics(self):
        """Export statistics to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Statistics",
            f"papa_games_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Game,Category,Difficulty,Plays,Total Time (min),Rating,Favorite,Streak\n")
                    for game in self.games:
                        total_mins = game.total_time // 60
                        f.write(f"{game.name},{game.category},{game.difficulty},{game.play_count},{total_mins},{game.rating},{game.favorite},{game.streak}\n")
                
                QMessageBox.information(self, "Success", f"Statistics exported to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def take_screenshot(self):
        """Take screenshot of current game"""
        if self.current_game:
            screenshots_dir = self.settings_file.parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"{self.current_game.name}_{timestamp}.png"
            
            # Take screenshot of web view
            pixmap = self.web_view.grab()
            pixmap.save(str(filename))
            
            self.status_label.setText(f"📷 Screenshot saved!")
            QMessageBox.information(self, "Screenshot", f"Screenshot saved to:\n{filename}")
        else:
            QMessageBox.warning(self, "No Game", "Please start a game first!")
    
    def go_home(self):
        self.show_welcome_screen()
        self.play_timer.stop()
        self.notification_timer.stop()
        self.current_game = None
        self.status_label.setText("Ready")
    
    def show_welcome_screen(self):
        theme = self.settings['theme']
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        
        if theme == 'ocean':
            gradient = "linear-gradient(135deg, #2E3192 0%, #1BFFFF 100%)"
        elif theme == 'forest':
            gradient = "linear-gradient(135deg, #134E5E 0%, #71B280 100%)"
        elif theme == 'sunset':
            gradient = "linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%)"
        elif theme == 'purple':
            gradient = "linear-gradient(135deg, #7F00FF 0%, #E100FF 100%)"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: {gradient};
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .container {{
                    text-align: center;
                    color: white;
                }}
                h1 {{
                    font-size: 52px;
                    margin-bottom: 20px;
                    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
                }}
                p {{
                    font-size: 22px;
                    opacity: 0.95;
                }}
                .emoji {{
                    font-size: 100px;
                    margin-bottom: 30px;
                    animation: bounce 2s infinite;
                }}
                .version {{
                    font-size: 16px;
                    opacity: 0.7;
                    margin-top: 20px;
                }}
                .stats {{
                    margin-top: 30px;
                    font-size: 18px;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-25px); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="emoji">🎮</div>
                <h1>Papa's Games Launcher</h1>
                <p>Your ultimate Papa Louie gaming hub!</p>
                <p>Select a game from the list to start playing</p>
                <div class="stats">
                    Level {self.user_level} | {self.total_games_played()} Games Played
                </div>
                <div class="version">v{self.version} by sugarypumpkin822</div>
            </div>
        </body>
        </html>
        """
        self.web_view.setHtml(html)
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_btn.setText("⛶ Full")
        else:
            self.showFullScreen()
            self.fullscreen_btn.setText("⛶ Exit")
    
    def show_theme_selector(self):
        """Show theme selection dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Theme")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        for theme_id, theme_info in self.available_themes.items():
            btn = QPushButton(f"{theme_info['emoji']} {theme_info['name']}")
            btn.clicked.connect(lambda checked, t=theme_id: self.set_theme(t, dialog))
            layout.addWidget(btn)
        
        dialog.exec()
    
    def set_theme(self, theme, dialog=None):
        """Set application theme"""
        self.settings['theme'] = theme
        self.save_settings()
        self.apply_theme()
        if dialog:
            dialog.accept()
    
    def apply_theme(self):
        theme = self.settings['theme']
        
        if theme == 'dark':
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #2c3e50; color: #ecf0f1; }
                QListWidget { background-color: #34495e; border: 2px solid #7f8c8d; color: #ecf0f1; }
                QListWidget::item:selected { background-color: #3498db; }
                QLineEdit, QComboBox, QSpinBox { background-color: #34495e; color: #ecf0f1; border: 2px solid #7f8c8d; padding: 5px; }
                QPushButton { background-color: #3498db; color: white; border: none; padding: 8px; border-radius: 4px; }
                QPushButton:hover { background-color: #2980b9; }
                QTextEdit { background-color: #34495e; color: #ecf0f1; border: 2px solid #7f8c8d; }
                QTableWidget { background-color: #34495e; color: #ecf0f1; gridline-color: #7f8c8d; }
                QHeaderView::section { background-color: #2c3e50; color: #ecf0f1; padding: 5px; }
                QFrame { background-color: #34495e; border-radius: 5px; padding: 10px; }
                QGroupBox { border: 2px solid #7f8c8d; border-radius: 5px; margin-top: 10px; }
                QProgressBar { border: 2px solid #7f8c8d; border-radius: 5px; text-align: center; }
                QProgressBar::chunk { background-color: #3498db; }
            """)
        elif theme == 'ocean':
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #1a3a52; color: #e8f4f8; }
                QListWidget { background-color: #2c5f77; border: 2px solid #4a90a4; color: #e8f4f8; }
                QListWidget::item:selected { background-color: #1BFFFF; color: #1a3a52; }
                QPushButton { background-color: #1BFFFF; color: #1a3a52; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #00d4d4; }
            """)
        elif theme == 'forest':
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #2d5016; color: #e8f5e9; }
                QListWidget { background-color: #3d6b21; border: 2px solid #5d8a35; color: #e8f5e9; }
                QListWidget::item:selected { background-color: #71B280; color: #2d5016; }
                QPushButton { background-color: #71B280; color: #2d5016; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #5d9968; }
            """)
        elif theme == 'sunset':
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #ff6b6b; color: #fff; }
                QListWidget { background-color: #ff8787; border: 2px solid #ffa0a0; color: #fff; }
                QListWidget::item:selected { background-color: #FFE66D; color: #ff6b6b; }
                QPushButton { background-color: #FFE66D; color: #ff6b6b; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #ffd700; }
            """)
        elif theme == 'purple':
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #4a148c; color: #f3e5f5; }
                QListWidget { background-color: #6a1b9a; border: 2px solid #8e24aa; color: #f3e5f5; }
                QListWidget::item:selected { background-color: #E100FF; color: #4a148c; }
                QPushButton { background-color: #E100FF; color: #4a148c; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #c700d8; }
            """)
        else:  # light
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #ecf0f1; color: #2c3e50; }
                QListWidget { background-color: white; border: 2px solid #bdc3c7; }
                QListWidget::item:selected { background-color: #3498db; color: white; }
                QLineEdit, QComboBox, QSpinBox { background-color: white; border: 2px solid #bdc3c7; padding: 5px; }
                QPushButton { background-color: #3498db; color: white; border: none; padding: 8px; border-radius: 4px; }
                QPushButton:hover { background-color: #2980b9; }
                QTextEdit { background-color: white; border: 2px solid #bdc3c7; }
                QTableWidget { background-color: white; gridline-color: #bdc3c7; }
                QHeaderView::section { background-color: #ecf0f1; padding: 5px; }
                QFrame { background-color: #f8f9fa; border-radius: 5px; padding: 10px; }
                QGroupBox { border: 2px solid #bdc3c7; border-radius: 5px; margin-top: 10px; }
                QProgressBar { border: 2px solid #bdc3c7; border-radius: 5px; text-align: center; }
                QProgressBar::chunk { background-color: #3498db; }
            """)
        
        self.show_welcome_screen()
    
    def apply_toolbar_style(self, toolbar):
        if self.settings['theme'] == 'dark':
            toolbar.setStyleSheet("QWidget { background-color: #34495e; padding: 5px; }")
        else:
            toolbar.setStyleSheet("QWidget { background-color: #3498db; color: white; padding: 5px; }")
    
    def update_animations(self):
        """Update any animations"""
        pass
    
    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Settings")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        # Profile settings
        profile_group = QGroupBox("👤 Profile")
        profile_layout = QVBoxLayout()
        
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        username_input = QLineEdit(self.username)
        username_layout.addWidget(username_input)
        profile_layout.addLayout(username_layout)
        
        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)
        
        # General settings
        general_group = QGroupBox("⚙️ General")
        general_layout = QVBoxLayout()
        
        update_check = QCheckBox("Check for updates on startup")
        update_check.setChecked(self.settings.get('check_updates', True))
        general_layout.addWidget(update_check)
        
        auto_save = QCheckBox("Auto-save game data")
        auto_save.setChecked(self.settings.get('auto_save', True))
        general_layout.addWidget(auto_save)
        
        show_tips = QCheckBox("Show gameplay tips")
        show_tips.setChecked(self.settings.get('show_tips', True))
        general_layout.addWidget(show_tips)
        
        performance_mode = QCheckBox("Performance mode (reduce animations)")
        performance_mode.setChecked(self.settings.get('performance_mode', False))
        general_layout.addWidget(performance_mode)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Notification settings
        notif_group = QGroupBox("🔔 Notifications")
        notif_layout = QVBoxLayout()
        
        notif_check = QCheckBox("Enable play time notifications")
        notif_check.setChecked(self.settings.get('notifications_enabled', True))
        notif_layout.addWidget(notif_check)
        
        reminder_layout = QHBoxLayout()
        reminder_layout.addWidget(QLabel("Reminder interval (minutes):"))
        reminder_spin = QSpinBox()
        reminder_spin.setMinimum(15)
        reminder_spin.setMaximum(240)
        reminder_spin.setValue(self.settings.get('play_reminder_minutes', 60))
        reminder_layout.addWidget(reminder_spin)
        notif_layout.addLayout(reminder_layout)
        
        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save")
        cancel_btn = QPushButton("❌ Cancel")
        reset_btn = QPushButton("🔄 Reset to Defaults")
        
        def save_settings_dialog():
            self.username = username_input.text()
            self.settings['check_updates'] = update_check.isChecked()
            self.settings['auto_save'] = auto_save.isChecked()
            self.settings['show_tips'] = show_tips.isChecked()
            self.settings['performance_mode'] = performance_mode.isChecked()
            self.settings['notifications_enabled'] = notif_check.isChecked()
            self.settings['play_reminder_minutes'] = reminder_spin.value()
            self.save_settings()
            self.update_profile_display()
            dialog.accept()
            QMessageBox.information(self, "Success", "Settings saved!")
        
        def reset_settings():
            reply = QMessageBox.question(
                dialog,
                "Reset Settings",
                "Are you sure you want to reset all settings to defaults?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.settings = {
                    'theme': 'light',
                    'check_updates': True,
                    'auto_save': True,
                    'show_tips': True,
                    'performance_mode': False,
                    'notifications_enabled': True,
                    'play_reminder_minutes': 60,
                }
                self.save_settings()
                dialog.accept()
                QMessageBox.information(self, "Reset", "Settings reset to defaults!")
        
        save_btn.clicked.connect(save_settings_dialog)
        cancel_btn.clicked.connect(dialog.reject)
        reset_btn.clicked.connect(reset_settings)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(reset_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def show_welcome_dialog(self):
        """Show welcome dialog for first-time users"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Welcome!")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        welcome_text = QLabel("""
        <h1>🎮 Welcome to Papa's Games Launcher!</h1>
        <p style='font-size: 14px;'>
        Thank you for choosing the ultimate Papa's games experience!<br><br>
        
        <b>Features:</b><br>
        ✅ Play all 14 Papa's games<br>
        ✅ Track statistics & achievements<br>
        ✅ Daily challenges<br>
        ✅ Level up system<br>
        ✅ Multiple themes<br>
        ✅ And much more!<br><br>
        
        <b>Quick Tips:</b><br>
        • Use <b>Ctrl+F</b> to search games<br>
        • Press <b>F11</b> for fullscreen<br>
        • Check out the Daily Challenge tab!<br>
        • Star the GitHub repo to support development<br>
        </p>
        """)
        welcome_text.setWordWrap(True)
        layout.addWidget(welcome_text)
        
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Enter your username:"))
        username_input = QLineEdit("Player")
        username_layout.addWidget(username_input)
        layout.addLayout(username_layout)
        
        btn = QPushButton("🚀 Get Started!")
        btn.clicked.connect(lambda: self.finish_welcome(username_input.text(), dialog))
        layout.addWidget(btn)
        
        dialog.exec()
    
    def finish_welcome(self, username, dialog):
        """Finish welcome process"""
        self.username = username
        self.settings['welcomed'] = True
        self.settings['username'] = username
        self.save_settings()
        self.update_profile_display()
        dialog.accept()
        QMessageBox.information(self, "Welcome!", f"Welcome, {username}! 🎉\nEnjoy your gaming experience!")
    
    def show_support_dialog(self):
        """Show support dialog"""
        QMessageBox.information(
            self,
            "💖 Support",
            "Thank you for using Papa's Games Launcher!\n\n"
            "Support the project:\n"
            "⭐ Star the GitHub repository\n"
            "🐛 Report bugs and issues\n"
            "💡 Suggest new features\n"
            "🤝 Contribute code\n\n"
            f"GitHub: {self.github_repo}"
        )
    
    def check_for_updates(self):
        self.status_label.setText("Checking for updates...")
        
        self.update_checker = UpdateChecker(self.version, self.github_repo)
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.finished.connect(lambda: self.status_label.setText("Update check complete"))
        self.update_checker.start()
    
    def on_update_available(self, version, url):
        reply = QMessageBox.question(
            self,
            "🔄 Update Available",
            f"Version {version} is available!\n\nWould you like to download it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.open_url(url)
    
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
    
    def closeEvent(self, event):
        self.save_game_data()
        self.save_settings()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Papa's Games Launcher")
    app.setOrganizationName("sugarypumpkin822")
    
    window = PapasGamesLauncher()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()