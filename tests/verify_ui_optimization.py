import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
# Set dummy driver just in case
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Import the module to be tested
from pyuno.ui import uno_ui

class TestStartMenuOptimization(unittest.TestCase):

    @patch('pyuno.ui.uno_ui.pygame')
    @patch('pyuno.ui.uno_ui.load_font_by_type')
    def test_start_menu_optimization_run(self, mock_load_font_func, mock_pygame_module):
        # Arguments are passed in reverse order of decorators (bottom up)
        # mock_load_font_func corresponds to @patch('...load_font_by_type')
        # mock_pygame_module corresponds to @patch('...pygame')

        # Setup mocks
        mock_screen = MagicMock()
        # mock_screen.get_width.return_value = 800 # Static value prevents resize logic from firing

        # We need dynamic return values for screen dimensions to simulate resize
        # Frame 1: 800 (Init)
        # Frame 2: 800 (Idle)
        # Frame 3: 800 (Resize event processed at END of frame)
        # Frame 4: 1024 (New size detected at START of frame)
        # Frame 5: 1024 (Quit)
        mock_screen.get_width.side_effect = [800, 800, 800, 1024, 1024]
        mock_screen.get_height.side_effect = [600, 600, 600, 768, 768]

        # Mock global screen in uno_ui
        uno_ui.screen = mock_screen

        # Mock events
        resize_event = MagicMock()
        resize_event.type = pygame.VIDEORESIZE
        resize_event.w = 1024
        resize_event.h = 768

        quit_event = MagicMock()
        quit_event.type = pygame.QUIT

        # Configure pygame mock
        mock_pygame_module.event.get.side_effect = [
            [],                 # Frame 1
            [],                 # Frame 2
            [resize_event],     # Frame 3 (Resize)
            [],                 # Frame 4
            [quit_event]        # Frame 5 (Quit)
        ]

        # Mock constants
        mock_pygame_module.QUIT = pygame.QUIT
        mock_pygame_module.VIDEORESIZE = pygame.VIDEORESIZE
        mock_pygame_module.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        mock_pygame_module.KEYDOWN = pygame.KEYDOWN
        mock_pygame_module.K_ESCAPE = pygame.K_ESCAPE
        mock_pygame_module.RESIZABLE = pygame.RESIZABLE

        # Mock mouse position
        mock_pygame_module.mouse.get_pos.return_value = (0, 0)

        # Mock display.set_mode
        mock_pygame_module.display.set_mode.return_value = mock_screen

        # Run start_menu
        try:
            uno_ui.start_menu()
        except StopIteration:
            pass

        # Verify calls
        print(f"load_font_by_type called {mock_load_font_func.call_count} times")
        print(f"pygame.transform.scale called {mock_pygame_module.transform.scale.call_count} times")

        # Verify Optimization
        # Expect 4 calls to load_font_by_type (2 initially + 2 on resize)
        # Expect 2 calls to transform.scale (1 initially + 1 on resize)
        self.assertEqual(mock_load_font_func.call_count, 4, "Optimization failed: Too many font loads")
        self.assertEqual(mock_pygame_module.transform.scale.call_count, 2, "Optimization failed: Too many logo scalings")

class TestLoadCardImagesCaching(unittest.TestCase):
    """Tests for load_card_images caching behavior."""

    def setUp(self):
        """Reset module-level cache state before each test."""
        uno_ui._RAW_CARD_IMAGES = None
        uno_ui._CACHED_SCALED_IMAGES = None
        uno_ui._LAST_CARD_DIMENSIONS = None

    @patch('pyuno.ui.uno_ui.pygame')
    def test_image_load_called_once_per_card(self, mock_pygame_module):
        """pygame.image.load is called once per card on first call, not on subsequent calls."""
        fake_surface = MagicMock()
        fake_surface.convert_alpha.return_value = fake_surface
        mock_pygame_module.image.load.return_value = fake_surface
        mock_pygame_module.transform.scale.return_value = fake_surface
        mock_pygame_module.error = pygame.error

        # First call - should load all images
        uno_ui.load_card_images(50, 70)
        first_call_count = mock_pygame_module.image.load.call_count
        self.assertGreater(first_call_count, 0, "Expected at least one image.load call on first invocation")

        # Second call with same dimensions - should NOT load images again
        uno_ui.load_card_images(50, 70)
        self.assertEqual(
            mock_pygame_module.image.load.call_count,
            first_call_count,
            "pygame.image.load should not be called again for same dimensions"
        )

    @patch('pyuno.ui.uno_ui.pygame')
    def test_transform_scale_only_on_dimension_change(self, mock_pygame_module):
        """pygame.transform.scale is called only when card dimensions change."""
        fake_surface = MagicMock()
        fake_surface.convert_alpha.return_value = fake_surface
        mock_pygame_module.image.load.return_value = fake_surface
        mock_pygame_module.transform.scale.return_value = fake_surface
        mock_pygame_module.error = pygame.error

        # First call
        uno_ui.load_card_images(50, 70)
        scale_count_after_first = mock_pygame_module.transform.scale.call_count
        self.assertGreater(scale_count_after_first, 0, "Expected scale calls on first invocation")

        # Second call with same dimensions - no additional scale calls
        uno_ui.load_card_images(50, 70)
        self.assertEqual(
            mock_pygame_module.transform.scale.call_count,
            scale_count_after_first,
            "transform.scale should not be called again when dimensions are unchanged"
        )

        # Third call with different dimensions - should rescale
        uno_ui.load_card_images(60, 84)
        self.assertGreater(
            mock_pygame_module.transform.scale.call_count,
            scale_count_after_first,
            "transform.scale should be called again when dimensions change"
        )

        # Fourth call with same new dimensions - no additional scale calls
        scale_count_after_resize = mock_pygame_module.transform.scale.call_count
        uno_ui.load_card_images(60, 84)
        self.assertEqual(
            mock_pygame_module.transform.scale.call_count,
            scale_count_after_resize,
            "transform.scale should not be called again when dimensions are unchanged after resize"
        )


if __name__ == '__main__':
    unittest.main()
