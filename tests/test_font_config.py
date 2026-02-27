import unittest
import sys
import os

# Add the src directory to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from pyuno.config.font_config import get_font_config, FONT_CONFIG

class TestFontConfig(unittest.TestCase):
    """Test cases for font configuration."""

    def test_get_font_config_valid_types(self):
        """Test retrieving configuration for valid font types."""
        for font_type, expected_config in FONT_CONFIG.items():
            config = get_font_config(font_type)
            self.assertEqual(config, expected_config, f"Config for '{font_type}' should match expected.")

    def test_get_font_config_unknown_type(self):
        """Test retrieving configuration for an unknown font type."""
        font_type = "unknown_font_type"
        expected_default = {'file': 'arial', 'fallback': 'arial'}
        config = get_font_config(font_type)
        self.assertEqual(config, expected_default, "Unknown font type should return default config.")

    def test_get_font_config_structure(self):
        """Test that returned configuration has required keys."""
        # Test with a known type
        config = get_font_config('title')
        self.assertIn('file', config)
        self.assertIn('fallback', config)

        # Test with an unknown type
        config = get_font_config('nonexistent')
        self.assertIn('file', config)
        self.assertIn('fallback', config)

if __name__ == '__main__':
    unittest.main()
