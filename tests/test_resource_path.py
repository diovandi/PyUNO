import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from pyuno.utils.resource_path import get_resource_path, get_asset_path, get_font_path, resource_exists

class TestResourcePath(unittest.TestCase):
    """Test cases for resource path utilities."""

    def test_get_resource_path_pyinstaller(self):
        """Test getting resource path when running with PyInstaller."""
        with patch.object(sys, '_MEIPASS', '/tmp/meipass', create=True):
            path = get_resource_path('test_file.txt')
            expected_path = os.path.join('/tmp/meipass', 'test_file.txt')
            self.assertEqual(path, expected_path)

    def test_get_resource_path_dev(self):
        """Test getting resource path in development mode."""
        # Ensure _MEIPASS is not present
        has_meipass = hasattr(sys, '_MEIPASS')
        if has_meipass:
            saved_meipass = sys._MEIPASS
            del sys._MEIPASS

        try:
            path = get_resource_path('test_file.txt')

            # In dev mode, it should be relative to project root
            # We verify it's an absolute path and ends with the relative path
            self.assertTrue(os.path.isabs(path))
            self.assertTrue(path.endswith('test_file.txt'))

            # Verify it correctly navigates up from src/pyuno/utils
            # resource_path.py is in src/pyuno/utils
            # base path is Path(__file__).parent.parent.parent.parent (project root)
            expected_base = Path(src_path).parent
            expected_path = str(expected_base / 'test_file.txt')

            # Normalize paths for comparison (handle potential differences in separators or capitalization)
            self.assertEqual(os.path.normpath(path), os.path.normpath(expected_path))

        finally:
            if has_meipass:
                sys._MEIPASS = saved_meipass

    @patch('pyuno.utils.resource_path.get_resource_path')
    def test_get_asset_path(self, mock_get_resource_path):
        """Test getting asset path."""
        mock_get_resource_path.return_value = '/abs/path/assets/logo.png'

        result = get_asset_path('logo.png')

        expected_arg = os.path.join('assets', 'logo.png')
        mock_get_resource_path.assert_called_once_with(expected_arg)
        self.assertEqual(result, '/abs/path/assets/logo.png')

    @patch('pyuno.utils.resource_path.get_resource_path')
    def test_get_font_path(self, mock_get_resource_path):
        """Test getting font path."""
        mock_get_resource_path.return_value = '/abs/path/assets/font.ttf'

        result = get_font_path('font.ttf')

        expected_arg = os.path.join('assets', 'font.ttf')
        mock_get_resource_path.assert_called_once_with(expected_arg)
        self.assertEqual(result, '/abs/path/assets/font.ttf')

    @patch('pyuno.utils.resource_path.os.path.exists')
    @patch('pyuno.utils.resource_path.get_resource_path')
    def test_resource_exists(self, mock_get_resource_path, mock_exists):
        """Test checking if resource exists."""
        mock_get_resource_path.return_value = '/abs/path/file.txt'

        # Test exists = True
        mock_exists.return_value = True
        self.assertTrue(resource_exists('file.txt'))
        mock_get_resource_path.assert_called_with('file.txt')
        mock_exists.assert_called_with('/abs/path/file.txt')

        # Test exists = False
        mock_exists.return_value = False
        self.assertFalse(resource_exists('file.txt'))

if __name__ == '__main__':
    unittest.main()
