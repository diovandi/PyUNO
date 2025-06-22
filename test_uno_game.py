import unittest
import time
from unittest.mock import patch, MagicMock
from uno_classes import Card, Deck, Player, Game


class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_valid_card_creation(self):
        """Test creating valid cards."""
        # Test numbered cards
        card = Card("red", "5")
        self.assertEqual(card.color, "red")
        self.assertEqual(card.value, "5")
        self.assertEqual(card.name, "red_5")
        
        # Test action cards
        card = Card("blue", "skip")
        self.assertEqual(card.color, "blue")
        self.assertEqual(card.value, "skip")
        self.assertEqual(card.name, "blue_skip")
        
        # Test wild cards
        card = Card("wild", "standard")
        self.assertEqual(card.color, "wild")
        self.assertEqual(card.value, "standard")
        self.assertEqual(card.name, "wild_standard")
        
        card = Card("wild", "drawfour")
        self.assertEqual(card.color, "wild")
        self.assertEqual(card.value, "drawfour")
        self.assertEqual(card.name, "wild_drawfour")
    
    def test_invalid_card_creation(self):
        """Test creating invalid cards raises exceptions."""
        # Invalid color
        with self.assertRaises(ValueError):
            Card("purple", "5")
        
        # Invalid value
        with self.assertRaises(ValueError):
            Card("red", "11")
        
        # Wild card with invalid value
        with self.assertRaises(ValueError):
            Card("wild", "5")
        
        # Non-wild card with wild-only value
        with self.assertRaises(ValueError):
            Card("red", "standard")
    
    def test_card_string_representation(self):
        """Test card string representation."""
        card = Card("green", "7")
        self.assertEqual(str(card), "green_7")
        
        card = Card("wild", "drawfour")
        self.assertEqual(str(card), "wild_drawfour")
    
    def test_can_play_on(self):
        """Test card compatibility rules."""
        # Same color
        card1 = Card("red", "5")
        card2 = Card("red", "8")
        self.assertTrue(card1.can_play_on(card2))
        
        # Same value
        card1 = Card("red", "5")
        card2 = Card("blue", "5")
        self.assertTrue(card1.can_play_on(card2))
        
        # Different color and value
        card1 = Card("red", "5")
        card2 = Card("blue", "8")
        self.assertFalse(card1.can_play_on(card2))
        
        # Wild card can always be played
        wild_card = Card("wild", "standard")
        card2 = Card("blue", "8")
        self.assertTrue(wild_card.can_play_on(card2))
        
        # Playing on wild card with selected color
        card1 = Card("red", "5")
        wild_card = Card("wild", "standard")
        self.assertTrue(card1.can_play_on(wild_card, "red"))
        self.assertFalse(card1.can_play_on(wild_card, "blue"))


