"""Games tab component"""
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                             QListWidgetItem, QLineEdit, QComboBox, QCheckBox,
                             QLabel, QPushButton, QTextEdit, QSlider, QFrame,
                             QGroupBox, QSplitter)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView


class GamesTab(QWidget):
    """Games tab widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        
        # Left panel - make it wider for better game list visibility
        left_panel = QWidget()
        left_panel.setMinimumWidth(650)
        left_panel.setMaximumWidth(900)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(10)
        
        # Search - more compact
        search_container = QHBoxLayout()
        search_container.setSpacing(8)
        search_label = QLabel("🔍")
        search_label.setFont(QFont("Arial", 12))
        search_container.addWidget(search_label)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search games... (Ctrl+F)")
        self.search_box.setMinimumHeight(32)
        self.search_box.textChanged.connect(self.filter_games)
        search_container.addWidget(self.search_box)
        left_layout.addLayout(search_container)
        
        # Filters - make them horizontal and more compact
        filters_container = QWidget()
        filters_layout = QHBoxLayout(filters_container)
        filters_layout.setContentsMargins(0, 0, 0, 0)
        filters_layout.setSpacing(8)
        
        category_label = QLabel("Category:")
        category_label.setFont(QFont("Arial", 9))
        filters_layout.addWidget(category_label)
        self.category_filter = QComboBox()
        self.category_filter.setMinimumHeight(28)
        self.category_filter.addItems(["All", "Restaurant", "Fast Food", "Dessert", 
                                      "Italian", "Mexican", "Breakfast", "Bakery", "Adventure"])
        self.category_filter.currentTextChanged.connect(self.filter_games)
        filters_layout.addWidget(self.category_filter)
        
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setFont(QFont("Arial", 9))
        filters_layout.addWidget(difficulty_label)
        self.difficulty_filter = QComboBox()
        self.difficulty_filter.setMinimumHeight(28)
        self.difficulty_filter.addItems(["All", "Easy", "Medium", "Hard"])
        self.difficulty_filter.currentTextChanged.connect(self.filter_games)
        filters_layout.addWidget(self.difficulty_filter)
        
        sort_label = QLabel("Sort:")
        sort_label.setFont(QFont("Arial", 9))
        filters_layout.addWidget(sort_label)
        self.sort_combo = QComboBox()
        self.sort_combo.setMinimumHeight(28)
        self.sort_combo.addItems(["Name", "Most Played", "Recently Played", 
                                 "Highest Rated", "Difficulty", "Play Time", "Streak"])
        self.sort_combo.currentTextChanged.connect(self.sort_games)
        filters_layout.addWidget(self.sort_combo)
        
        left_layout.addWidget(filters_container)
        
        # View options - make them horizontal checkboxes
        view_options_layout = QHBoxLayout()
        view_options_layout.setSpacing(12)
        
        self.show_unplayed = QCheckBox("Unplayed only")
        self.show_unplayed.stateChanged.connect(self.filter_games)
        view_options_layout.addWidget(self.show_unplayed)
        
        self.show_favorites_only = QCheckBox("Favorites")
        self.show_favorites_only.stateChanged.connect(self.filter_games)
        view_options_layout.addWidget(self.show_favorites_only)
        
        self.show_downloaded_only = QCheckBox("Downloaded")
        self.show_downloaded_only.stateChanged.connect(self.filter_games)
        view_options_layout.addWidget(self.show_downloaded_only)
        view_options_layout.addStretch()
        
        left_layout.addLayout(view_options_layout)
        
        # Game list - make it take up most of the space
        list_label = QLabel("📋 Games")
        list_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        left_layout.addWidget(list_label)
        
        self.game_list = QListWidget()
        self.game_list.setIconSize(QSize(56, 56))  # Slightly smaller icons for more items visible
        self.game_list.setSpacing(4)  # Reduced spacing
        self.game_list.itemClicked.connect(self.on_game_selected)
        self.game_list.setAlternatingRowColors(True)
        # Give game list stretch priority so it takes most of the vertical space
        left_layout.addWidget(self.game_list, stretch=10)
        
        # Game info panel - make it more compact
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_frame.setMaximumHeight(180)  # Limit height to give more space to game list
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(6)
        info_layout.setContentsMargins(10, 10, 10, 10)
        
        # Compact header
        header_layout = QHBoxLayout()
        self.game_title_label = QLabel("No game selected")
        self.game_title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.game_title_label.setWordWrap(True)
        header_layout.addWidget(self.game_title_label)
        info_layout.addLayout(header_layout)
        
        self.game_stats_label = QLabel("")
        self.game_stats_label.setFont(QFont("Arial", 8))
        info_layout.addWidget(self.game_stats_label)
        
        # Compact action buttons and rating in one row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)
        
        # Rating - compact
        rating_label = QLabel("⭐")
        rating_label.setFont(QFont("Arial", 10))
        controls_layout.addWidget(rating_label)
        self.rating_slider = QSlider(Qt.Orientation.Horizontal)
        self.rating_slider.setMinimum(0)
        self.rating_slider.setMaximum(5)
        self.rating_slider.setMaximumWidth(100)
        self.rating_slider.valueChanged.connect(self.rate_game)
        controls_layout.addWidget(self.rating_slider)
        self.rating_label = QLabel("0/5")
        self.rating_label.setFont(QFont("Arial", 9))
        self.rating_label.setMinimumWidth(35)
        controls_layout.addWidget(self.rating_label)
        
        controls_layout.addStretch()
        
        # Action buttons - compact
        self.favorite_btn = QPushButton("⭐")
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setMaximumWidth(40)
        self.favorite_btn.setMaximumHeight(28)
        self.favorite_btn.setToolTip("Toggle favorite")
        self.favorite_btn.clicked.connect(self.toggle_favorite)
        controls_layout.addWidget(self.favorite_btn)
        
        self.play_btn = QPushButton("▶️ Play")
        self.play_btn.setMaximumHeight(28)
        self.play_btn.clicked.connect(self.play_selected_game)
        controls_layout.addWidget(self.play_btn)
        
        self.fullscreen_btn = QPushButton("⛶ Full")
        self.fullscreen_btn.setMaximumHeight(28)
        self.fullscreen_btn.setToolTip("Play in fullscreen")
        self.fullscreen_btn.clicked.connect(self.play_fullscreen)
        controls_layout.addWidget(self.fullscreen_btn)
        
        info_layout.addLayout(controls_layout)
        
        left_layout.addWidget(info_frame)
        
        # Compact control buttons in one row
        controls_row = QHBoxLayout()
        controls_row.setSpacing(6)
        
        self.home_btn = QPushButton("🏠")
        self.home_btn.setMaximumWidth(40)
        self.home_btn.setMaximumHeight(28)
        self.home_btn.setToolTip("Go to home screen")
        self.home_btn.clicked.connect(self.go_home)
        controls_row.addWidget(self.home_btn)
        
        screenshot_btn = QPushButton("📷")
        screenshot_btn.setMaximumWidth(40)
        screenshot_btn.setMaximumHeight(28)
        screenshot_btn.setToolTip("Take screenshot")
        screenshot_btn.clicked.connect(self.take_screenshot)
        controls_row.addWidget(screenshot_btn)
        
        download_btn = QPushButton("⬇️")
        download_btn.setMaximumWidth(40)
        download_btn.setMaximumHeight(28)
        download_btn.setToolTip("Download game locally")
        download_btn.clicked.connect(self.download_game)
        controls_row.addWidget(download_btn)
        
        controls_row.addStretch()
        
        # Status label - compact
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 8))
        self.status_label.setStyleSheet("color: #666;")
        controls_row.addWidget(self.status_label)
        
        left_layout.addLayout(controls_row)
        
        # Right panel - web view
        self.web_view = QWebEngineView()
        
        # Right panel - web view with label
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(5)
        
        web_label = QLabel("🎮 Game Preview")
        web_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        right_layout.addWidget(web_label)
        
        self.web_view = QWebEngineView()
        right_layout.addWidget(self.web_view)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)  # Give more stretch to left panel
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([700, 1000])  # Wider left panel by default
        
        layout.addWidget(splitter)
    
    def populate_game_list(self, games):
        """Populate the game list"""
        self.game_list.clear()
        
        placeholder_pixmap = QPixmap(64, 64)
        placeholder_pixmap.fill(Qt.GlobalColor.lightGray)
        placeholder_icon = QIcon(placeholder_pixmap)
        
        for game in games:
            item = QListWidgetItem(placeholder_icon, game.name)
            item.setData(Qt.ItemDataRole.UserRole, game)
            self.game_list.addItem(item)
    
    def on_game_selected(self, item):
        """Handle game selection"""
        if not self.main_window:
            return
        
        game = item.data(Qt.ItemDataRole.UserRole)
        
        difficulty_colors = {'Easy': '🟢', 'Medium': '🟡', 'Hard': '🔴'}
        diff_emoji = difficulty_colors.get(game.difficulty, '⚪')
        
        # Compact title with category
        self.game_title_label.setText(f"{game.name} {diff_emoji} | {game.category}")
        
        # Compact stats on one line
        stats_parts = [f"🎮 {game.play_count} plays"]
        if game.total_time > 0:
            hours = game.total_time // 3600
            minutes = (game.total_time % 3600) // 60
            if hours > 0:
                stats_parts.append(f"⏱️ {hours}h")
            else:
                stats_parts.append(f"⏱️ {minutes}m")
        if game.last_played:
            stats_parts.append(f"📅 {game.last_played.strftime('%m/%d')}")
        if game.streak > 0:
            stats_parts.append(f"🔥 {game.streak}")
        
        self.game_stats_label.setText(" | ".join(stats_parts))
        
        self.favorite_btn.setChecked(game.favorite)
        self.rating_slider.setValue(game.rating)
        self.rating_label.setText(f"{game.rating}/5")
    
    def save_game_notes(self):
        """Save notes for current game - removed notes field in compact layout"""
        pass  # Notes feature removed for compact layout
    
    def play_selected_game(self):
        """Play the selected game"""
        item = self.game_list.currentItem()
        if item and self.main_window:
            game = item.data(Qt.ItemDataRole.UserRole)
            self.main_window.play_game(game)
    
    def play_fullscreen(self):
        """Play game in fullscreen"""
        item = self.game_list.currentItem()
        if item and self.main_window:
            game = item.data(Qt.ItemDataRole.UserRole)
            self.main_window.play_game_fullscreen(game)
    
    def toggle_favorite(self):
        """Toggle favorite status"""
        item = self.game_list.currentItem()
        if item and self.main_window:
            game = item.data(Qt.ItemDataRole.UserRole)
            game.favorite = self.favorite_btn.isChecked()
            self.main_window.game_manager.save_game_data()
            self.main_window.update_favorites_list()
            self.main_window.achievement_manager.check_achievements()
    
    def rate_game(self, value):
        """Rate the game"""
        item = self.game_list.currentItem()
        if item and self.main_window:
            game = item.data(Qt.ItemDataRole.UserRole)
            game.rating = value
            self.rating_label.setText(f"{value}/5")
            self.main_window.game_manager.save_game_data()
            self.main_window.update_statistics()
            self.main_window.achievement_manager.check_achievements()
    
    def filter_games(self):
        """Filter games based on criteria"""
        if not self.main_window:
            return
        
        category = self.category_filter.currentText()
        difficulty = self.difficulty_filter.currentText()
        search_text = self.search_box.text().lower()
        show_unplayed_only = self.show_unplayed.isChecked()
        show_favorites_only = getattr(self, 'show_favorites_only', None) and self.show_favorites_only.isChecked()
        show_downloaded_only = getattr(self, 'show_downloaded_only', None) and self.show_downloaded_only.isChecked()
        
        for i in range(self.game_list.count()):
            item = self.game_list.item(i)
            game = item.data(Qt.ItemDataRole.UserRole)
            
            category_match = category == "All" or game.category == category
            difficulty_match = difficulty == "All" or game.difficulty == difficulty
            search_match = search_text in game.name.lower() or search_text in game.description.lower()
            unplayed_match = not show_unplayed_only or game.play_count == 0
            favorites_match = not show_favorites_only or game.favorite
            downloaded_match = not show_downloaded_only or game.is_downloaded
            
            item.setHidden(not (category_match and difficulty_match and search_match and 
                              unplayed_match and favorites_match and downloaded_match))
    
    def sort_games(self, sort_by):
        """Sort games"""
        if not self.main_window:
            return
        
        from datetime import datetime
        
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
        elif sort_by == "Play Time":
            games.sort(key=lambda g: g.total_time, reverse=True)
        elif sort_by == "Streak":
            games.sort(key=lambda g: g.streak, reverse=True)
        else:
            games.sort(key=lambda g: g.name)
        
        self.populate_game_list(games)
        if self.main_window:
            self.main_window.load_icons()
    
    def go_home(self):
        """Go to home screen"""
        if self.main_window:
            self.main_window.go_home()
    
    def take_screenshot(self):
        """Take screenshot"""
        if self.main_window:
            self.main_window.take_screenshot()
    
    def download_game(self):
        """Download game files"""
        item = self.game_list.currentItem()
        if item and self.main_window:
            game = item.data(Qt.ItemDataRole.UserRole)
            self.main_window.download_game_files(game)

