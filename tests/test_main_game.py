import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import importlib

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TestMainGame(unittest.TestCase):

    def test_initialize_game(self):
        """Test the initialize_game function."""
        # Mock pygame and uno_ui in sys.modules for the duration of this test
        # We need to include src.pyuno.ui.uno_ui because main_game imports it
        with patch.dict(sys.modules, {'pygame': MagicMock(), 'src.pyuno.ui.uno_ui': MagicMock()}):

            # Import main_game inside the patched environment
            # If main_game was already imported, we reload it to ensure mocks are used
            # If it wasn't, we import it fresh
            try:
                import main_game
                importlib.reload(main_game)
            except ImportError:
                # If import fails (e.g. due to missing deps), we might need to mock more
                # But with pygame mocked, it should be fine.
                raise

            # Use patch.object on the module we just imported/reloaded
            # This ensures we are patching the Game/Player classes used by THAT module instance
            with patch.object(main_game, 'Game') as mock_game_class, \
                 patch.object(main_game, 'Player') as mock_player_class:

                # Setup mocks
                mock_game_instance = mock_game_class.return_value

                # Create player mocks
                player_mocks = [MagicMock(name=f"Player {i+1}") for i in range(4)]
                mock_player_class.side_effect = player_mocks

                # Call the function under test
                game = main_game.initialize_game()

                # Verify Game was instantiated
                mock_game_class.assert_called_once()

                # Verify Players were created with correct names
                expected_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
                self.assertEqual(mock_player_class.call_count, 4)
                actual_names = [call.args[0] for call in mock_player_class.call_args_list]
                self.assertEqual(actual_names, expected_names)

                # Verify players were added to game
                self.assertEqual(mock_game_instance.add_player.call_count, 4)
                for player_mock in player_mocks:
                    mock_game_instance.add_player.assert_any_call(player_mock)

                # Verify game.start_game() was called
                mock_game_instance.start_game.assert_called_once()

                # Verify return value
                self.assertEqual(game, mock_game_instance)

if __name__ == '__main__':
    unittest.main()
