# PyUNO

![PyUNO Logo](assets/uno_logo.png)

A Python implementation of the classic UNO card game built with Pygame.

## Project Structure

```
PyUNO/
├── src/                     # Source code
│   └── pyuno/              # Main package
│       ├── core/           # Core game logic
│       │   ├── __init__.py
│       │   └── uno_classes.py
│       ├── ui/             # User interface
│       │   ├── __init__.py
│       │   └── uno_ui.py
│       ├── config/         # Configuration files
│       │   ├── __init__.py
│       │   └── font_config.py
│       └── __init__.py
├── tests/                  # Test files
│   ├── test_uno_game.py
│   └── debug_test.py
├── docs/                   # Documentation
│   ├── README_TESTS.md
│   └── FONT_README.md
├── assets/                 # Game assets
│   ├── *.png              # Card images
│   ├── *.ttf, *.otf       # Font files
│   └── uno_logo.png       # Game logo
├── main_game.py           # Main entry point
└── LICENSE
```

## Installation & Usage

### Option 1: Run from Source
1. Make sure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main_game.py
   ```

### Option 2: Build Executable

#### Windows
1. Make sure you have Python 3.7+ installed
2. Double-click `build.bat` or run:
   ```cmd
   python build_executable.py
   ```
3. Find `PyUNO.exe` in the `dist` folder
4. Run `PyUNO.exe` directly or use `run_pyuno.bat`

#### macOS
1. Make sure you have Python 3.7+ installed
2. Open Terminal and run:
   ```bash
   ./build.sh
   ```
   Or manually:
   ```bash
   python3 build_executable.py
   ```
3. Find `PyUNO.app` in the `dist` folder
4. Double-click `PyUNO.app` or use `run_pyuno.command`

#### Linux
1. Make sure you have Python 3.7+ installed
2. Open Terminal and run:
   ```bash
   ./build.sh
   ```
   Or manually:
   ```bash
   python3 build_executable.py
   ```
3. Find `PyUNO` executable in the `dist` folder
4. Run `./PyUNO` directly or use `run_pyuno.sh`

### Alternative Build Methods
- Use the spec file: `pyinstaller pyuno.spec`
- Clean build: `python build_executable.py --clean`
- Rebuild: `python build_executable.py --rebuild`

### Platform-Specific Notes
- **macOS**: Supports both Intel and Apple Silicon Macs (Universal2 binary)
- **Windows**: Creates a single `.exe` file with all dependencies
- **Linux**: Creates a standalone executable compatible with most distributions

## Running Tests

To run the test suite:
```bash
python -m pytest tests/
```

To run debug tests:
```bash
python tests/debug_test.py
```

## Features

- Full UNO gameplay with 2-4 players
- AI opponents
- Beautiful UI with custom fonts and card graphics
- Special card effects (Draw Two, Skip, Reverse, Wild cards)
- UNO calling system with penalties
- Comprehensive test coverage

## Game Rules

This implementation follows standard UNO rules with support for:
- Number cards (0-9) in four colors
- Action cards (Skip, Reverse, Draw Two)
- Wild cards (Wild, Wild Draw Four)
- Proper card stacking mechanics
- UNO calling system

## Credits

Developed by Group 19 for the Basics in Python course at FH-SWF. 
