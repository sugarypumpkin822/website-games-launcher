"""Main window for the game launcher"""
import sys
import random
import webbrowser
import requests
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QListWidgetItem, QPushButton, QLabel, 
                             QLineEdit, QMessageBox, QTabWidget, QTextEdit, 
                             QProgressBar, QComboBox, QCheckBox, QDialog,
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                             QSlider, QSystemTrayIcon, QMenu, QScrollArea,
                             QFileDialog, QGroupBox, QSpinBox)
from PyQt6.QtCore import Qt, QUrl, QSize, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QColor, QFont, QAction, QShortcut, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from core.settings_manager import SettingsManager
from core.game_manager import GameManager
from core.achievement_manager import AchievementManager
from core.download_manager import DownloadManager
from gui.tabs.games_tab import GamesTab
from gui.widgets.fullscreen_game_window import FullscreenGameWindow
from utils.update_checker import UpdateChecker
from utils.update_checker import UpdateChecker
from utils.daily_challenge_generator import DailyChallengeGenerator
from utils.downloader import FileDownloader


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # App metadata
        self.version = "2.0.0"
        self.github_repo = "https://github.com/sugarypumpkin822/website-games-launcher"
        
        self.setWindowTitle(f"🎮 Papa's Games Launcher v{self.version}")
        self.setGeometry(100, 100, 1700, 1000)
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.game_manager = GameManager(self.settings_manager)
        self.achievement_manager = AchievementManager(self.game_manager, self.settings_manager)
        self.download_manager = DownloadManager(self.settings_manager.get_cache_dir())
        
        # User profile
        self.username = self.settings_manager.get('username', 'Player')
        self.user_level = self.settings_manager.get('user_level', 1)
        self.total_xp = self.settings_manager.get('total_xp', 0)
        
        # Current game state
        self.current_game = None
        self.game_start_time = None
        self.fullscreen_window = None
        
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
        
        # Daily challenge
        self.daily_challenge = DailyChallengeGenerator.generate(self.game_manager)
        
        # System tray
        self.setup_system_tray()
        
        # Shortcuts
        self.setup_shortcuts()
        
        # Initialize UI
        self.init_ui()
        self.load_icons()
        self.load_achievements()
        self.update_statistics()
        self.update_favorites_list()
        self.update_challenge_display()
        
        # Check for updates on startup
        if self.settings_manager.get('check_updates', True):
            self.check_for_updates()
        
        # Show welcome message for first time users
        if not self.settings_manager.get('welcomed', False):
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
        if hasattr(self.games_tab, 'search_box'):
            self.games_tab.search_box.setFocus()
            self.games_tab.search_box.selectAll()
    
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
    
    def init_ui(self):
        """Initialize the UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        # Top toolbar with better spacing
        toolbar = QWidget()
        toolbar.setMinimumHeight(70)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(20, 15, 20, 15)
        toolbar_layout.setSpacing(15)
        
        title_label = QLabel("🎮 Papa's Games Launcher")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        toolbar_layout.addWidget(title_label)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.VLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(separator1)
        
        # User profile section with better styling
        profile_container = QWidget()
        profile_layout = QVBoxLayout(profile_container)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(3)
        
        self.profile_label = QLabel(f"👤 {self.username} | Level {self.user_level}")
        self.profile_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        profile_layout.addWidget(self.profile_label)
        
        # XP Progress bar with better styling
        self.xp_progress = QProgressBar()
        self.xp_progress.setMaximum(self.xp_for_next_level())
        self.xp_progress.setValue(self.total_xp % self.xp_for_next_level())
        self.xp_progress.setFormat(f"{self.total_xp % self.xp_for_next_level()}/{self.xp_for_next_level()} XP")
        self.xp_progress.setFixedWidth(220)
        self.xp_progress.setMinimumHeight(20)
        profile_layout.addWidget(self.xp_progress)
        
        toolbar_layout.addWidget(profile_container)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(separator2)
        
        toolbar_layout.addStretch()
        
        # Quick action buttons with better spacing
        random_btn = QPushButton("🎲 Random")
        random_btn.setToolTip("Play a random game")
        random_btn.setMinimumHeight(35)
        random_btn.setMinimumWidth(100)
        random_btn.clicked.connect(self.play_random_game)
        toolbar_layout.addWidget(random_btn)
        
        export_btn = QPushButton("📊 Export")
        export_btn.setToolTip("Export your statistics")
        export_btn.setMinimumHeight(35)
        export_btn.setMinimumWidth(100)
        export_btn.clicked.connect(self.export_statistics)
        toolbar_layout.addWidget(export_btn)
        
        self.theme_btn = QPushButton("🎨 Theme")
        self.theme_btn.setMinimumHeight(35)
        self.theme_btn.setMinimumWidth(100)
        self.theme_btn.clicked.connect(self.show_theme_selector)
        toolbar_layout.addWidget(self.theme_btn)
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setMinimumHeight(35)
        settings_btn.setMinimumWidth(100)
        settings_btn.clicked.connect(self.show_settings)
        toolbar_layout.addWidget(settings_btn)
        
        update_btn = QPushButton("🔄 Update")
        update_btn.setMinimumHeight(35)
        update_btn.setMinimumWidth(100)
        update_btn.clicked.connect(self.check_for_updates)
        toolbar_layout.addWidget(update_btn)
        
        self.apply_toolbar_style(toolbar)
        main_layout.addWidget(toolbar)
        
        # Main content with tabs
        self.tabs = QTabWidget()
        
        # Games tab
        self.games_tab = GamesTab(self)
        self.games_tab.populate_game_list(self.game_manager.games)
        self.tabs.addTab(self.games_tab, "🎮 Games")
        
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
    
    def create_favorites_tab(self):
        """Create favorites tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Header section
        header_layout = QHBoxLayout()
        title = QLabel("⭐ Your Favorite Games")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        count_label = QLabel(f"({sum(1 for g in self.game_manager.games if g.favorite)} games)")
        count_label.setFont(QFont("Arial", 12))
        count_label.setStyleSheet("color: #666;")
        header_layout.addWidget(count_label)
        layout.addLayout(header_layout)
        
        # Description
        desc = QLabel("Double-click a game to play it, or right-click for more options")
        desc.setFont(QFont("Arial", 9))
        desc.setStyleSheet("color: #888; padding-bottom: 10px;")
        layout.addWidget(desc)
        
        self.favorites_list = QListWidget()
        self.favorites_list.setIconSize(QSize(80, 80))
        self.favorites_list.setSpacing(15)
        self.favorites_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.favorites_list.setGridSize(QSize(180, 180))
        self.favorites_list.setMovement(QListWidget.Movement.Static)
        self.favorites_list.itemDoubleClicked.connect(self.play_favorite)
        layout.addWidget(self.favorites_list, stretch=1)
        
        return widget
    
    def create_stats_tab(self):
        """Create statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        title = QLabel("📊 Your Gaming Statistics")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Stats summary with cards - better spacing
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        plays_card = self.create_stat_card("🎮 Total Plays", str(self.game_manager.total_games_played()))
        cards_layout.addWidget(plays_card)
        
        total_time = self.game_manager.total_play_time()
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        time_card = self.create_stat_card("⏱️ Total Time", f"{hours}h {minutes}m")
        cards_layout.addWidget(time_card)
        
        fav_card = self.create_stat_card("⭐ Favorites", str(sum(1 for g in self.game_manager.games if g.favorite)))
        cards_layout.addWidget(fav_card)
        
        unlocked = sum(1 for a in self.achievement_manager.achievements if a.unlocked)
        ach_card = self.create_stat_card("🏆 Achievements", f"{unlocked}/{len(self.achievement_manager.achievements)}")
        cards_layout.addWidget(ach_card)
        
        # Additional stats
        avg_rating = sum(g.rating for g in self.game_manager.games) / len(self.game_manager.games) if self.game_manager.games else 0
        rating_card = self.create_stat_card("⭐ Avg Rating", f"{avg_rating:.1f}/5")
        cards_layout.addWidget(rating_card)
        
        layout.addLayout(cards_layout)
        
        # Stats table with better styling
        table_label = QLabel("📋 Detailed Game Statistics")
        table_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(table_label)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(7)
        self.stats_table.setHorizontalHeaderLabels(["Game", "Category", "Plays", "Time", "Last Played", "Rating", "Streak"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stats_table.setMinimumHeight(400)
        layout.addWidget(self.stats_table, stretch=1)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        refresh_btn = QPushButton("🔄 Refresh Statistics")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setMinimumWidth(150)
        refresh_btn.clicked.connect(self.update_statistics)
        btn_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.setMinimumHeight(35)
        clear_btn.setMinimumWidth(150)
        clear_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return widget
    
    def create_stat_card(self, title, value):
        """Create a statistic card with better styling"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(120)
        card.setMinimumWidth(150)
        card.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(value_label)
        
        return card
    
    def create_achievements_tab(self):
        """Create achievements tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🏆 Achievements")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        unlocked = sum(1 for a in self.achievement_manager.achievements if a.unlocked)
        total = len(self.achievement_manager.achievements)
        progress_percent = (unlocked / total * 100) if total > 0 else 0
        
        progress_label = QLabel(f"Progress: {unlocked}/{total} ({progress_percent:.0f}%)")
        progress_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        progress_label.setStyleSheet("color: #27ae60; padding: 5px;")
        header_layout.addWidget(progress_label)
        layout.addLayout(header_layout)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setMaximum(total)
        progress_bar.setValue(unlocked)
        progress_bar.setFormat(f"{unlocked}/{total}")
        progress_bar.setMinimumHeight(25)
        layout.addWidget(progress_bar)
        
        # Achievements list with better spacing
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(12)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        
        for achievement in self.achievement_manager.achievements:
            ach_frame = QFrame()
            ach_frame.setFrameShape(QFrame.Shape.StyledPanel)
            ach_frame.setMinimumHeight(100)
            ach_frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                    padding: 10px;
                }
            """)
            
            ach_layout = QHBoxLayout(ach_frame)
            ach_layout.setSpacing(15)
            ach_layout.setContentsMargins(15, 15, 15, 15)
            
            icon_label = QLabel(achievement.icon)
            icon_label.setFont(QFont("Arial", 40))
            icon_label.setMinimumWidth(60)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ach_layout.addWidget(icon_label)
            
            info_layout = QVBoxLayout()
            info_layout.setSpacing(5)
            
            name_label = QLabel(achievement.name)
            name_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
            info_layout.addWidget(name_label)
            
            desc_label = QLabel(achievement.description)
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
            
            if achievement.unlocked:
                unlock_label = QLabel(f"✅ Unlocked on {achievement.unlock_date.strftime('%B %d, %Y')}")
                unlock_label.setStyleSheet("color: #27ae60; font-weight: bold; padding-top: 5px;")
                unlock_label.setFont(QFont("Arial", 9))
                info_layout.addWidget(unlock_label)
            else:
                lock_label = QLabel("🔒 Locked - Keep playing to unlock!")
                lock_label.setStyleSheet("color: #95a5a6; font-style: italic; padding-top: 5px;")
                lock_label.setFont(QFont("Arial", 9))
                info_layout.addWidget(lock_label)
            
            ach_layout.addLayout(info_layout)
            ach_layout.addStretch()
            
            scroll_layout.addWidget(ach_frame)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, stretch=1)
        
        return widget
    
    def create_challenge_tab(self):
        """Create daily challenge tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        title = QLabel("🎯 Daily Challenge")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Complete daily challenges to earn bonus XP and rewards!")
        desc.setFont(QFont("Arial", 10))
        desc.setStyleSheet("color: #666; padding-bottom: 10px;")
        layout.addWidget(desc)
        
        self.challenge_frame = QFrame()
        self.challenge_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.challenge_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #3498db;
                border-radius: 12px;
                background-color: #ecf0f1;
                padding: 20px;
            }
        """)
        challenge_layout = QVBoxLayout(self.challenge_frame)
        challenge_layout.setSpacing(15)
        challenge_layout.setContentsMargins(20, 20, 20, 20)
        
        self.challenge_date_label = QLabel()
        self.challenge_date_label.setFont(QFont("Arial", 11))
        self.challenge_date_label.setStyleSheet("color: #7f8c8d;")
        challenge_layout.addWidget(self.challenge_date_label)
        
        self.challenge_game_label = QLabel()
        self.challenge_game_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        challenge_layout.addWidget(self.challenge_game_label)
        
        self.challenge_text_label = QLabel()
        self.challenge_text_label.setWordWrap(True)
        self.challenge_text_label.setFont(QFont("Arial", 12))
        self.challenge_text_label.setStyleSheet("padding: 10px; background-color: white; border-radius: 5px;")
        challenge_layout.addWidget(self.challenge_text_label)
        
        self.challenge_status_label = QLabel()
        self.challenge_status_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        challenge_layout.addWidget(self.challenge_status_label)
        
        challenge_btn_layout = QHBoxLayout()
        challenge_btn_layout.setSpacing(10)
        
        self.play_challenge_btn = QPushButton("▶️ Play Challenge Game")
        self.play_challenge_btn.setMinimumHeight(40)
        self.play_challenge_btn.setMinimumWidth(180)
        self.play_challenge_btn.clicked.connect(self.play_daily_challenge)
        challenge_btn_layout.addWidget(self.play_challenge_btn)
        
        self.complete_challenge_btn = QPushButton("✅ Mark as Complete")
        self.complete_challenge_btn.setMinimumHeight(40)
        self.complete_challenge_btn.setMinimumWidth(180)
        self.complete_challenge_btn.clicked.connect(self.complete_challenge)
        challenge_btn_layout.addWidget(self.complete_challenge_btn)
        
        challenge_layout.addLayout(challenge_btn_layout)
        
        layout.addWidget(self.challenge_frame)
        
        # Challenge history section
        history_label = QLabel("📅 Recent Challenges")
        history_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(history_label)
        
        self.challenge_history = QTextEdit()
        self.challenge_history.setReadOnly(True)
        self.challenge_history.setMaximumHeight(150)
        self.challenge_history.setFont(QFont("Arial", 9))
        layout.addWidget(self.challenge_history)
        
        layout.addStretch()
        
        return widget
    
    def create_recommendations_tab(self):
        """Create recommendations tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("💡 Recommended For You")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        refresh_rec_btn = QPushButton("🔄 Refresh")
        refresh_rec_btn.setMinimumHeight(35)
        refresh_rec_btn.setMinimumWidth(120)
        refresh_rec_btn.clicked.connect(self.update_recommendations)
        header_layout.addWidget(refresh_rec_btn)
        layout.addLayout(header_layout)
        
        desc = QLabel("Personalized game recommendations based on your play history, preferences, and ratings")
        desc.setFont(QFont("Arial", 10))
        desc.setStyleSheet("color: #666; padding-bottom: 10px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Recommendations list with better styling
        self.recommendations_list = QListWidget()
        self.recommendations_list.setIconSize(QSize(80, 80))
        self.recommendations_list.setSpacing(12)
        self.recommendations_list.setAlternatingRowColors(True)
        self.recommendations_list.itemDoubleClicked.connect(self.play_favorite)
        layout.addWidget(self.recommendations_list, stretch=1)
        
        # Info label
        self.recommendations_info = QLabel("")
        self.recommendations_info.setFont(QFont("Arial", 9))
        self.recommendations_info.setStyleSheet("color: #888; padding: 5px;")
        layout.addWidget(self.recommendations_info)
        
        return widget
    
    def create_about_tab(self):
        """Create about tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("ℹ️ About Papa's Games Launcher")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        version_label = QLabel(f"Version {self.version}")
        version_label.setFont(QFont("Arial", 12))
        version_label.setStyleSheet("color: #7f8c8d; padding: 5px;")
        header_layout.addWidget(version_label)
        layout.addLayout(header_layout)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml(f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">🌟 About</h2>
        <p style="font-size: 11pt;">The ultimate, feature-packed launcher for all Papa's games from Poki! 
        Enjoy all your favorite Papa Louie restaurant games with advanced tracking, achievements, fullscreen mode, 
        local downloads, and much more!</p>
        
        <h2 style="color: #2c3e50;">✨ Key Features</h2>
        <ul style="font-size: 10pt;">
            <li>✅ Play all 14 Papa's games in-app with embedded browser</li>
            <li>✅ <b>Fullscreen game mode</b> - Immersive gaming experience</li>
            <li>✅ <b>Local game downloads</b> - Download HTML/CSS/JS for offline play</li>
            <li>✅ Comprehensive statistics tracking (plays, time, streaks, ratings)</li>
            <li>✅ Achievements system with 11+ unlockable achievements</li>
            <li>✅ Daily challenges with XP rewards</li>
            <li>✅ Smart personalized game recommendations</li>
            <li>✅ 6 beautiful themes (Light, Dark, Ocean, Forest, Sunset, Purple)</li>
            <li>✅ User leveling system with XP and level progression</li>
            <li>✅ Game notes, favorites, and custom ratings</li>
            <li>✅ Screenshot capture functionality</li>
            <li>✅ Export statistics to CSV format</li>
            <li>✅ Keyboard shortcuts for quick navigation</li>
            <li>✅ System tray integration</li>
            <li>✅ Auto-update notifications</li>
            <li>✅ Enhanced filtering and sorting options</li>
            <li>✅ Game download management and cache control</li>
        </ul>
        
        <h2 style="color: #2c3e50;">⌨️ Keyboard Shortcuts</h2>
        <ul style="font-size: 10pt;">
            <li><b>Ctrl+F</b> - Focus search box</li>
            <li><b>Ctrl+H</b> - Go to home screen</li>
            <li><b>F11</b> - Toggle fullscreen mode</li>
            <li><b>Ctrl+S</b> - Open settings</li>
            <li><b>Ctrl+Q</b> - Quit application</li>
            <li><b>Escape</b> - Exit fullscreen (when in fullscreen mode)</li>
        </ul>
        
        <h2 style="color: #2c3e50;">📊 Statistics</h2>
        <p style="font-size: 10pt;">
        <b>Total Games:</b> {len(self.game_manager.games)}<br>
        <b>Total Plays:</b> {self.game_manager.total_games_played()}<br>
        <b>Total Play Time:</b> {self.game_manager.total_play_time() // 3600}h {(self.game_manager.total_play_time() % 3600) // 60}m<br>
        <b>Favorites:</b> {len(self.game_manager.get_favorite_games())}<br>
        <b>Achievements Unlocked:</b> {sum(1 for a in self.achievement_manager.achievements if a.unlocked)}/{len(self.achievement_manager.achievements)}
        </p>
        
        <h2 style="color: #2c3e50;">🔗 Links</h2>
        <p style="font-size: 10pt;">
        <a href="{self.github_repo}" style="color: #3498db;">GitHub Repository</a><br>
        <a href="https://poki.com" style="color: #3498db;">Poki.com - Game Platform</a>
        </p>
        
        <h2 style="color: #2c3e50;">👨‍💻 Developer</h2>
        <p style="font-size: 10pt;">Created with ❤️ by <b>sugarypumpkin822</b></p>
        
        <h2 style="color: #2c3e50;">🎮 Credits</h2>
        <p style="font-size: 10pt;">
        Games by <b>Flipline Studios</b><br>
        Hosted on <b>Poki.com</b><br>
        Built with <b>PyQt6</b> and Python
        </p>
        </div>
        """)
        about_text.setMinimumHeight(500)
        layout.addWidget(about_text, stretch=1)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        github_btn = QPushButton("🔗 GitHub Repository")
        github_btn.setMinimumHeight(40)
        github_btn.setMinimumWidth(180)
        github_btn.clicked.connect(lambda: self.open_url(self.github_repo))
        button_layout.addWidget(github_btn)
        
        poki_btn = QPushButton("🌐 Visit Poki.com")
        poki_btn.setMinimumHeight(40)
        poki_btn.setMinimumWidth(180)
        poki_btn.clicked.connect(lambda: self.open_url("https://poki.com"))
        button_layout.addWidget(poki_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return widget
    
    def load_icons(self):
        """Load game icons"""
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText("Loading game icons...")
        
        for i in range(self.games_tab.game_list.count()):
            item = self.games_tab.game_list.item(i)
            game = item.data(Qt.ItemDataRole.UserRole)
            
            request = QNetworkRequest(QUrl(game.icon_url))
            reply = self.network_manager.get(request)
            self.pending_requests[reply] = (game, item)
    
    def on_icon_downloaded(self, reply):
        """Handle icon download completion"""
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
                if hasattr(self.games_tab, 'status_label'):
                    self.games_tab.status_label.setText(f"{len(self.game_manager.games)} games ready!")
                self.update_favorites_list()
                self.update_recommendations()
        
        reply.deleteLater()
    
    def load_achievements(self):
        """Load achievements from game data"""
        data_file = self.settings_manager.settings_file.parent / "game_data.json"
        try:
            if data_file.exists():
                import json
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.achievement_manager.load_achievements(data)
        except:
            pass
    
    def play_game(self, game):
        """Play a game"""
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
        
        # Check if game is downloaded locally
        if game.is_downloaded and game.local_path:
            html_file = Path(game.local_path)
            if html_file.exists():
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.games_tab.web_view.setHtml(html_content, baseUrl=QUrl.fromLocalFile(str(html_file.parent)))
        else:
            self.games_tab.web_view.setUrl(QUrl(game.url))
        
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText(f"▶️ Playing: {game.name} (+{xp_gained} XP)")
        
        self.play_timer.start(1000)
        
        if self.settings_manager.get('notifications_enabled', True):
            reminder_minutes = self.settings_manager.get('play_reminder_minutes', 60)
            self.notification_timer.start(reminder_minutes * 60 * 1000)
        
        self.game_manager.save_game_data()
        self.update_statistics()
        newly_unlocked = self.achievement_manager.check_achievements()
        if newly_unlocked:
            self.save_achievements()
            for ach in newly_unlocked:
                xp_reward = 50
                self.add_xp(xp_reward)
                self.tray_icon.showMessage(
                    "🏆 Achievement Unlocked!",
                    f"{ach.icon} {ach.name}\n+{xp_reward} XP",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )
    
    def play_game_fullscreen(self, game):
        """Play game in fullscreen window"""
        # Update game stats
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
        
        # Create and show fullscreen window
        self.fullscreen_window = FullscreenGameWindow(self)
        self.fullscreen_window.closed.connect(self.on_fullscreen_closed)
        
        # Check if game is downloaded locally
        if game.is_downloaded and game.local_path:
            html_file = Path(game.local_path)
            if html_file.exists():
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                # Use baseUrl so relative paths work
                base_url = QUrl.fromLocalFile(str(html_file.parent / ""))
                self.fullscreen_window.web_view.setHtml(html_content, base_url)
            else:
                self.fullscreen_window.set_url(QUrl(game.url))
        else:
            self.fullscreen_window.set_url(QUrl(game.url))
        
        # Start timers
        self.play_timer.start(1000)
        if self.settings_manager.get('notifications_enabled', True):
            reminder_minutes = self.settings_manager.get('play_reminder_minutes', 60)
            self.notification_timer.start(reminder_minutes * 60 * 1000)
        
        # Show fullscreen window
        self.fullscreen_window.show()
        
        # Save game data
        self.game_manager.save_game_data()
        self.update_statistics()
        
        # Check achievements
        newly_unlocked = self.achievement_manager.check_achievements()
        if newly_unlocked:
            self.save_achievements()
            for ach in newly_unlocked:
                xp_reward = 50
                self.add_xp(xp_reward)
                self.tray_icon.showMessage(
                    "🏆 Achievement Unlocked!",
                    f"{ach.icon} {ach.name}\n+{xp_reward} XP",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )
    
    def on_fullscreen_closed(self):
        """Handle fullscreen window close"""
        # Stop timers when fullscreen closes
        self.play_timer.stop()
        self.notification_timer.stop()
        self.fullscreen_window = None
        self.current_game = None
    
    def download_game_files(self, game):
        """Download game files locally"""
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText(f"⬇️ Downloading {game.name}...")
        
        result = self.download_manager.download_website(game.url, game.name)
        
        if result['success']:
            game.local_path = str(result['html_file'])
            game.is_downloaded = True
            self.game_manager.save_game_data()
            if hasattr(self.games_tab, 'status_label'):
                self.games_tab.status_label.setText(f"✅ {game.name} downloaded successfully!")
            QMessageBox.information(self, "Download Complete", 
                                  f"{game.name} has been downloaded locally!\n"
                                  f"You can now play it offline.")
        else:
            if hasattr(self.games_tab, 'status_label'):
                self.games_tab.status_label.setText(f"❌ Download failed: {result.get('error', 'Unknown error')}")
            QMessageBox.warning(self, "Download Failed", 
                              f"Failed to download {game.name}:\n{result.get('error', 'Unknown error')}")
    
    def add_xp(self, amount):
        """Add XP and check for level up"""
        self.total_xp += amount
        
        while self.total_xp >= self.xp_for_next_level():
            self.total_xp -= self.xp_for_next_level()
            self.user_level += 1
            self.show_level_up_notification()
        
        self.update_profile_display()
        self.settings_manager.set('total_xp', self.total_xp)
        self.settings_manager.set('user_level', self.user_level)
    
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
        """Update play time"""
        if self.current_game and self.game_start_time:
            self.current_game.total_time += 1
            if self.settings_manager.get('auto_save', True) and self.current_game.total_time % 60 == 0:
                self.game_manager.save_game_data()
    
    def show_play_reminder(self):
        """Show play reminder"""
        if self.current_game:
            elapsed = (datetime.now() - self.game_start_time).total_seconds()
            minutes = int(elapsed / 60)
            self.tray_icon.showMessage(
                "⏰ Gaming Reminder",
                f"You've been playing {self.current_game.name} for {minutes} minutes!",
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )
    
    def update_favorites_list(self):
        """Update favorites list"""
        self.favorites_list.clear()
        
        for game in self.game_manager.games:
            if game.favorite and game.icon:
                item = QListWidgetItem(game.icon, game.name)
                item.setData(Qt.ItemDataRole.UserRole, game)
                self.favorites_list.addItem(item)
    
    def play_favorite(self, item):
        """Play a favorite game"""
        game = item.data(Qt.ItemDataRole.UserRole)
        self.tabs.setCurrentIndex(0)
        self.play_game(game)
    
    def play_random_game(self):
        """Play a random game"""
        if self.game_manager.games:
            game = random.choice(self.game_manager.games)
            self.tabs.setCurrentIndex(0)
            self.play_game(game)
            QMessageBox.information(self, "Random Game", f"🎲 Playing: {game.name}")
    
    def update_statistics(self):
        """Update statistics table"""
        self.stats_table.setRowCount(len(self.game_manager.games))
        
        for i, game in enumerate(self.game_manager.games):
            self.stats_table.setItem(i, 0, QTableWidgetItem(game.name))
            self.stats_table.setItem(i, 1, QTableWidgetItem(game.category))
            self.stats_table.setItem(i, 2, QTableWidgetItem(str(game.play_count)))
            
            time_hours = game.total_time // 3600
            time_mins = (game.total_time % 3600) // 60
            self.stats_table.setItem(i, 3, QTableWidgetItem(f"{time_hours}h {time_mins}m"))
            
            last_played = game.last_played.strftime('%Y-%m-%d') if game.last_played else "Never"
            self.stats_table.setItem(i, 4, QTableWidgetItem(last_played))
            
            rating_text = f"{'⭐' * game.rating}" if game.rating > 0 else "-"
            self.stats_table.setItem(i, 5, QTableWidgetItem(rating_text))
            
            self.stats_table.setItem(i, 6, QTableWidgetItem(f"{game.streak} days" if game.streak > 0 else "-"))
    
    def clear_history(self):
        """Clear game history"""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all game history? This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for game in self.game_manager.games:
                game.play_count = 0
                game.total_time = 0
                game.last_played = None
                game.streak = 0
            
            self.game_manager.save_game_data()
            self.update_statistics()
            QMessageBox.information(self, "Success", "Game history cleared!")
    
    def save_achievements(self):
        """Save achievements to game data"""
        data_file = self.settings_manager.settings_file.parent / "game_data.json"
        try:
            import json
            if data_file.exists():
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            data['achievements'] = self.achievement_manager.save_achievements()
            
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
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
        """Update game recommendations with enhanced algorithm"""
        self.recommendations_list.clear()
        
        recommended = []
        
        # 1. Recommend unplayed games (highest priority)
        unplayed = [g for g in self.game_manager.games if g.play_count == 0]
        for game in unplayed[:4]:
            recommended.append(("🎮 New Game - Try this!", game))
        
        # 2. Recommend games in favorite categories
        favorite_categories = set()
        for game in self.game_manager.games:
            if game.favorite:
                favorite_categories.add(game.category)
        
        for game in self.game_manager.games:
            if game.category in favorite_categories and game.play_count > 0 and game not in [r[1] for r in recommended]:
                if len(recommended) < 8:
                    recommended.append(("⭐ Similar to your favorites", game))
        
        # 3. Add highly rated games
        highly_rated = sorted([g for g in self.game_manager.games if g.rating >= 4], 
                             key=lambda x: x.rating, reverse=True)
        for game in highly_rated[:3]:
            if len(recommended) < 10 and game not in [r[1] for r in recommended]:
                recommended.append(("🌟 Highly Rated", game))
        
        # 4. Recommend games with long play time (user enjoys them)
        long_play = sorted([g for g in self.game_manager.games if g.total_time > 1800], 
                          key=lambda x: x.total_time, reverse=True)
        for game in long_play[:2]:
            if len(recommended) < 12 and game not in [r[1] for r in recommended]:
                recommended.append(("⏱️ You've played this a lot", game))
        
        # 5. Recommend games with streaks
        streak_games = sorted([g for g in self.game_manager.games if g.streak > 0], 
                            key=lambda x: x.streak, reverse=True)
        for game in streak_games[:2]:
            if len(recommended) < 14 and game not in [r[1] for r in recommended]:
                recommended.append(("🔥 On a streak!", game))
        
        # Display recommendations
        for reason, game in recommended:
            if game.icon:
                item = QListWidgetItem(game.icon, f"{game.name}\n{reason}")
                item.setData(Qt.ItemDataRole.UserRole, game)
                item.setToolTip(f"{game.description}\nCategory: {game.category} | Difficulty: {game.difficulty}")
                self.recommendations_list.addItem(item)
        
        # Update info label
        if hasattr(self, 'recommendations_info'):
            self.recommendations_info.setText(f"Showing {len(recommended)} personalized recommendations")
    
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
                    for game in self.game_manager.games:
                        total_mins = game.total_time // 60
                        f.write(f"{game.name},{game.category},{game.difficulty},{game.play_count},{total_mins},{game.rating},{game.favorite},{game.streak}\n")
                
                QMessageBox.information(self, "Success", f"Statistics exported to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def take_screenshot(self):
        """Take screenshot of current game"""
        if self.current_game:
            screenshots_dir = self.settings_manager.settings_file.parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"{self.current_game.name}_{timestamp}.png"
            
            # Take screenshot of web view
            pixmap = self.games_tab.web_view.grab()
            pixmap.save(str(filename))
            
            if hasattr(self.games_tab, 'status_label'):
                self.games_tab.status_label.setText(f"📷 Screenshot saved!")
            QMessageBox.information(self, "Screenshot", f"Screenshot saved to:\n{filename}")
        else:
            QMessageBox.warning(self, "No Game", "Please start a game first!")
    
    def go_home(self):
        """Go to home screen"""
        self.show_welcome_screen()
        self.play_timer.stop()
        self.notification_timer.stop()
        self.current_game = None
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText("Ready")
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        theme = self.settings_manager.get('theme', 'light')
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
                    Level {self.user_level} | {self.game_manager.total_games_played()} Games Played
                </div>
                <div class="version">v{self.version} by sugarypumpkin822</div>
            </div>
        </body>
        </html>
        """
        self.games_tab.web_view.setHtml(html)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
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
        self.settings_manager.set('theme', theme)
        self.apply_theme()
        if dialog:
            dialog.accept()
    
    def apply_theme(self):
        """Apply theme styles"""
        theme = self.settings_manager.get('theme', 'light')
        
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
        """Apply toolbar style"""
        if self.settings_manager.get('theme', 'light') == 'dark':
            toolbar.setStyleSheet("QWidget { background-color: #34495e; padding: 5px; }")
        else:
            toolbar.setStyleSheet("QWidget { background-color: #3498db; color: white; padding: 5px; }")
    
    def show_settings(self):
        """Show settings dialog"""
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
        update_check.setChecked(self.settings_manager.get('check_updates', True))
        general_layout.addWidget(update_check)
        
        auto_save = QCheckBox("Auto-save game data")
        auto_save.setChecked(self.settings_manager.get('auto_save', True))
        general_layout.addWidget(auto_save)
        
        download_locally = QCheckBox("Download games locally when possible")
        download_locally.setChecked(self.settings_manager.get('download_games_locally', False))
        general_layout.addWidget(download_locally)
        
        auto_download_updates = QCheckBox("Auto-download updates when available")
        auto_download_updates.setChecked(self.settings_manager.get('auto_download_updates', False))
        general_layout.addWidget(auto_download_updates)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save")
        cancel_btn = QPushButton("❌ Cancel")
        
        def save_settings_dialog():
            self.username = username_input.text()
            self.settings_manager.set('username', self.username)
            self.settings_manager.set('check_updates', update_check.isChecked())
            self.settings_manager.set('auto_save', auto_save.isChecked())
            self.settings_manager.set('download_games_locally', download_locally.isChecked())
            self.settings_manager.set('auto_download_updates', auto_download_updates.isChecked())
            self.update_profile_display()
            dialog.accept()
            QMessageBox.information(self, "Success", "Settings saved!")
        
        save_btn.clicked.connect(save_settings_dialog)
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
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
        ✅ Fullscreen mode<br>
        ✅ Download games locally<br>
        ✅ Track statistics & achievements<br>
        ✅ Daily challenges<br>
        ✅ Level up system<br>
        ✅ Multiple themes<br>
        ✅ And much more!<br><br>
        
        <b>Quick Tips:</b><br>
        • Use <b>Ctrl+F</b> to search games<br>
        • Press <b>F11</b> for fullscreen<br>
        • Check out the Daily Challenge tab!<br>
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
        self.settings_manager.set('welcomed', True)
        self.settings_manager.set('username', username)
        self.update_profile_display()
        dialog.accept()
        QMessageBox.information(self, "Welcome!", f"Welcome, {username}! 🎉\nEnjoy your gaming experience!")
    
    def check_for_updates(self):
        """Check for updates"""
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText("Checking for updates...")
        
        self.update_checker = UpdateChecker(self.version, self.github_repo)
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.no_update.connect(self.on_no_update)
        self.update_checker.finished.connect(lambda: self.games_tab.status_label.setText("Ready") if hasattr(self.games_tab, 'status_label') else None)
        self.update_checker.start()
    
    def on_no_update(self):
        """Handle no update available"""
        if hasattr(self.games_tab, 'status_label'):
            self.games_tab.status_label.setText("✅ You're on the latest version!")
        QMessageBox.information(self, "No Updates", "You're already running the latest version!")
    
    def on_update_available(self, latest_version, url, release_data):
        """Handle update available"""
        auto_download = self.settings_manager.get('auto_download_updates', False)
        
        if auto_download:
            # Auto-download the update
            self.download_update(latest_version, url, release_data)
        else:
            # Ask user first
            reply = QMessageBox.question(
                self,
                "🔄 Update Available",
                f"Version {latest_version} is available!\n\nCurrent version: {self.version}\n\nWould you like to download it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.download_update(latest_version, url, release_data)
    
    def download_update(self, version, url, release_data):
        """Download the update"""
        try:
            # Find the download URL (look for zip or exe files)
            assets = release_data.get('assets', [])
            download_url = None
            filename = None
            
            # Prefer .zip files, then .exe, then any other asset
            for asset in assets:
                asset_name = asset.get('name', '')
                if asset_name.endswith('.zip'):
                    download_url = asset.get('browser_download_url')
                    filename = asset_name
                    break
                elif asset_name.endswith('.exe') and not download_url:
                    download_url = asset.get('browser_download_url')
                    filename = asset_name
            
            if not download_url and assets:
                # Use first asset as fallback
                download_url = assets[0].get('browser_download_url')
                filename = assets[0].get('name', 'update.zip')
            
            if download_url:
                # Download to user's Downloads folder
                downloads_path = Path.home() / "Downloads"
                downloads_path.mkdir(exist_ok=True)
                filepath = downloads_path / filename
                
                if hasattr(self.games_tab, 'status_label'):
                    self.games_tab.status_label.setText(f"⬇️ Downloading update {version}...")
                
                # Show progress dialog
                from PyQt6.QtWidgets import QProgressDialog
                progress = QProgressDialog(f"Downloading {filename}...", "Cancel", 0, 100, self)
                progress.setWindowTitle("Downloading Update")
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setMinimumDuration(0)
                progress.show()
                
                # Download the file
                response = requests.get(download_url, stream=True, timeout=60)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if progress.wasCanceled():
                            filepath.unlink(missing_ok=True)
                            progress.close()
                            if hasattr(self.games_tab, 'status_label'):
                                self.games_tab.status_label.setText("Download cancelled")
                            return
                        
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                progress_value = int((downloaded / total_size) * 100)
                                progress.setValue(progress_value)
                
                progress.close()
                
                if hasattr(self.games_tab, 'status_label'):
                    self.games_tab.status_label.setText(f"✅ Update downloaded to Downloads folder")
                
                reply = QMessageBox.question(
                    self,
                    "✅ Download Complete",
                    f"Update {version} has been downloaded to:\n{filepath}\n\nWould you like to open the folder?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    import os
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(filepath.parent)
                    elif platform.system() == "Darwin":  # macOS
                        os.system(f"open '{filepath.parent}'")
                    else:  # Linux
                        os.system(f"xdg-open '{filepath.parent}'")
            else:
                # No downloadable asset, just open the release page
                QMessageBox.information(
                    self,
                    "Update Available",
                    f"Version {version} is available!\n\nOpening release page in browser..."
                )
                self.open_url(url)
        except Exception as e:
            QMessageBox.warning(
                self,
                "Download Error",
                f"Failed to download update:\n{str(e)}\n\nOpening release page in browser instead."
            )
            self.open_url(url)
    
    def open_url(self, url):
        """Open URL in browser"""
        webbrowser.open(url)
    
    def closeEvent(self, event):
        """Handle close event"""
        self.game_manager.save_game_data()
        self.save_achievements()
        self.settings_manager.set('total_xp', self.total_xp)
        self.settings_manager.set('user_level', self.user_level)
        event.accept()

