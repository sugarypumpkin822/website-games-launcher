# 🎮 Papa's Games Launcher

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-AGPL--3.0-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**The ultimate, feature-packed launcher for all Papa's games from Poki!**

Enjoy all your favorite Papa Louie restaurant games with advanced tracking, achievements, fullscreen mode, and local game downloads.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Games](#-games-included) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Games Included](#-games-included)
- [Configuration](#-configuration)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Features Deep Dive](#-features-deep-dive)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Changelog](#-changelog)
- [License](#-license)
- [Credits](#-credits)
- [Contributing](#-contributing)
- [Support](#-support)

---

## ✨ Features

### 🎯 Core Features

- **Play all 14 Papa's games** in-app with embedded browser
  - Seamless integration with Poki.com
  - No need to open external browsers
  - Instant game loading with caching
  
- **Fullscreen game mode** - Immersive gaming experience
  - Dedicated fullscreen window with auto-hide controls
  - F11 quick toggle support
  - Smooth transitions and animations
  - Exit button appears on mouse hover
  
- **Local game downloads** - True offline gaming
  - Download complete HTML, CSS, and JS files
  - Games cached locally in `~/.papas_launcher/cache/`
  - Automatic fallback to local files when offline
  - One-click download for any game
  - Progress tracking during downloads
  
- **Comprehensive statistics tracking**
  - Total play time per game
  - Play count tracking
  - Daily, weekly, and monthly streaks
  - Last played timestamps
  - First played dates
  - Average session length
  - Most played games rankings
  
- **Achievements system** - 11+ achievements to unlock
  - "First Timer" - Play your first game
  - "Marathon Player" - Play for 2 hours straight
  - "Completionist" - Play all 14 games
  - "Streak Master" - Maintain a 7-day streak
  - "Night Owl" - Play between midnight and 6 AM
  - "Early Bird" - Play between 6 AM and 9 AM
  - "Variety Seeker" - Play 5 different games in one day
  - "Dedicated Player" - Reach 10 hours total play time
  - "Loyal Fan" - Play for 30 days total
  - "Speed Runner" - Play 10 games in one day
  - "Champion" - Unlock all other achievements
  - Each achievement grants XP rewards
  
- **Daily challenges** - New challenges every day
  - Randomly generated challenges
  - Play specific games
  - Achieve play time goals
  - Complete streak challenges
  - Bonus XP rewards for completion
  - Challenge history tracking
  
- **Smart game recommendations** - AI-powered suggestions
  - Based on your play history
  - Considers favorite games
  - Takes into account recent activity
  - Suggests games you haven't tried
  - Refresh recommendations anytime
  
- **User leveling system** - RPG-style progression
  - Gain XP from playing games
  - Level up based on cumulative XP
  - Unlock achievements for XP bonuses
  - Complete daily challenges for extra XP
  - Visual level display with progress bar
  
- **Game notes and favorites** - Personal organization
  - Add custom notes to any game
  - Rate games with 1-5 stars
  - Mark games as favorites
  - Filter and sort by favorites
  - Quick access to favorite games

### 🎨 UI Features

- **Multiple themes** - 6 beautiful, carefully designed themes
  - **Light Theme** - Clean and bright for daytime use
  - **Dark Theme** - Easy on the eyes for night gaming
  - **Ocean Theme** - Calming blue tones inspired by the sea
  - **Forest Theme** - Natural green aesthetics
  - **Sunset Theme** - Warm orange and purple gradients
  - **Purple Theme** - Royal purple accents
  - Instant theme switching
  - Theme affects entire application
  - Custom color schemes for each theme
  
- **Modern interface** - Clean and intuitive design
  - Card-based game display
  - Smooth animations and transitions
  - Responsive layout that adapts to window size
  - Clear visual hierarchy
  - Intuitive navigation
  - Contextual tooltips
  
- **System tray integration** - Convenient background operation
  - Minimize to system tray
  - Quick access menu from tray icon
  - Notification support
  - Double-click to restore window
  - Right-click menu with common actions
  - Close to tray option
  
- **Keyboard shortcuts** - Power user features
  - Fast navigation between tabs
  - Quick search activation
  - Instant settings access
  - Game launch shortcuts
  - Fullscreen toggle
  - Quick exit commands
  
- **Screenshot capture** - Preserve your gaming moments
  - Capture current game view
  - Saves to Pictures folder
  - Automatic filename with timestamp
  - Notification on successful capture
  - Works in both windowed and fullscreen mode
  
- **Export statistics** - Data portability
  - Export all stats to CSV format
  - Import into Excel or other tools
  - Includes all tracked metrics
  - Timestamped export files
  - Easy data analysis

### 🔧 Technical Features

- **Modular architecture** - Professional code organization
  - Clear separation of concerns
  - Models for data representation
  - Core modules for business logic
  - GUI components separated from logic
  - Utilities for common functions
  - Easy to maintain and extend
  
- **Offline support** - Play anywhere, anytime
  - Download games for offline play
  - Local cache management
  - Automatic cache updates
  - Smart fallback to online when needed
  - Cache size tracking
  
- **Auto-update notifications** - Always stay current
  - Checks for updates on launch
  - GitHub release integration
  - Optional update checking
  - Version comparison
  - Direct download links
  
- **Performance mode** - Optimized gaming experience
  - Reduced animations for better performance
  - Lower resource usage
  - Faster game loading
  - Improved battery life on laptops
  - Toggle on/off in settings
  
- **Auto-save** - Never lose your progress
  - Automatic saving every 5 minutes
  - Saves on window close
  - Crash recovery
  - Backup system
  - Data integrity checks

### 🔒 Privacy & Security

- **Local data storage** - Your data stays on your device
  - No cloud storage required
  - No telemetry or tracking
  - No ads or analytics
  - Open source for transparency
  
- **No account required** - Instant play
  - No registration needed
  - No email collection
  - No personal information stored
  - Just download and play

---

## 📸 Screenshots

*Screenshots showcase the main interface, game browser, fullscreen mode, statistics, achievements, and theme variations.*

> **Note**: Add screenshots here by placing images in a `screenshots/` folder and linking them.

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 7/8/10/11, macOS 10.13+, or Linux (Ubuntu 18.04+, Fedora 30+)
- **Processor**: 1.6 GHz dual-core processor
- **Memory**: 2 GB RAM
- **Storage**: 500 MB available space (plus cache for downloaded games)
- **Graphics**: Any GPU with OpenGL 2.0 support
- **Network**: Internet connection for online play and downloads
- **Display**: 1024x768 minimum resolution

### Recommended Requirements
- **OS**: Windows 10/11, macOS 11+, or Linux (latest LTS)
- **Processor**: 2.0 GHz quad-core processor
- **Memory**: 4 GB RAM
- **Storage**: 2 GB available space
- **Graphics**: Dedicated GPU recommended for smoother animations
- **Network**: Broadband internet connection
- **Display**: 1920x1080 or higher resolution

### Software Dependencies
- **Python**: 3.8 or higher (3.9+ recommended)
- **pip**: Latest version
- **PyQt6**: Automatically installed with requirements
- **QtWebEngine**: Automatically installed with PyQt6
- **Internet connection**: Required for initial setup and online play

---

## 🚀 Installation

### Quick Start (Recommended)

#### Windows

1. **Download Python** (if not installed)
   - Visit [python.org](https://www.python.org/downloads/)
   - Download Python 3.9 or higher
   - Run installer and check "Add Python to PATH"

2. **Download the Launcher**
   ```cmd
   git clone https://github.com/sugarypumpkin822/website-games-launcher.git
   cd website-games-launcher
   ```

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```cmd
   python main.py
   ```

#### macOS

1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python@3.9
   ```

3. **Download the Launcher**
   ```bash
   git clone https://github.com/sugarypumpkin822/website-games-launcher.git
   cd website-games-launcher
   ```

4. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python3 main.py
   ```

#### Linux (Ubuntu/Debian)

1. **Install Python and pip**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

2. **Download the Launcher**
   ```bash
   git clone https://github.com/sugarypumpkin822/website-games-launcher.git
   cd website-games-launcher
   ```

3. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python3 main.py
   ```

#### Linux (Fedora/RHEL)

1. **Install Python and pip**
   ```bash
   sudo dnf install python3 python3-pip git
   ```

2. **Follow steps 2-4 from Ubuntu/Debian instructions**

### Alternative Installation Methods

#### Using Virtual Environment (Recommended for Development)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run application**
   ```bash
   python main.py
   ```

#### Direct Download (No Git Required)

1. Download ZIP from GitHub: [Download Link](https://github.com/sugarypumpkin822/website-games-launcher/archive/refs/heads/main.zip)
2. Extract the ZIP file
3. Open terminal/command prompt in extracted folder
4. Follow installation steps 3-4 from Quick Start

### Post-Installation

On first launch, you'll be prompted to:
1. Set your username
2. Choose your preferred theme
3. Configure auto-save settings
4. Enable/disable update checking

All settings can be changed later in the Settings menu.

---

## 📖 Usage

### Getting Started

#### First Launch

When you launch the application for the first time:

1. **Welcome Dialog**: You'll see a welcome screen
   - Enter your preferred username
   - This will be displayed throughout the app
   - Can be changed later in settings

2. **Theme Selection**: Choose your initial theme
   - Preview available themes
   - Select one that suits your preference
   - Can be changed anytime

3. **Main Interface**: Explore the launcher
   - **Games Tab**: Browse and play all available games
   - **Statistics Tab**: View your gaming stats
   - **Achievements Tab**: Track your progress
   - **Challenges Tab**: Check daily challenges
   - **Settings Tab**: Customize your experience

### Playing Games

#### Method 1: Embedded Browser (Online)

1. **Select a Game**
   - Browse the games list
   - Click on any game card to select it
   - View game details in the info panel

2. **Launch Game**
   - Click the "▶️ Play" button
   - Game loads in embedded browser
   - Starts tracking play time automatically

3. **Playing**
   - Game loads from Poki.com
   - Full game functionality
   - Statistics tracked in background

#### Method 2: Fullscreen Mode

1. **Enter Fullscreen**
   - Click "⛶ Fullscreen" button
   - Or press `F11` keyboard shortcut
   - Game opens in dedicated fullscreen window

2. **Fullscreen Controls**
   - Move mouse to top of screen to reveal exit button
   - Click "× Exit Fullscreen" to return
   - Or press `Escape` key
   - Or press `F11` again

3. **Benefits**
   - Immersive gaming experience
   - No distractions
   - Better focus
   - Larger play area

#### Method 3: Offline Play (Downloaded Games)

1. **Download a Game**
   - Select game from list
   - Click "⬇️ Download" button
   - Wait for download to complete
   - Green checkmark indicates download success

2. **Play Offline**
   - Downloaded games automatically use local files
   - No internet required after download
   - Same features as online play
   - Statistics still tracked

3. **Managing Downloads**
   - View cache size in settings
   - Clear cache if needed
   - Re-download if files corrupted
   - Updates checked automatically

### Advanced Features

#### Game Organization

**Favorites**
- Click the star icon on any game card
- Mark frequently played games
- Filter games list to show only favorites
- Quick access to your preferred games

**Ratings**
- Rate games from 1-5 stars
- Personal ratings for your reference
- Sort games by rating
- Helps with game selection

**Notes**
- Add custom notes to any game
- Reminders, strategies, or tips
- Accessed from game info panel
- Saved automatically

#### Statistics Tracking

The launcher tracks comprehensive statistics:

**Per-Game Stats**
- Total play time (hours, minutes, seconds)
- Number of times played
- Last played date and time
- First played date
- Average session length
- Current streak (consecutive days)

**Global Stats**
- Total play time across all games
- Total number of games played
- Unique games played
- Longest streak
- Most played game
- Total achievements unlocked
- Current level and XP

**Exporting Stats**
1. Go to Statistics tab
2. Click "Export Statistics" button
3. Choose save location
4. Opens as CSV file
5. Import to Excel/Sheets for analysis

#### Achievements System

**How Achievements Work**
- Unlock by completing specific tasks
- Each achievement has XP reward
- Progress tracked automatically
- Notifications on unlock
- View all achievements in Achievements tab

**Achievement Categories**
- **Milestone Achievements**: Based on total playtime or count
- **Streak Achievements**: Based on daily play consistency
- **Variety Achievements**: Based on playing different games
- **Time-based Achievements**: Based on playing at specific times
- **Ultimate Achievement**: Unlock all other achievements

**Viewing Progress**
- Check Achievements tab
- See locked and unlocked achievements
- Progress bars for multi-step achievements
- XP rewards displayed
- Total achievement completion percentage

#### Daily Challenges

**Challenge System**
- New challenge generated daily at midnight
- Three challenge types:
  1. **Play Specific Game**: Play a random game
  2. **Play Time Goal**: Play for X minutes total
  3. **Streak Challenge**: Maintain daily streak

**Completing Challenges**
- Challenges tracked automatically
- Completion grants bonus XP
- View challenge history
- Streak of completed challenges tracked

**Challenge Tips**
- Check challenges each day
- Plan gameplay to complete challenges
- Combine with achievement goals
- Don't miss days for streak challenges

#### Game Recommendations

**How Recommendations Work**
- Analyzes your play history
- Considers favorite games
- Looks at recently played games
- Suggests games you haven't tried
- Updates based on new plays

**Using Recommendations**
- View in Games tab
- Recommendations displayed at top
- Click game to view details
- Refresh button for new suggestions
- Personalized to your preferences

#### Leveling System

**Gaining XP**
- Play games: +1 XP per minute
- Complete achievements: Varies by achievement
- Complete daily challenges: Bonus XP
- First time playing a game: Bonus XP

**Leveling Up**
- XP accumulates over time
- Level increases at thresholds
- Current level displayed in main window
- Progress bar shows next level progress
- No level cap

**Level Benefits**
- Track your dedication
- Milestone achievements at certain levels
- Personal satisfaction
- Bragging rights

---

## 🎮 Games Included

The launcher includes all 14 Papa Louie games from Poki:

### Restaurant Management Games

1. **Papa's Wingeria** 🍗
   - Run a chicken wing restaurant
   - Take orders, fry wings, add sauces
   - Serve satisfied customers

2. **Papa's Freezeria** 🍦
   - Manage an ice cream shop
   - Mix flavors, add toppings
   - Create perfect sundaes

3. **Papa's Sushiria** 🍣
   - Operate a sushi restaurant
   - Prepare sushi, bubble tea
   - Master Japanese cuisine

4. **Papa's Pastaria** 🍝
   - Run an Italian pasta restaurant
   - Cook pasta, add sauces
   - Perfect pasta dishes

5. **Papa's Pancakeria** 🥞
   - Breakfast restaurant management
   - Cook pancakes, add toppings
   - Serve breakfast combos

6. **Papa's Donuteria** 🍩
   - Donut shop operations
   - Fry donuts, add frosting
   - Create custom donuts

7. **Papa's Bakeria** 🥖
   - Bakery management
   - Bake pies, add crusts
   - Perfect pie recipes

8. **Papa's Taco Mia** 🌮
   - Taco restaurant
   - Grill meats, add toppings
   - Authentic tacos

9. **Papa's Cupcakeria** 🧁
   - Cupcake bakery
   - Bake cupcakes, add frosting
   - Decorative cupcakes

10. **Papa's Hotdoggeria** 🌭
    - Hot dog stand
    - Grill hot dogs, add condiments
    - Classic American food

11. **Papa's Burgeria** 🍔
    - Burger restaurant
    - Grill burgers, build orders
    - Perfect burger assembly

12. **Papa's Pizzeria** 🍕
    - Pizza shop
    - Top pizzas, bake to perfection
    - Classic pizza making

13. **Papa's Cheeseria** 🧀
    - Grilled cheese sandwich shop
    - Grill sandwiches, add fillings
    - Gourmet grilled cheese

### Adventure Game

14. **Papa Louie: When Pizzas Attack** 🏃
    - Platform adventure game
    - Rescue customers from mutant food
    - Action-packed gameplay

### Game Features

All games include:
- Order taking system
- Cooking/preparation stations
- Topping/customization
- Customer satisfaction ratings
- Day progression
- Increasing difficulty
- Mini-games
- Customer unlocks
- Ranking system

---

## ⚙️ Configuration

### Settings Location

All configuration files are stored in your user directory:

**Windows**: `C:\Users\YourUsername\.papas_launcher\`
**macOS**: `/Users/YourUsername/.papas_launcher/`
**Linux**: `/home/yourusername/.papas_launcher/`

### Configuration Files

#### settings.json

Main settings file containing:

```json
{
  "username": "Player",
  "theme": "dark",
  "auto_save": true,
  "auto_save_interval": 5,
  "check_updates": true,
  "notifications_enabled": true,
  "download_enabled": true,
  "performance_mode": false,
  "minimize_to_tray": true,
  "close_to_tray": false,
  "window_size": [1200, 800],
  "window_position": [100, 100]
}
```

**Setting Descriptions:**
- `username`: Display name
- `theme`: Active theme name
- `auto_save`: Enable automatic saving
- `auto_save_interval`: Minutes between auto-saves
- `check_updates`: Check for updates on launch
- `notifications_enabled`: Show notifications
- `download_enabled`: Allow game downloads
- `performance_mode`: Reduce animations
- `minimize_to_tray`: Minimize to system tray
- `close_to_tray`: Close button minimizes instead
- `window_size`: Window dimensions [width, height]
- `window_position`: Window position [x, y]

#### game_data.json

Game statistics and user data:

```json
{
  "games": {
    "papas_pizzeria": {
      "play_time": 7200,
      "play_count": 15,
      "last_played": "2024-12-27T15:30:00",
      "first_played": "2024-12-01T10:00:00",
      "rating": 5,
      "is_favorite": true,
      "notes": "Best game ever!",
      "current_streak": 7,
      "downloaded": true
    }
  },
  "user": {
    "level": 12,
    "xp": 4500,
    "total_play_time": 86400,
    "achievements_unlocked": ["first_timer", "marathon_player"],
    "challenges_completed": 25,
    "daily_challenge": {
      "date": "2024-12-27",
      "type": "play_time",
      "target": 30,
      "progress": 15,
      "completed": false
    }
  }
}
```

### Cache Directory

Downloaded games stored in: `~/.papas_launcher/cache/`

Structure:
```
cache/
├── papas_pizzeria/
│   ├── index.html
│   ├── styles/
│   │   └── game.css
│   └── scripts/
│       └── game.js
├── papas_burgeria/
│   └── ...
└── cache_manifest.json
```

### Modifying Settings

#### Through GUI
1. Open Settings tab
2. Modify desired settings
3. Changes save automatically
4. Restart app if prompted

#### Manual Editing
1. Close the application
2. Navigate to `~/.papas_launcher/`
3. Edit `settings.json` with text editor
4. Save and restart application
5. Ensure JSON syntax is valid

### Backup and Restore

**Creating Backup:**
1. Close application
2. Copy entire `.papas_launcher` folder
3. Store in safe location

**Restoring Backup:**
1. Close application
2. Replace `.papas_launcher` folder with backup
3. Restart application

### Reset to Defaults

**Reset Settings:**
- Delete `settings.json`
- Restart application
- Reconfigure preferences

**Reset All Data:**
- Delete entire `.papas_launcher` folder
- Restart application
- Fresh start with defaults

---

## ⌨️ Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search box |
| `Ctrl+H` | Return to home/games tab |
| `Ctrl+S` | Open settings |
| `Ctrl+Q` | Quit application |
| `Ctrl+R` | Refresh current view |
| `Ctrl+T` | Toggle theme menu |
| `Ctrl+1-5` | Switch to tab 1-5 |
| `F1` | Open help/about |
| `F5` | Refresh game list |
| `F11` | Toggle fullscreen |

### Game Controls

| Shortcut | Action |
|----------|--------|
| `Enter` | Play selected game |
| `Space` | Play/pause (when applicable) |
| `F11` | Enter/exit fullscreen |
| `Escape` | Exit fullscreen |
| `Ctrl+P` | Screenshot |
| `Ctrl+D` | Download game |
| `Ctrl+I` | View game info |

### Navigation

| Shortcut | Action |
|----------|--------|
| `Arrow Up/Down` | Navigate game list |
| `Home` | Jump to first game |
| `End` | Jump to last game |
| `Page Up/Down` | Scroll page |
| `Tab` | Navigate between elements |
| `Shift+Tab` | Navigate backwards |

### Productivity

| Shortcut | Action |
|----------|--------|
| `Ctrl+E` | Export statistics |
| `Ctrl+N` | Add note to game |
| `Ctrl+*` | Toggle favorite |
| `Ctrl+/` | Toggle search |

---

## 🔍 Features Deep Dive

### Theme System

The launcher features a sophisticated theme engine:

**Available Themes:**

1. **Light Theme**
   - Background: White (#FFFFFF)
   - Text: Dark Gray (#333333)
   - Accent: Blue (#2196F3)
   - Best for: Daytime use, bright environments

2. **Dark Theme**
   - Background: Dark Gray (#1E1E1E)
   - Text: White (#FFFFFF)
   - Accent: Teal (#00BCD4)
   - Best for: Night gaming, reducing eye strain

3. **Ocean Theme**
   - Background: Deep Blue (#1A237E)
   - Text: White (#FFFFFF)
   - Accent: Light Blue (#03A9F4)
   - Best for: Calming atmosphere, water lovers

4. **Forest Theme**
   - Background: Dark Green (#1B5E20)
   - Text: White (#FFFFFF)
   - Accent: Light Green (#8BC34A)
   - Best for: Nature enthusiasts, relaxing vibe

5. **Sunset Theme**
   - Background: Deep Orange (#BF360C)
   - Text: White (#FFFFFF)
   - Accent: Amber (#FFC107)
   - Best for: Warm atmosphere, evening gaming

6. **Purple Theme**
   - Background: Deep Purple (#4A148C)
   - Text: White (#FFFFFF)
   - Accent: Pink (#E91E63)
   - Best for: Unique look, purple fans

**Theme Features:**
- Instant switching
- Persistent across sessions
- Affects all UI elements
- Custom color schemes
- Smooth transitions

### Download Manager

The download manager enables offline play:

**Download Process:**
1. Fetches HTML, CSS, and JavaScript files
2. Stores in local cache directory
3. Creates manifest for tracking
4. Validates file integrity
5. Updates game status

**Cache Management:**
- View total cache size
- Clear individual games
- Clear all cache
- Re-download corrupted files
- Automatic cache updates

**Offline Play:**
- Automatic detection of local files
- Seamless fallback to cached versions
- No internet required after download
- Full game functionality maintained
- Statistics still tracked

### Achievement System

Detailed achievement mechanics:

**Achievement Structure:**
```python
{
    "id": "achievement_id",
    "name": "Achievement Name",
    "description": "What you need to do",
    "xp_reward": 100,
    "unlocked": False,
    "unlock_date": None,
    "progress": 0,
    "max_progress": 1
}
```

**Achievement Types:**

1. **Binary Achievements**: Unlock once
2. **Progressive Achievements**: Track progress
3. **Hidden Achievements**: Surprise unlocks
4. **Challenge Achievements**: Difficult tasks

**XP Rewards:**
- Easy: 50-100 XP
- Medium: 100-250 XP
- Hard: 250-500 XP
- Ultimate: 1000+ XP

### Statistics Engine

Comprehensive stat tracking:

**Real-time Tracking:**
- Play time per second
- Session tracking
- Streak calculations
- Daily aggregation

**Statistical Analysis:**
- Average session length
- Peak play times
- Game preferences
- Play patterns

**Data Visualization:**
- Charts and graphs
- Trend analysis
- Comparison views
- Historical data

---

## 📁 Project Structure

```
website-games-launcher/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # AGPL-3.0 License
│
├── models/                # Data models
│   ├── __init__.py
│   ├── game_item.py      # Game data structure
│   ├── achievement.py    # Achievement model
│   └── daily_challenge.py # Challenge model
│
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── game_manager.py   # Game CRUD operations
│   ├── settings_manager.py # Settings persistence
│   ├── achievement_manager.py # Achievement logic
│   └── download_manager.py # Download handling
│
├── gui/                  # GUI components
│   ├── __init__.py
│   ├── main_window.py    # Main application window
│   ├── tabs/            # Tab components
│   │   ├── __init__.py
│   │   └── games_tab.py  # Games browser tab
│   └── widgets/         # Custom widgets
│       ├── __init__.py
│       └── fullscreen_game_window.py # Fullscreen view
│
└── utils/                # Utilities
    ├── __init__.py
    ├── update_checker.py # Version checking
    └── daily_challenge_generator.py # Challenge RNG
```

### Module Descriptions

**main.py**
- Application entry point
- Initializes Qt application
- Creates main window
- Handles command-line arguments

**models/**
- Data structures and models
- Game representation
- Achievement schema
- Challenge definitions

**core/**
- Business logic
- Data management
- File I/O operations
- Core algorithms

**gui/**
- User interface components
- PyQt6 widgets and windows
- Event handling
- Visual presentation

**utils/**
- Helper functions
- Common utilities
- External integrations
- Miscellaneous tools

---

## 🛠️ Development

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/website-games-launcher.git
   cd website-games-launcher
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install development tools**
   ```bash
   pip install black flake8 pytest pylint mypy
   ```

### Code Style

This project follows PEP 8 with some modifications:

**Formatting:**
- Line length: 100 characters
- Indentation: 4 spaces
- String quotes: Double quotes preferred
- Imports: Grouped and sorted

**Use Black for formatting:**
```bash
black --line-length 100 .
```

**Linting:**
```bash
flake8 --max-line-length 100 .
pylint **/*.py
```

**Type Checking:**
```bash
mypy --strict .
```

### Adding New Features

#### Adding a New Game

1. Open `core/game_manager.py`
2. Add to `_initialize_games()` method:

```python
self.games["game_id"] = GameItem(
    game_id="game_id",
    name="Game Name",
    url="https://poki.com/en/g/game-url",
    icon_url="https://img.poki.com/game-icon.png",
    description="Game description"
)
```

3. Test the new game

#### Adding a New Achievement

1. Open `core/achievement_manager.py`
2. Add to `_initialize_achievements()` method:

```python
self.achievements["achievement_id"] = Achievement(
    achievement_id="achievement_id",
    name="Achievement Name",
    description="How to unlock",
    xp_reward=100,
    icon="🏆"
)
```

3. Implement unlock logic in appropriate method
4. Test achievement unlocking

#### Adding a New Theme

1. Open `gui/main_window.py`
2. Add to `available_themes` dictionary:

```python
"theme_name": {
    "background": "#HEXCOLOR",
    "foreground": "#HEXCOLOR",
    "accent": "#HEXCOLOR",
    "card": "#HEXCOLOR",
    "hover": "#HEXCOLOR"
}
```

3. Update `apply_theme()` method if needed
4. Test theme switching

#### Adding a New Tab

1. Create new file in `gui/tabs/`
2. Inherit from `QWidget`
3. Implement UI and logic
4. Add to `main_window.py`:

```python
self.new_tab = NewTab()
self.tabs.addTab(self.new_tab, "Tab Name")
```

### Testing

**Manual Testing:**
1. Test all features manually
2. Check different scenarios
3. Verify data persistence
4. Test error handling

**Unit Tests (TODO):**
```bash
pytest tests/
```

### Building Distribution

#### Windows (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PapasLauncher" main.py
```

#### macOS (py2app)

```bash
pip install py2app
python setup.py py2app
```

#### Linux (AppImage)

```bash
pip install appimage-builder
appimage-builder --recipe AppImageBuilder.yml
```

### Debugging

**Enable debug mode:**
```bash
python main.py --debug
```

**Common issues:**
- QtWebEngine not loading: Check PyQt6-WebEngine installation
- Games not loading: Check internet connection
- Settings not saving: Check file permissions
- Cache issues: Clear cache directory

---

## 🔧 Troubleshooting

### Installation Issues

**Problem: pip install fails**
```
Solution:
1. Update pip: python -m pip install --upgrade pip
2. Install individually: pip install PyQt6 PyQt6-WebEngine requests
3. Check Python version: python --version (must be 3.8+)
```

**Problem: PyQt6 not found**
```
Solution:
1. Verify installation: pip show PyQt6
2. Reinstall: pip uninstall PyQt6 && pip install PyQt6
3. Check virtual environment activation
```

**Problem: Permission denied**
```
Solution:
1. Windows: Run as administrator
2. macOS/Linux: Use --user flag: pip install --user -r requirements.txt
3. Check directory permissions
```

### Runtime Issues

**Problem: Games not loading**
```
Solution:
1. Check internet connection
2. Clear browser cache in settings
3. Try different game
4. Check firewall settings
5. Update PyQt6-WebEngine
```

**Problem: Fullscreen not working**
```
Solution:
1. Update graphics drivers
2. Try windowed mode first
3. Check display settings
4. Disable hardware acceleration
```

**Problem: Application crashes on startup**
```
Solution:
1. Delete .papas_launcher folder
2. Reinstall dependencies
3. Check Python version
4. Run with --debug flag
5. Check error logs
```

**Problem: Settings not saving**
```
Solution:
1. Check .papas_launcher folder permissions
2. Verify disk space
3. Check file system errors
4. Run as administrator (Windows)
```

**Problem: High CPU/Memory usage**
```
Solution:
1. Enable performance mode in settings
2. Close unnecessary games
3. Clear cache
4. Reduce window size
5. Update application
```

### Game-Specific Issues

**Problem: Game controls not responsive**
```
Solution:
1. Click inside game window
2. Refresh game (F5)
3. Try fullscreen mode
4. Clear browser cache
```

**Problem: Game audio not working**
```
Solution:
1. Check system volume
2. Check browser permissions
3. Restart application
4. Update audio drivers
```

**Problem: Downloaded games not working offline**
```
Solution:
1. Re-download game
2. Check cache integrity
3. Verify complete download
4. Check file permissions
```

### Platform-Specific Issues

**Windows:**
- Antivirus blocking: Add exception for launcher
- SmartScreen warning: Click "More info" → "Run anyway"
- DLL errors: Install Visual C++ Redistributable

**macOS:**
- "Unverified developer": Right-click → Open
- Gatekeeper blocking: System Preferences → Security & Privacy → Allow
- Python certificate issues: Run Python's Install Certificates.command

**Linux:**
- Missing libraries: Install libxcb-xinerama0
- Display issues: Check X11/Wayland compatibility
- Font rendering: Install required fonts

### Getting Help

If none of these solutions work:

1. Check GitHub Issues for similar problems
2. Create new issue with details:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce
3. Join community discussions
4. Contact developer

---

## ❓ FAQ

### General Questions

**Q: Is this launcher free?**
A: Yes, completely free and open source under AGPL-3.0 license.

**Q: Do I need an account?**
A: No account required. Just download and play.

**Q: Is my data private?**
A: Yes, all data stored locally on your device. No cloud storage or telemetry.

**Q: Can I play offline?**
A: Yes, after downloading games using the download feature.

**Q: Which platforms are supported?**
A: Windows, macOS, and Linux (all major distributions).

**Q: Are the games official?**
A: Games are from Poki.com, which hosts official Papa's games by Flipline Studios.

### Technical Questions

**Q: What is the file size?**
A: Launcher: ~50MB. Each game: 10-50MB. Total depends on downloads.

**Q: Does it support multiple users?**
A: Not currently. Each OS user has separate profile.

**Q: Can I backup my progress?**
A: Yes, backup the `.papas_launcher` folder.

**Q: How often is it updated?**
A: Updates released as needed. Check GitHub for latest version.

**Q: Can I contribute?**
A: Yes! Contributions welcome. See Contributing section.

**Q: Is there a mobile version?**
A: Not currently. Desktop only (Windows/Mac/Linux).

### Feature Questions

**Q: How do achievements work?**
A: Complete specific tasks to unlock achievements and earn XP.

**Q: What are daily challenges?**
A: Random challenges generated daily for bonus XP.

**Q: Can I add custom games?**
A: Not currently, but planned for future update.

**Q: How is XP calculated?**
A: 1 XP per minute of play, plus bonuses for achievements and challenges.

**Q: What's the level cap?**
A: No level cap. Level up infinitely.

**Q: Can I reset my stats?**
A: Yes, delete game_data.json or use reset option in settings.

### Troubleshooting Questions

**Q: Why won't a game load?**
A: Check internet connection. Try clearing cache. Restart launcher.

**Q: How do I fix crashes?**
A: Update Python and dependencies. Delete .papas_launcher folder. Reinstall.

**Q: Why is performance slow?**
A: Enable performance mode. Close other applications. Update graphics drivers.

**Q: Games work online but not offline?**
A: Re-download games. Check cache integrity. Verify complete downloads.

**Q: How do I report bugs?**
A: Open issue on GitHub with details and reproduction steps.

---

## 📝 Changelog

### Version 1.0.0 (Current)

**Initial Release**
- 14 Papa's games support
- Embedded browser play
- Fullscreen mode
- Local game downloads
- Statistics tracking
- Achievement system (11 achievements)
- Daily challenges
- 6 themes
- Game recommendations
- User leveling system
- Favorites and ratings
- System tray integration
- Keyboard shortcuts
- Screenshot capture
- Export statistics
- Auto-save
- Update checker

### Planned Features (Future Versions)

**Version 1.1.0** (Planned)
- More achievements
- Leaderboards
- Game time limits
- Parent controls
- Custom themes
- Plugin system

**Version 1.2.0** (Planned)
- Multiplayer stats sharing
- Cloud sync option
- Mobile companion app
- More games support
- Achievement guides

**Version 2.0.0** (Future)
- Complete UI redesign
- AI recommendations
- Social features
- Game mods support
- Custom game integration

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

### What this means:

✅ **You can:**
- Use the software for any purpose
- Study how the program works
- Modify the source code
- Distribute copies
- Distribute modified versions

❗ **You must:**
- Disclose source code of modifications
- State significant changes
- Include original license
- Use same license for derivatives
- Provide access to source for network use

See the [LICENSE](LICENSE) file for full legal text.

### Why AGPL-3.0?

This strong copyleft license ensures:
- Software remains free and open source
- Improvements benefit everyone
- Network services share their source
- Community-driven development
- Transparent modifications

---

## 🙏 Credits

### Games
- **Created by**: Flipline Studios
- **Hosted on**: Poki.com
- **Licensed to**: Freely accessible web games

### Development
- **Developer**: sugarypumpkin822
- **Repository**: [GitHub](https://github.com/sugarypumpkin822/website-games-launcher)
- **License**: AGPL-3.0

### Technologies
- **Framework**: [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- **Web Engine**: [QtWebEngine](https://doc.qt.io/qt-6/qtwebengine-index.html) - Browser component
- **Language**: [Python 3](https://www.python.org/) - Programming language
- **Icons**: Game icons from Poki.com

### Special Thanks
- Flipline Studios for creating amazing games
- Poki.com for hosting the games
- PyQt6 team for excellent framework
- Python community
- All contributors and testers

### Community
- Contributors: See [Contributors](https://github.com/sugarypumpkin822/website-games-launcher/graphs/contributors)
- Bug reporters
- Feature requesters
- Documentation improvers

---

## 🤝 Contributing

Contributions make the open source community amazing! Any contributions are **greatly appreciated**.

### How to Contribute

1. **Fork the Project**
   - Click "Fork" button on GitHub
   - Clone your fork locally

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests if applicable

4. **Commit Changes**
   ```bash
   git add .
   git commit -m 'Add some AmazingFeature'
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Open Pull Request**
   - Go to original repository
   - Click "New Pull Request"
   - Describe your changes
   - Wait for review

### Contribution Guidelines

**Code Quality:**
- Follow PEP 8 style guide
- Write clear comments
- Use meaningful variable names
- Keep functions focused
- Add docstrings to functions

**Git Commit Messages:**
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues if applicable
- Keep commits atomic

**Pull Requests:**
- Clear title and description
- Reference related issues
- Include screenshots for UI changes
- Update documentation
- Test thoroughly

### Areas for Contribution

**Code:**
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test coverage

**Documentation:**
- README improvements
- Code comments
- User guides
- API documentation
- Translation

**Design:**
- UI/UX improvements
- New themes
- Icons and graphics
- Layout enhancements

**Testing:**
- Bug reporting
- Feature testing
- Compatibility testing
- User experience feedback

### Code of Conduct

**Be respectful:**
- Welcome newcomers
- Respect different opinions
- Give constructive feedback
- Assume good intentions

**Be collaborative:**
- Help others
- Share knowledge
- Participate in discussions
- Review code thoughtfully

**Be professional:**
- No harassment
- No discrimination
- No spam
- Follow project guidelines

---

## 🐛 Reporting Issues

Found a bug? Have a suggestion? Let us know!

### Before Reporting

1. **Check existing issues** - Might already be reported
2. **Try latest version** - Might be fixed already
3. **Check documentation** - Might be known behavior
4. **Gather information** - Prepare details

### Creating Good Bug Reports

Include:

**Environment:**
- Operating System and version
- Python version
- Launcher version
- Installation method

**Description:**
- What you expected
- What actually happened
- Steps to reproduce
- Error messages
- Screenshots if applicable

**Example:**
```
**Environment:**
- OS: Windows 10 Home 64-bit
- Python: 3.9.7
- Launcher: v1.0.0
- Installed via: pip

**Bug:**
Application crashes when clicking "Download" button on Papa's Pizzeria.

**Steps to Reproduce:**
1. Launch application
2. Select Papa's Pizzeria
3. Click "Download" button
4. Application crashes

**Error Message:**
[Include error text or screenshot]

**Expected:**
Game should download successfully.

**Additional Context:**
Happens only with Papa's Pizzeria, other games work fine.
```

### Feature Requests

For feature requests, include:
- Clear description
- Use case
- Expected behavior
- Mockups if applicable
- Why it would be useful

---

## 💬 Support

Need help? Multiple ways to get support:

### Self-Help Resources

1. **Documentation**
   - Read this README thoroughly
   - Check FAQ section
   - Review Troubleshooting guide

2. **Search Issues**
   - Browse [existing issues](https://github.com/sugarypumpkin822/website-games-launcher/issues)
   - Check closed issues
   - Use GitHub search

### Community Support

1. **GitHub Discussions**
   - Ask questions
   - Share tips
   - Connect with users
   - Get community help

2. **GitHub Issues**
   - Report bugs
   - Request features
   - Technical problems
   - Development questions

### Contact Developer

For direct support:
- **GitHub**: [@sugarypumpkin822](https://github.com/sugarypumpkin822)
- **Email**: Available on GitHub profile
- **Issues**: [Create new issue](https://github.com/sugarypumpkin822/website-games-launcher/issues/new)

### Response Times

- **Bugs**: 1-3 days
- **Features**: 1-7 days
- **Questions**: 1-5 days
- **Pull Requests**: 1-7 days

*Note: Times are estimates. Response may vary.*

---

## ⭐ Star History

If you find this project useful, please consider:

- ⭐ **Star the repository** on GitHub
- 🔄 **Share with friends** who love Papa's games
- 🐛 **Report bugs** to improve the launcher
- 💡 **Suggest features** for future updates
- 🤝 **Contribute code** to make it better

### Show Your Support

```bash
# Star on GitHub
# Visit: https://github.com/sugarypumpkin822/website-games-launcher

# Share on social media
# Tweet about it
# Post in gaming communities
# Tell your friends
```

---

## 🎉 Acknowledgments

This project exists thanks to:

- **Flipline Studios** - For creating Papa's games
- **Poki.com** - For hosting the games
- **PyQt6** - For the amazing GUI framework
- **Python** - For the fantastic programming language
- **Contributors** - For improvements and bug fixes
- **Users** - For feedback and support
- **You** - For using Papa's Games Launcher!

---

## 📞 Contact & Links

**Project Links:**
- 🏠 [Homepage](https://github.com/sugarypumpkin822/website-games-launcher)
- 📦 [Releases](https://github.com/sugarypumpkin822/website-games-launcher/releases)
- 🐛 [Issues](https://github.com/sugarypumpkin822/website-games-launcher/issues)
- 💬 [Discussions](https://github.com/sugarypumpkin822/website-games-launcher/discussions)

**Developer:**
- GitHub: [@sugarypumpkin822](https://github.com/sugarypumpkin822)
- Email: Available on GitHub profile

**Games:**
- [Flipline Studios](http://www.flipline.com/)
- [Poki.com](https://poki.com/)

---

<div align="center">

### 🎮 Enjoy Gaming! 🎮

**Made with ❤️ by [sugarypumpkin822](https://github.com/sugarypumpkin822)**

*Last Updated: December 27, 2025*

---

[![GitHub stars](https://img.shields.io/github/stars/sugarypumpkin822/website-games-launcher?style=social)](https://github.com/sugarypumpkin822/website-games-launcher/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sugarypumpkin822/website-games-launcher?style=social)](https://github.com/sugarypumpkin822/website-games-launcher/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/sugarypumpkin822/website-games-launcher?style=social)](https://github.com/sugarypumpkin822/website-games-launcher/watchers)

</div>
