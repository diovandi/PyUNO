import unittest
import sys
import os

# Add the src directory to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from pyuno.config.font_config import get_font_config, FONT_CONFIG

class TestFontConfig(unittest.TestCase):
    """Test cases for the font configuration."""

    def test_valid_font_types(self):
        """Test getting configuration for valid font types."""
        for font_type, expected_config in FONT_CONFIG.items():
            self.assertEqual(get_font_config(font_type), expected_config)

    def test_unknown_font_type(self):
        """Test getting configuration for an unknown font type."""
        unknown_type = "unknown_font_type"
        expected_default = {'file': 'arial', 'fallback': 'arial'}
        self.assertEqual(get_font_config(unknown_type), expected_default)

    def test_return_structure(self):
        """Test that the returned dictionary always has 'file' and 'fallback' keys."""
        font_types = list(FONT_CONFIG.keys()) + ["unknown_font_type", "another_unknown", ""]
        for font_type in font_types:
            config = get_font_config(font_type)
            self.assertIn('file', config)
            self.assertIn('fallback', config)
            self.assertIsInstance(config['file'], str)
            self.assertIsInstance(config['fallback'], str)

if __name__ == '__main__':
    unittest.main()
