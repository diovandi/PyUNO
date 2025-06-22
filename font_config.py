"""
Font configuration for PyUNO game
This file centralizes all font settings and provides fallback options
"""

# Font configuration with fallbacks
FONT_CONFIG = {
    'credit': {
        'file': 'Baksosapi.otf',
        'fallback': 'georgia'  # Elegant serif font for credits
    },
    'start_button': {
        'file': 'Arcadeclassic.ttf', 
        'fallback': 'impact'  # Bold font for buttons
    },
    'title': {
        'file': 'Fishcrispy.otf',
        'fallback': 'arial'  # Clean font for titles
    },
    'status': {
        'file': 'Fishcrispy.otf',
        'fallback': 'arial'  # Same as title for consistency
    },
    'button': {
        'file': 'Chunq.ttf',
        'fallback': 'arial'  # Simple, readable font for buttons
    },
    'winner': {
        'file': 'Fishcrispy.otf',
        'fallback': 'arial'  # Same as title for consistency
    }
}

def get_font_config(font_type):
    """
    Get font configuration for a specific font type
    Args:
        font_type: Type of font ('credit', 'start_button', 'title', etc.)
    Returns:
        dict: Font configuration with 'file' and 'fallback' keys
    """
    return FONT_CONFIG.get(font_type, {'file': 'arial', 'fallback': 'arial'}) 