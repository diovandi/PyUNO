import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Mock pygame before importing anything that uses it
sys.modules['pygame'] = MagicMock()

# Import the function to be tested
# We try to import main_game, which imports src.pyuno.ui.uno_ui, which imports pygame
from main_game import initialize_game

class TestMainGame(unittest.TestCase):

    @patch('main_game.Game')
    @patch('main_game.Player')
    def test_initialize_game(self, mock_player, mock_game):
        """Test the initialize_game function."""
        # Setup mocks
        mock_game_instance = mock_game.return_value

        # Create player mocks
        player_mocks = [MagicMock(name=f"Player {i+1}") for i in range(4)]
        mock_player.side_effect = player_mocks

        # Call the function under test
        game = initialize_game()

        # Verify Game was instantiated
        mock_game.assert_called_once()

        # Verify Players were created with correct names
        expected_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.assertEqual(mock_player.call_count, 4)
        actual_names = [call.args[0] for call in mock_player.call_args_list]
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