class TestDeck(unittest.TestCase):
    """Test cases for the Deck class."""
    
    def test_deck_initialization(self):
        """Test deck is properly initialized."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 108)  # Standard UNO deck size
        self.assertEqual(len(deck.discard_pile), 0)
    
    def test_deck_shuffle(self):
        """Test deck shuffling."""
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        # Note: shuffle might not change order in rare cases, but we can't test for that
        self.assertEqual(len(deck.cards), len(original_order))
    
    def test_draw_card(self):
        """Test drawing cards from deck."""
        deck = Deck()
        initial_count = len(deck.cards)
        
        card = deck.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(len(deck.cards), initial_count - 1)
        self.assertIsInstance(card, Card)
    
    def test_draw_card_empty_deck(self):
        """Test drawing from empty deck triggers reshuffle."""
        deck = Deck()
        # Draw all cards
        while deck.cards:
            deck.draw_card()
        
        # Add one card to discard pile
        deck.play_card(Card("red", "5"))
        
        # Drawing should reshuffle
        card = deck.draw_card()
        self.assertIsNotNone(card)
    
    def test_play_card(self):
        """Test playing cards to discard pile."""
        deck = Deck()
        card = Card("red", "5")
        
        deck.play_card(card)
        self.assertEqual(len(deck.discard_pile), 1)
        self.assertEqual(deck.discard_pile[0], card)
    
    def test_get_top_card(self):
        """Test getting top card from discard pile."""
        deck = Deck()
        
        # Empty discard pile
        self.assertIsNone(deck.get_top_card())
        
        # With cards in discard pile
        card1 = Card("red", "5")
        card2 = Card("blue", "8")
        deck.play_card(card1)
        deck.play_card(card2)
        
        self.assertEqual(deck.get_top_card(), card2)


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""
    
    def test_player_initialization(self):
        """Test player initialization."""
        player = Player("Test Player")
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(len(player.hand), 0)
        self.assertFalse(player.has_called_uno)
        self.assertEqual(player.uno_penalties, 0)
    
    def test_add_card(self):
        """Test adding cards to player's hand."""
        player = Player("Test Player")
        card = Card("red", "5")
        
        player.add_card(card)
        self.assertEqual(len(player.hand), 1)
        self.assertIn(card, player.hand)
        
        # Adding more cards should reset UNO call
        player.has_called_uno = True
        player.add_card(Card("blue", "8"))
        self.assertFalse(player.has_called_uno)
    
    def test_remove_card(self):
        """Test removing cards from player's hand."""
        player = Player("Test Player")
        card = Card("red", "5")
        player.add_card(card)
        
        player.remove_card(card)
        self.assertEqual(len(player.hand), 0)
        self.assertNotIn(card, player.hand)
    
    def test_call_uno(self):
        """Test UNO calling functionality."""
        player = Player("Test Player")
        
        # Can't call UNO with more than 1 card
        player.add_card(Card("red", "5"))
        player.add_card(Card("blue", "8"))
        self.assertFalse(player.call_uno())
        
        # Can call UNO with exactly 1 card
        player.remove_card(Card("red", "5"))
        self.assertTrue(player.call_uno())
        self.assertTrue(player.has_called_uno)
        
        # Can't call UNO twice
        self.assertFalse(player.call_uno())
    
    def test_check_uno_penalty(self):
        """Test UNO penalty checking."""
        player = Player("Test Player")
        
        # No penalty with more than 1 card
        player.add_card(Card("red", "5"))
        player.add_card(Card("blue", "8"))
        self.assertFalse(player.check_uno_penalty())
        
        # Penalty with 1 card and no UNO call
        player.remove_card(Card("red", "5"))
        self.assertTrue(player.check_uno_penalty())
        
        # No penalty with 1 card and UNO called
        player.call_uno()
        self.assertFalse(player.check_uno_penalty())
    
    def test_apply_uno_penalty(self):
        """Test applying UNO penalty."""
        player = Player("Test Player")
        player.add_card(Card("red", "5"))
        player.call_uno()
        
        player.apply_uno_penalty()
        self.assertEqual(player.uno_penalties, 1)
        self.assertFalse(player.has_called_uno)
    
    def test_can_play_card(self):
        """Test checking if player can play any card."""
        player = Player("Test Player")
        player.add_card(Card("red", "5"))
        player.add_card(Card("blue", "8"))
        
        top_card = Card("red", "3")
        self.assertTrue(player.can_play_card(top_card))
        
        top_card = Card("green", "9")
        self.assertFalse(player.can_play_card(top_card))
    
    def test_get_playable_cards(self):
        """Test getting list of playable cards."""
        player = Player("Test Player")
        card1 = Card("red", "5")
        card2 = Card("blue", "8")
        card3 = Card("green", "5")
        player.add_card(card1)
        player.add_card(card2)
        player.add_card(card3)
        
        top_card = Card("blue", "5")  # Value match
        playable = player.get_playable_cards(top_card)
        self.assertIn(card1, playable)  # Same value
        self.assertIn(card3, playable)  # Same value
        self.assertIn(card2, playable)  # Same color
    
    def test_has_one_card(self):
        """Test checking if player has exactly one card."""
        player = Player("Test Player")
        self.assertFalse(player.has_one_card())
        
        player.add_card(Card("red", "5"))
        self.assertTrue(player.has_one_card())
        
        player.add_card(Card("blue", "8"))
        self.assertFalse(player.has_one_card())
    
    def test_has_won(self):
        """Test checking if player has won."""
        player = Player("Test Player")
        self.assertTrue(player.has_won())
        
        player.add_card(Card("red", "5"))
        self.assertFalse(player.has_won())


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.player3 = Player("Player 3")
        self.player4 = Player("Player 4")
    
    def test_game_initialization(self):
        """Test game initialization."""
        self.assertEqual(len(self.game.players), 0)
        self.assertEqual(self.game.current_player_index, 0)
        self.assertEqual(self.game.direction, 1)
        self.assertFalse(self.game.game_started)
        self.assertFalse(self.game.waiting_for_color)
        self.assertIsNone(self.game.last_played_card)
        self.assertFalse(self.game.is_ai_turn)
        self.assertIsNone(self.game.selected_color)
        self.assertFalse(self.game.skip_next_turn)
        self.assertEqual(self.game.draw_cards_pending, 0)
        self.assertFalse(self.game.draw_stack_active)
    
    def test_add_player(self):
        """Test adding players to game."""
        self.game.add_player(self.player1)
        self.assertEqual(len(self.game.players), 1)
        self.assertIn(self.player1, self.game.players)
        
        self.game.add_player(self.player2)
        self.assertEqual(len(self.game.players), 2)
    
    def test_start_game(self):
        """Test starting the game."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        
        self.game.start_game()
        self.assertTrue(self.game.game_started)
        self.assertEqual(len(self.player1.hand), 7)
        self.assertEqual(len(self.player2.hand), 7)
        self.assertIsNotNone(self.game.deck.get_top_card())
        self.assertFalse(self.game.is_ai_turn)  # First player is human
    
    def test_start_game_insufficient_players(self):
        """Test starting game with insufficient players."""
        self.game.add_player(self.player1)
        
        with self.assertRaises(ValueError):
            self.game.start_game()
    
    def test_call_uno(self):
        """Test UNO calling in game context."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Give player 1 exactly one card
        self.player1.hand.clear()
        self.player1.add_card(Card("red", "5"))
        
        self.assertTrue(self.game.call_uno(self.player1))
        self.assertTrue(self.player1.has_called_uno)
    
    def test_next_player(self):
        """Test advancing to next player."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)
        self.game.start_game()
        
        # Normal advancement
        self.assertEqual(self.game.current_player_index, 0)
        self.game.next_player()
        self.assertEqual(self.game.current_player_index, 1)
        self.assertTrue(self.game.is_ai_turn)
        
        # Skip next turn
        self.game.skip_next_turn = True
        self.game.next_player()
        self.assertEqual(self.game.current_player_index, 0)  # Skip player 2, go to player 3, then back to 0
        self.assertFalse(self.game.is_ai_turn)
    
    def test_reverse_direction(self):
        """Test reversing game direction."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)
        self.game.start_game()
        
        self.assertEqual(self.game.direction, 1)
        self.game.reverse_direction()
        self.assertEqual(self.game.direction, -1)
        
        # With 2 players, reverse acts like skip
        self.game.players = [self.player1, self.player2]
        self.game.current_player_index = 0
        self.game.direction = 1
        self.game.reverse_direction()
        self.assertTrue(self.game.skip_next_turn)
    
    def test_get_current_player(self):
        """Test getting current player."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        self.assertEqual(self.game.get_current_player(), self.player1)
        self.game.next_player()
        self.assertEqual(self.game.get_current_player(), self.player2)
    
    def test_play_card(self):
        """Test playing cards."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Get a playable non-wild card
        top_card = self.game.deck.get_top_card()
        playable_card = None
        if top_card:
            for card in self.player1.hand:
                if card.can_play_on(top_card) and card.color != "wild":
                    playable_card = card
                    break
        
        if playable_card:
            initial_hand_size = len(self.player1.hand)
            
            # Check if player will have one card after playing
            will_have_one_card = (initial_hand_size - 1) == 1
            if will_have_one_card:
                # Call UNO before playing to avoid the UNO penalty condition
                self.game.call_uno(self.player1)
            
            self.assertTrue(self.game.play_card(self.player1, playable_card))
            self.assertEqual(len(self.player1.hand), initial_hand_size - 1)
            self.assertEqual(self.game.current_player_index, 1)
        elif top_card:
            # If no non-wild card is playable, test with a wild card
            for card in self.player1.hand:
                if card.can_play_on(top_card) and card.color == "wild":
                    playable_card = card
                    break
            
            if playable_card:
                initial_hand_size = len(self.player1.hand)
                
                # Check if player will have one card after playing
                will_have_one_card = (initial_hand_size - 1) == 1
                if will_have_one_card:
                    # Call UNO before playing to avoid the UNO penalty condition
                    self.game.call_uno(self.player1)
                
                self.assertTrue(self.game.play_card(self.player1, playable_card))
                self.assertEqual(len(self.player1.hand), initial_hand_size - 1)
                self.assertTrue(self.game.waiting_for_color)
                
                # Select a color to complete the turn
                self.assertTrue(self.game.select_color("red"))
                self.assertEqual(self.game.current_player_index, 1)
    
    def test_play_card_invalid(self):
        """Test playing invalid cards."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Try to play card when it's not player's turn
        card = Card("red", "5")
        self.assertFalse(self.game.play_card(self.player2, card))
        
        # Try to play card that doesn't match
        top_card = self.game.deck.get_top_card()
        if top_card and top_card.color != "red" and top_card.value != "5":
            self.assertFalse(self.game.play_card(self.player1, card))
    
    def test_select_color(self):
        """Test color selection for wild cards."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Play a wild card
        wild_card = None
        for card in self.player1.hand:
            if card.color == "wild":
                wild_card = card
                break
        
        if wild_card:
            self.game.play_card(self.player1, wild_card)
            self.assertTrue(self.game.waiting_for_color)
            
            # Select color
            self.assertTrue(self.game.select_color("red"))
            self.assertEqual(self.game.selected_color, "red")
            self.assertFalse(self.game.waiting_for_color)
    
    def test_can_draw_card(self):
        """Test checking if player can draw card."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Player should be able to draw if they have no playable cards
        # This depends on the current top card and player's hand
        # For this test, we'll just verify the method exists and works
        result = self.game.can_draw_card(self.player1)
        self.assertIsInstance(result, bool)
    
    def test_draw_card(self):
        """Test drawing cards."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        initial_hand_size = len(self.player1.hand)
        card = self.game.draw_card(self.player1)
        
        if card:
            self.assertEqual(len(self.player1.hand), initial_hand_size + 1)
        else:
            # Player might have drawn a playable card and played it
            self.assertGreaterEqual(len(self.player1.hand), initial_hand_size)
    
    def test_check_winner(self):
        """Test checking for winner."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # No winner initially
        self.assertIsNone(self.game.check_winner())
        
        # Player 1 wins
        self.player1.hand.clear()
        self.assertEqual(self.game.check_winner(), self.player1)
    
    def test_handle_ai_turn(self):
        """Test AI turn handling."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # AI turn should be False initially (first player is human)
        self.assertFalse(self.game.is_ai_turn)
        
        # Advance to AI player
        self.game.next_player()
        self.assertTrue(self.game.is_ai_turn)
        
        # Handle AI turn
        result = self.game.handle_ai_turn()
        self.assertIsInstance(result, bool)
    
    def test_apply_uno_penalty(self):
        """Test applying UNO penalty."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()
        
        # Give player 1 one card and don't call UNO
        self.player1.hand.clear()
        self.player1.add_card(Card("red", "5"))
        
        initial_hand_size = len(self.player1.hand)
        self.game.apply_uno_penalty(self.player1)
        
        self.assertEqual(len(self.player1.hand), initial_hand_size + 2)
        self.assertEqual(self.player1.uno_penalties, 1)
    
    def test_check_uno_penalties(self):
        """Test checking for UNO penalties."""
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.start_game()

        # Simulate player 1 playing a card so last_card_played_time is set
        top_card = self.game.deck.get_top_card()
        playable_card = None
        if top_card:
            for card in self.player1.hand:
                if card.can_play_on(top_card):
                    playable_card = card
                    break
        if playable_card:
            self.game.play_card(self.player1, playable_card)

        # Now give player 1 one card and don't call UNO
        self.player1.hand.clear()
        self.player1.add_card(Card("red", "5"))

        # Check penalties immediately (should be empty due to time window)
        penalized = self.game.check_uno_penalties(time.time())
        self.assertEqual(len(penalized), 0)

        # Check penalties after time window
        penalized = self.game.check_uno_penalties(time.time() + 4.0)
        self.assertIn(self.player1, penalized)


class TestGameIntegration(unittest.TestCase):
    """Integration tests for the game."""
    
    def test_full_game_flow(self):
        """Test a basic game flow."""
        game = Game()
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        
        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        # Verify game state
        self.assertTrue(game.game_started)
        self.assertEqual(len(player1.hand), 7)
        self.assertEqual(len(player2.hand), 7)
        self.assertIsNotNone(game.deck.get_top_card())
        
        # Verify initial player
        self.assertEqual(game.get_current_player(), player1)
        self.assertFalse(game.is_ai_turn)
    
    def test_special_cards(self):
        """Test special card effects."""
        game = Game()
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        # Test skip card
        skip_card = Card("red", "skip")
        player1.add_card(skip_card)
        
        # Set up a playable top card
        game.deck.discard_pile.clear()
        game.deck.play_card(Card("red", "5"))
        
        # Record the current player index
        start_index = game.current_player_index
        game.play_card(player1, skip_card)
        # After skip, the turn should go to the player after the next
        expected_index = (start_index + 2) % len(game.players)
        self.assertEqual(game.current_player_index, expected_index)
        
        # Test reverse card
        game.skip_next_turn = False
        reverse_card = Card("blue", "reverse")
        player1.add_card(reverse_card)
        game.deck.play_card(Card("blue", "3"))
        
        game.play_card(player1, reverse_card)
        self.assertEqual(game.direction, -1)


if __name__ == '__main__':
    unittest.main()
