"""
Resource path utility for PyInstaller compatibility
Handles proper asset loading for both development and executable environments
"""

import os
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    
    Args:
        relative_path: Path relative to the base directory (e.g., 'assets/uno_logo.png')
    
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS')
    except AttributeError:
        # Running in development mode
        # Go up from src/pyuno/utils to project root
        base_path = Path(__file__).parent.parent.parent.parent
    
    return os.path.join(base_path, relative_path)

def get_asset_path(asset_name):
    """
    Get path to an asset file
    
    Args:
        asset_name: Name of the asset file (e.g., 'uno_logo.png')
    
    Returns:
        Absolute path to the asset
    """
    return get_resource_path(os.path.join('assets', asset_name))

def get_font_path(font_name):
    """
    Get path to a font file
    
    Args:
        font_name: Name of the font file (e.g., 'Gameplay.ttf')
    
    Returns:
        Absolute path to the font
    """
    return get_resource_path(os.path.join('assets', font_name))

def resource_exists(relative_path):
    """
    Check if a resource exists
    
    Args:
        relative_path: Path relative to the base directory
    
    Returns:
        True if the resource exists, False otherwise
    """
    return os.path.exists(get_resource_path(relative_path)) 