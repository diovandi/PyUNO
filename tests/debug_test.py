#!/usr/bin/env python3
"""
Comprehensive debug tests for all identified UNO game issues.
Tests the recent fixes for draw card logic, deck reshuffling, and special card handling.
"""

import sys
import os
import time

# Add the src directory to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
from pyuno.core.uno_classes import Game, Player, Card

def test_draw_two_consistency():
    """Test that Draw Two cards work consistently."""
    print("=== Testing Draw Two Card Consistency ===")
    
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    
    # Clear hands and set up test scenario
    player1.hand = [Card("red", "drawtwo")]
    player2.hand = [Card("blue", "5"), Card("blue", "6")]
    
    # Set a compatible top card
    game.deck.discard_pile = [Card("red", "5")]
    
    print(f"Player 1 hand: {[str(c) for c in player1.hand]}")
    print(f"Player 2 hand before: {[str(c) for c in player2.hand]}")
    print(f"Top card: {game.deck.get_top_card()}")
    
    # Play the Draw Two card
    success = game.play_card(player1, player1.hand[0])
    print(f"Draw Two played successfully: {success}")
    print(f"Draw stack active: {game.draw_stack_active}")
    print(f"Draw cards pending: {game.draw_cards_pending}")
    print(f"Current player: {game.get_current_player().name}")
    
    # In the stacking system, Player 2 must either stack another draw card or draw the penalty
    # Let's simulate Player 2 drawing the penalty
    if game.draw_stack_active and game.get_current_player() == player2:
        game.draw_card(player2)  # This should apply the penalty and end their turn
    
    print(f"Player 2 hand after drawing penalty: {[str(c) for c in player2.hand]}")
    
    # Player 2 should have 4 cards now (2 original + 2 penalty)
    expected_cards = 4
    actual_cards = len(player2.hand)
    print(f"Expected cards for Player 2: {expected_cards}, Actual: {actual_cards}")
    
    if actual_cards == expected_cards and not game.draw_stack_active:
        print("✅ Draw Two card working correctly!")
    else:
        print("❌ Draw Two card has issues!")
    
    print()

def test_draw_stack_break():
    """Test that breaking the draw stack works correctly."""
    print("=== Testing Draw Stack Break Logic ===")
    
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    
    # Set up draw stack scenario
    player1.hand = [Card("red", "drawtwo")]
    player2.hand = [Card("red", "5"), Card("blue", "3")]  # Give Player 2 more cards
    
    game.deck.discard_pile = [Card("red", "3")]  # Compatible top card
    
    # Player 1 plays Draw Two (this activates draw stack)
    game.play_card(player1, player1.hand[0])
    print(f"After Player 1 Draw Two - Stack active: {game.draw_stack_active}, Pending: {game.draw_cards_pending}")
    print(f"Current player: {game.get_current_player().name}")
    
    # Player 2 breaks the stack with a non-draw card
    initial_hand_size = len(player2.hand)
    print(f"Player 2 hand before breaking stack: {[str(c) for c in player2.hand]}")
    
    success = game.play_card(player2, player2.hand[0])  # Play the red 5
    print(f"Stack break successful: {success}")
    print(f"Draw stack active after break: {game.draw_stack_active}")
    print(f"Current player after break: {game.get_current_player().name}")
    print(f"Player 2 hand after: {[str(c) for c in player2.hand]}")
    
    # When breaking the stack:
    # 1. Player 2 gets the penalty cards (2 cards) - hand goes from 2 to 4
    # 2. Player 2 plays their card - hand goes from 4 to 3
    # 3. Stack is deactivated
    expected_final_hand_size = initial_hand_size + 2 - 1  # +2 penalty, -1 played card
    actual_final_hand_size = len(player2.hand)
    
    if not game.draw_stack_active and actual_final_hand_size == expected_final_hand_size:
        print("✅ Draw stack break working correctly!")
    else:
        print(f"❌ Draw stack break has issues! Expected {expected_final_hand_size} cards, got {actual_final_hand_size}")
    
    print()

def test_deck_empty_scenario():
    """Test behavior when deck runs out of cards."""
    print("=== Testing Deck Empty Scenario ===")
    
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    
    # Artificially empty the deck but keep one card in discard
    game.deck.cards = []
    game.deck.discard_pile = [Card("red", "5")]
    
    print(f"Deck size: {len(game.deck.cards)}")
    print(f"Discard pile size: {len(game.deck.discard_pile)}")
    
    # Try to draw a card - this should trigger reshuffle logic
    drawn_card = game.deck.draw_card()
    print(f"Drew card: {drawn_card}")
    print(f"Deck size after draw: {len(game.deck.cards)}")
    print(f"Discard pile size after draw: {len(game.deck.discard_pile)}")
    
    # With only one card in discard pile, no reshuffle should occur
    if drawn_card is None and len(game.deck.discard_pile) == 1:
        print("✅ Deck empty scenario handled correctly!")
    else:
        print("❌ Deck empty scenario has issues!")
    
    print()

def test_wild_card_resolution():
    """Test wild card color selection and resolution."""
    print("=== Testing Wild Card Resolution ===")
    
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    
    # Set up wild card scenario
    player1.hand = [Card("wild", "standard")]
    player2.hand = [Card("blue", "5")]
    
    game.deck.discard_pile = [Card("red", "5")]
    
    # Play wild card
    success = game.play_card(player1, player1.hand[0])
    print(f"Wild card played: {success}")
    print(f"Waiting for color: {game.waiting_for_color}")
    print(f"Top card before color selection: {game.deck.get_top_card()}")
    
    # Select color
    color_success = game.select_color("blue")
    print(f"Color selected: {color_success}")
    print(f"Selected color: {game.selected_color}")
    print(f"Top card after color selection: {game.deck.get_top_card()}")
    print(f"Current player: {game.get_current_player().name}")
    
    # The top card should now be a blue card, not a wild card
    top_card = game.deck.get_top_card()
    if top_card and top_card.color == "blue" and top_card.value == "0":
        print("✅ Wild card resolution working correctly!")
    else:
        print("❌ Wild card resolution has issues!")
    
    print()

def test_reverse_with_two_players():
    """Test reverse card behavior with exactly 2 players."""
    print("=== Testing Reverse Card with 2 Players ===")
    
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    
    # Set up reverse scenario
    player1.hand = [Card("red", "reverse")]
    game.deck.discard_pile = [Card("red", "5")]
    
    initial_player = game.get_current_player()
    print(f"Initial player: {initial_player.name}")
    print(f"Initial direction: {game.direction}")
    
    # Play reverse card
    success = game.play_card(player1, player1.hand[0])
    print(f"Reverse played: {success}")
    print(f"Direction after reverse: {game.direction}")
    print(f"Current player after reverse: {game.get_current_player().name}")
    
    # With 2 players, reverse should act like skip
    if game.direction == -1 and game.get_current_player() == initial_player:
        print("✅ Reverse with 2 players working correctly!")
    else:
        print("❌ Reverse with 2 players has issues!")
    
    print()

def run_all_tests():
    """Run all comprehensive tests."""
    print("🧪 Running Comprehensive UNO Game Tests 🧪\n")
    
    test_draw_two_consistency()
    test_draw_stack_break()
    test_deck_empty_scenario()
    test_wild_card_resolution()
    test_reverse_with_two_players()
    
    print("🏁 All tests completed! 🏁")

if __name__ == "__main__":
    run_all_tests() 