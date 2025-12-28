# 🎮 Papa's Games Launcher

The ultimate, feature-packed launcher for all Papa's games from Poki! Enjoy all your favorite Papa Louie restaurant games with advanced tracking, achievements, fullscreen mode, and local game downloads.

## ✨ Features

### 🎯 Core Features
- **Play all 14 Papa's games** in-app with embedded browser
- **Fullscreen game mode** - Immersive gaming experience with dedicated fullscreen window
- **Local game downloads** - Download HTML, CSS, and JS files to play games offline
- **Comprehensive statistics tracking** - Track play time, play counts, streaks, and more
- **Achievements system** - 11+ achievements to unlock
- **Daily challenges** - New challenges every day
- **Smart game recommendations** - Personalized recommendations based on your play history
- **User leveling system** - Gain XP and level up as you play
- **Game notes and favorites** - Organize and rate your favorite games

### 🎨 UI Features
- **Multiple themes** - 6 beautiful themes (Light, Dark, Ocean, Forest, Sunset, Purple)
- **Modern interface** - Clean and intuitive design
- **System tray integration** - Minimize to tray and quick access
- **Keyboard shortcuts** - Fast navigation and actions
- **Screenshot capture** - Capture your gaming moments
- **Export statistics** - Export your stats to CSV

### 🔧 Technical Features
- **Modular architecture** - Clean, organized codebase with separate modules
- **Offline support** - Download and play games locally
- **Auto-update notifications** - Stay up to date with the latest version
- **Performance mode** - Optimize for better performance
- **Auto-save** - Automatic saving of game data and settings

## 📁 Project Structure

```
website-games-launcher/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # License file
│
├── models/                # Data models
│   ├── __init__.py
│   ├── game_item.py      # Game item model
│   ├── achievement.py    # Achievement model
│   └── daily_challenge.py # Daily challenge model
│
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── game_manager.py   # Game data management
│   ├── settings_manager.py # Settings management
│   ├── achievement_manager.py # Achievement system
│   └── download_manager.py # Website download functionality
│
├── gui/                  # GUI components
│   ├── __init__.py
│   ├── main_window.py    # Main application window
│   ├── tabs/            # Tab components
│   │   ├── __init__.py
│   │   └── games_tab.py  # Games tab
│   └── widgets/         # Custom widgets
│       ├── __init__.py
│       └── fullscreen_game_window.py # Fullscreen game window
│
└── utils/                # Utilities
    ├── __init__.py
    ├── update_checker.py # Update checking
    └── daily_challenge_generator.py # Challenge generation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sugarypumpkin822/website-games-launcher.git
   cd website-games-launcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

### Getting Started

1. **First Launch**: On first launch, you'll see a welcome dialog where you can set your username.

2. **Playing Games**:
   - Select a game from the Games tab
   - Click "▶️ Play" to play in the embedded browser
   - Click "⛶ Fullscreen" to play in fullscreen mode
   - Press `F11` to toggle fullscreen

3. **Downloading Games Locally**:
   - Select a game
   - Click "⬇️ Download" to download HTML, CSS, and JS files
   - Games will be cached locally for offline play
   - Downloaded games will automatically use local files when available

4. **Fullscreen Mode**:
   - Click the "⛶ Fullscreen" button or press `F11`
   - Move mouse to top of screen to show exit button
   - Press `Escape` to exit fullscreen

### Keyboard Shortcuts

- `Ctrl+F` - Focus search box
- `Ctrl+H` - Go to home screen
- `F11` - Toggle fullscreen
- `Ctrl+S` - Open settings
- `Ctrl+Q` - Quit application
- `Escape` - Exit fullscreen (when in fullscreen mode)

### Features Guide

#### Statistics
- View your total play time, play counts, and streaks
- Export statistics to CSV for analysis
- Clear history if needed

#### Achievements
- Unlock achievements by completing various tasks
- Earn XP rewards for unlocking achievements
- Track your progress

#### Daily Challenges
- Complete daily challenges for bonus XP
- Challenges reset every day
- Track your challenge history

#### Recommendations
- Get personalized game recommendations
- Based on your play history and preferences
- Refresh recommendations anytime

#### Themes
- Choose from 6 beautiful themes
- Themes affect the entire application
- Settings are saved automatically

## 🎮 Games Included

1. Papa's Wingeria
2. Papa's Freezeria
3. Papa's Sushiria
4. Papa's Pastaria
5. Papa's Pancakeria
6. Papa's Donuteria
7. Papa's Bakeria
8. Papa's Taco Mia
9. Papa's Cupcakeria
10. Papa's Hotdoggeria
11. Papa's Burgeria
12. Papa's Pizzeria
13. Papa's Cheeseria
14. Papa Louie: When Pizzas Attack

## 🔧 Configuration

Settings are stored in `~/.papas_launcher/settings.json`. You can modify:
- Theme preferences
- Auto-save settings
- Update checking
- Notification preferences
- Download preferences

Game data is stored in `~/.papas_launcher/game_data.json`.

Downloaded games are cached in `~/.papas_launcher/cache/`.

## 🛠️ Development

### Project Structure

The project is organized into several modules:

- **models/**: Data models for games, achievements, and challenges
- **core/**: Core functionality including game management, settings, achievements, and downloads
- **gui/**: GUI components including the main window, tabs, and widgets
- **utils/**: Utility functions for updates and challenge generation

### Adding New Features

1. **New Game**: Add to `core/game_manager.py` in the `_initialize_games()` method
2. **New Achievement**: Add to `core/achievement_manager.py` in the `_initialize_achievements()` method
3. **New Theme**: Add to `gui/main_window.py` in the `available_themes` dictionary and `apply_theme()` method

## 📝 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Games**: Created by Flipline Studios, hosted on Poki.com
- **Developer**: sugarypumpkin822
- **Framework**: PyQt6
- **Icons**: Game icons from Poki.com

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Reporting Issues

If you encounter any bugs or have feature requests, please open an issue on GitHub.

## 📧 Support

For support, please open an issue on the GitHub repository or contact the developer.

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by sugarypumpkin822**
