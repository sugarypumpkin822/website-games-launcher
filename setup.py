"""
Setup script for building Website Games Launcher executable
Uses PyInstaller to create a standalone .exe file without console window
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the main script
    main_script = os.path.join(script_dir, 'main.py')
    
    # PyInstaller arguments
    pyinstaller_args = [
        main_script,
        '--name=WebsiteGamesLauncher',  # Name of the executable
        '--onefile',                     # Create a single executable file
        '--windowed',                    # No console window (same as --noconsole)
        '--clean',                       # Clean PyInstaller cache before building
        
        # Add all package directories
        '--add-data=core;core',
        '--add-data=gui;gui',
        '--add-data=models;models',
        '--add-data=utils;utils',
        
        # Add README and LICENSE if you want them included
        '--add-data=README.md;.',
        '--add-data=LICENSE;.',
        
        # Hidden imports that might not be detected automatically
        '--hidden-import=core',
        '--hidden-import=core.achievement_manager',
        '--hidden-import=core.download_manager',
        '--hidden-import=core.game_manager',
        '--hidden-import=core.settings_manager',
        '--hidden-import=gui',
        '--hidden-import=gui.main_window',
        '--hidden-import=gui.tabs',
        '--hidden-import=gui.tabs.games_tab',
        '--hidden-import=gui.widgets',
        '--hidden-import=gui.widgets.fullscreen_game_window',
        '--hidden-import=models',
        '--hidden-import=models.achievement',
        '--hidden-import=models.daily_challenge',
        '--hidden-import=models.game_item',
        '--hidden-import=utils',
        '--hidden-import=utils.daily_challenge_generator',
        '--hidden-import=utils.update_checker',
        
        # Common PyQt/PySide hidden imports (uncomment based on your GUI framework)
        # For PyQt5:
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.QtWebEngineWidgets',
        
        # For PyQt6:
        # '--hidden-import=PyQt6',
        # '--hidden-import=PyQt6.QtCore',
        # '--hidden-import=PyQt6.QtGui',
        # '--hidden-import=PyQt6.QtWidgets',
        # '--hidden-import=PyQt6.QtWebEngineWidgets',
        
        # For PySide6:
        # '--hidden-import=PySide6',
        # '--hidden-import=PySide6.QtCore',
        # '--hidden-import=PySide6.QtGui',
        # '--hidden-import=PySide6.QtWidgets',
        # '--hidden-import=PySide6.QtWebEngineWidgets',
        
        # Optimize
        '--optimize=2',
        
        # Add icon (uncomment and modify if you have an icon file)
        # '--icon=icon.ico',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=PIL',
        
        # Output directory
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ]
    
    print("Building executable...")
    print("This may take a few minutes...")
    
    # Run PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n" + "="*60)
    print("Build complete!")
    print(f"Executable location: {os.path.join(script_dir, 'dist', 'WebsiteGamesLauncher.exe')}")
    print("="*60)


if __name__ == '__main__':
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller is not installed!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)
    
    build_exe()
