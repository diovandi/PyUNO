# UNO Game Unit Tests

This document describes the comprehensive unit test suite for the UNO game implementation.

## Test Structure

The test suite is organized into several test classes, each focusing on a specific component of the game:

### 1. TestCard
Tests for the `Card` class functionality:
- **test_valid_card_creation**: Tests creating valid cards (numbered, action, and wild cards)
- **test_invalid_card_creation**: Tests that invalid card creation raises appropriate exceptions
- **test_card_string_representation**: Tests the string representation of cards
- **test_can_play_on**: Tests card compatibility rules (color matching, value matching, wild cards)

### 2. TestDeck
Tests for the `Deck` class functionality:
- **test_deck_initialization**: Verifies deck is properly initialized with 108 cards
- **test_deck_shuffle**: Tests deck shuffling functionality
- **test_draw_card**: Tests drawing cards from the deck
- **test_draw_card_empty_deck**: Tests reshuffling when deck is empty
- **test_play_card**: Tests adding cards to the discard pile
- **test_get_top_card**: Tests retrieving the top card from discard pile

### 3. TestPlayer
Tests for the `Player` class functionality:
- **test_player_initialization**: Tests player object creation
- **test_add_card**: Tests adding cards to player's hand
- **test_remove_card**: Tests removing cards from player's hand
- **test_call_uno**: Tests UNO calling functionality
- **test_check_uno_penalty**: Tests UNO penalty checking
- **test_apply_uno_penalty**: Tests applying UNO penalties
- **test_can_play_card**: Tests checking if player can play any card
- **test_get_playable_cards**: Tests getting list of playable cards
- **test_has_one_card**: Tests checking if player has exactly one card
- **test_has_won**: Tests checking if player has won

### 4. TestGame
Tests for the `Game` class functionality:
- **test_game_initialization**: Tests game object creation
- **test_add_player**: Tests adding players to the game
- **test_start_game**: Tests game initialization and dealing
- **test_start_game_insufficient_players**: Tests error handling for insufficient players
- **test_call_uno**: Tests UNO calling in game context
- **test_next_player**: Tests player turn advancement
- **test_reverse_direction**: Tests direction reversal
- **test_get_current_player**: Tests getting current player
- **test_play_card**: Tests playing cards
- **test_play_card_invalid**: Tests invalid card playing
- **test_select_color**: Tests color selection for wild cards
- **test_can_draw_card**: Tests checking if player can draw
- **test_draw_card**: Tests drawing cards
- **test_check_winner**: Tests winner detection
- **test_handle_ai_turn**: Tests AI turn handling
- **test_apply_uno_penalty**: Tests applying UNO penalties
- **test_check_uno_penalties**: Tests checking for UNO penalties

### 5. TestGameIntegration
Integration tests for game flow:
- **test_full_game_flow**: Tests basic game initialization and setup
- **test_special_cards**: Tests special card effects (skip, reverse)

## Running the Tests

### Option 1: Using unittest directly
```bash
python -m unittest test_uno_game.py -v
```

### Option 2: Using pytest (if installed)
```bash
python -m pytest test_uno_game.py -v
```

### Option 3: Running specific test classes
```bash
# Run only Card tests
python -m unittest test_uno_game.TestCard -v

# Run only Player tests
python -m unittest test_uno_game.TestPlayer -v

# Run only Game tests
python -m unittest test_uno_game.TestGame -v
```

### Option 4: Running specific test methods
```bash
# Run a specific test method
python -m unittest test_uno_game.TestCard.test_valid_card_creation -v
```

## Test Coverage

The test suite covers:

1. **Card Logic**: All card creation, validation, and compatibility rules
2. **Deck Management**: Deck initialization, shuffling, drawing, and discard pile management
3. **Player State**: Hand management, UNO calling, penalties, and win conditions
4. **Game Flow**: Turn management, player advancement, special card effects
5. **AI Behavior**: AI turn handling and decision making
6. **Error Handling**: Invalid operations and edge cases
7. **Integration**: End-to-end game flow testing

## Key Features Tested

- **UNO Rules**: Proper implementation of UNO game rules
- **Card Compatibility**: Color and value matching logic
- **Special Cards**: Skip, reverse, draw two, draw four, and wild cards
- **UNO Penalties**: Time-based penalty system for forgetting to call UNO
- **AI Strategy**: Basic AI decision making for card selection
- **Game State Management**: Proper state transitions and validation
- **Error Conditions**: Handling of invalid operations and edge cases

## Expected Test Results

When all tests pass, you should see output similar to:
```
test_can_play_on (test_uno_game.TestCard.test_can_play_on) ... ok
test_card_string_representation (test_uno_game.TestCard.test_card_string_representation) ... ok
test_invalid_card_creation (test_uno_game.TestCard.test_invalid_card_creation) ... ok
test_valid_card_creation (test_uno_game.TestCard.test_valid_card_creation) ... ok
...
----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

## Troubleshooting

If tests fail, check:
1. All required dependencies are installed
2. The `uno_classes.py` file is in the same directory
3. Python version compatibility (Python 3.6+ recommended)
4. No syntax errors in the test file

## Adding New Tests

To add new tests:
1. Create a new test method in the appropriate test class
2. Follow the naming convention: `test_descriptive_name`
3. Add a docstring describing what the test does
4. Use appropriate assertions (`assertEqual`, `assertTrue`, `assertRaises`, etc.)
5. Run the tests to ensure they pass 