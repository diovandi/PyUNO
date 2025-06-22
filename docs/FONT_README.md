# Font System Documentation

## Overview

PyUNO uses custom fonts to create an enhanced visual experience. To ensure the game works on all systems, we've implemented a robust font fallback system that gracefully handles missing fonts.

## How It Works

### 1. Custom Fonts
The game includes custom fonts in the `fonts/` directory:
- **Baksosapi.otf** - Used for credits
- **Arcadeclassic.ttf** - Used for start button
- **Fishcrispy.otf** - Used for titles and status text
- **Chunq.ttf** - Used for buttons and UI elements

### 2. Fallback System
If custom fonts aren't available, the system automatically falls back to:
1. **Specific fallbacks** - Carefully chosen system fonts that match the style
2. **Common system fonts** - Arial, Helvetica, Calibri, etc.
3. **Default pygame font** - As a last resort

### 3. Configuration
Font settings are centrally managed in `font_config.py`, making it easy to:
- Change which fonts are used where
- Modify fallback preferences
- Add new font types

## For Developers

### Adding New Font Types
To add a new font type:

1. Add it to `FONT_CONFIG` in `font_config.py`:
```python
FONT_CONFIG = {
    # ... existing fonts ...
    'new_type': {
        'file': 'YourFont.ttf',
        'fallback': 'system_font_name'
    }
}
```

2. Use it in your code:
```python
my_font = load_font_by_type('new_type', size)
```

### Font Loading Functions
- `load_font_by_type(font_type, size)` - Recommended method using configuration
- `load_font_safe(font_path, size, fallback_font)` - Direct loading with fallback

## For Users

### If You're Missing Fonts
Don't worry! The game will automatically use system fonts if custom fonts aren't available. You'll see warning messages in the console, but the game will work perfectly.

### Installing Custom Fonts (Optional)
If you want the intended visual experience:
1. All custom fonts are included in the `fonts/` directory
2. No additional installation required - they load directly from the game files

## Testing

Run the font test script to verify everything works:
```bash
python test_fonts.py
```

This will test:
- ✅ Custom font loading
- ✅ Fallback font loading
- ✅ Text rendering

## Troubleshooting

### Common Issues

1. **"Font file not found" warnings**
   - **Cause**: Missing font files in `fonts/` directory
   - **Solution**: Ensure `fonts/` directory exists with all font files, or ignore (fallbacks will work)

2. **Text appears in different font than expected**
   - **Cause**: Custom font failed to load, using fallback
   - **Solution**: Check font file exists and is readable

3. **No text appears at all**
   - **Cause**: Severe font loading failure
   - **Solution**: Run `test_fonts.py` to diagnose the issue

### Advanced Configuration

You can modify font preferences in `font_config.py`:

```python
# Example: Change button font fallback
'button': {
    'file': 'Chunq.ttf',
    'fallback': 'impact'  # Change this to your preferred system font
}
```

## Benefits of This System

1. **Reliability** - Game works on all systems regardless of font availability
2. **Graceful degradation** - Fallbacks maintain good visual appearance
3. **Easy maintenance** - Centralized configuration
4. **User-friendly** - Clear warnings but no crashes
5. **Cross-platform** - Works on Windows, Mac, and Linux

## File Structure
```
fonts/                  # Custom font files
font_config.py         # Font configuration and mappings
uno_ui.py             # Font loading implementation
test_fonts.py         # Font system testing
FONT_README.md        # This documentation
``` 