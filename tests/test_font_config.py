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

    def test_get_font_config_known_types(self):
        """Test get_font_config with known font types."""
        for font_type, expected_config in FONT_CONFIG.items():
            config = get_font_config(font_type)
            self.assertEqual(config, expected_config)
            self.assertIn('file', config)
            self.assertIn('fallback', config)

    def test_get_font_config_unknown_type(self):
        """Test get_font_config with an unknown font type."""
        unknown_type = 'unknown_font_type_xyz'
        expected_default = {'file': 'arial', 'fallback': 'arial'}
        config = get_font_config(unknown_type)
        self.assertEqual(config, expected_default)
        self.assertIn('file', config)
        self.assertIn('fallback', config)

if __name__ == '__main__':
    unittest.main()
