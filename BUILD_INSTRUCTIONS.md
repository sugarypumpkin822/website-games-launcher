# Building Website Games Launcher Executable

This guide explains how to compile your Python application into a standalone Windows executable (.exe) that runs without showing a command prompt window.

## Prerequisites

- Python 3.8 or higher installed
- All dependencies from `requirements.txt` installed

## Method 1: Using setup.py (Recommended)

### Quick Build

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Run the build script:**
```bash
python setup.py
```

3. **Find your executable:**
   - Location: `dist/WebsiteGamesLauncher.exe`
   - This is a standalone file that can be distributed

### Using the Batch File (Windows)

Simply double-click `build.bat` or run:
```bash
build.bat
```

This will automatically:
- Check for Python
- Install PyInstaller if needed
- Build the executable
- Show you where the .exe is located

## Method 2: Using the .spec File (Advanced)

The `.spec` file provides more control over the build process:

```bash
pyinstaller WebsiteGamesLauncher.spec
```

## Important Notes

### GUI Framework Detection

The setup.py includes imports for **PyQt5** by default. If you're using a different framework:

**For PyQt6:** Edit `setup.py` and uncomment these lines:
```python
'--hidden-import=PyQt6',
'--hidden-import=PyQt6.QtCore',
'--hidden-import=PyQt6.QtGui',
'--hidden-import=PyQt6.QtWidgets',
'--hidden-import=PyQt6.QtWebEngineWidgets',
```

**For PySide6:** Edit `setup.py` and uncomment these lines:
```python
'--hidden-import=PySide6',
'--hidden-import=PySide6.QtCore',
'--hidden-import=PySide6.QtGui',
'--hidden-import=PySide6.QtWidgets',
'--hidden-import=PySide6.QtWebEngineWidgets',
```

### Adding an Icon

To add a custom icon to your executable:

1. Create or obtain an `.ico` file (256x256 recommended)
2. Place it in your project root (e.g., `icon.ico`)
3. In `setup.py`, uncomment and modify this line:
```python
'--icon=icon.ico',
```

### Including Additional Files

If you have game data, images, or other assets:

1. Create a folder (e.g., `assets/`)
2. Add to `setup.py`:
```python
'--add-data=assets;assets',
```

### Data Files and Resources

The build includes all your Python packages automatically. If you need to access data files at runtime, use:

```python
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Usage
config_file = resource_path('config.json')
```

## Build Configurations

### One-File vs One-Folder

**One-File (Default):**
- Single .exe file
- Slower startup (extracts to temp folder)
- Easier distribution
- Current setting: `--onefile`

**One-Folder:**
- Faster startup
- Multiple files in a folder
- Larger distribution package
- Change to: `--onedir` in setup.py

### Reducing File Size

The executable may be large (50-150MB) due to bundled libraries. To reduce size:

1. **Use a virtual environment** with only required packages
2. **Exclude unused modules** (already configured in setup.py)
3. **Enable UPX compression** (already enabled)

## Troubleshooting

### "Module not found" errors

Add the missing module to hidden imports in `setup.py`:
```python
'--hidden-import=missing_module_name',
```

### The .exe won't run on other computers

Common causes:
- Missing Visual C++ Redistributables (user needs to install)
- Windows Defender blocking (sign your executable or add exception)
- Antivirus false positive (submit to vendor)

### The window closes immediately

1. Test in console mode first: Remove `--windowed` flag
2. Add error logging to your `main.py`
3. Check for missing dependencies

### Large file size

This is normal for Python applications. A typical build is 50-150MB due to:
- Python runtime
- GUI framework (PyQt/PySide)
- All dependencies

## Distribution

Your executable is completely standalone and can be distributed:

1. **Single .exe distribution:**
   - Send `dist/WebsiteGamesLauncher.exe`
   - Users can run it directly
   - No Python installation needed

2. **With installer:**
   - Use Inno Setup or NSIS to create an installer
   - Include Visual C++ Redistributables
   - Add Start Menu shortcuts

3. **Testing before distribution:**
   - Test on a clean Windows VM
   - Test with antivirus software enabled
   - Test on different Windows versions

## Clean Build

If you need to rebuild from scratch:

```bash
# Delete build artifacts
rmdir /s /q build dist
del WebsiteGamesLauncher.spec

# Rebuild
python setup.py
```

## Alternative Build Tools

If PyInstaller doesn't work well for your project:

- **cx_Freeze:** Good alternative, similar approach
- **Nuitka:** Compiles to C++, faster but more complex
- **py2exe:** Windows-only, older but reliable

## Support

For PyInstaller issues, check:
- Official docs: https://pyinstaller.org/
- GitHub issues: https://github.com/pyinstaller/pyinstaller/issues
- StackOverflow: Search "pyinstaller" + your error message
