import random
from typing import List, Optional
import time

class Card:
    VALID_COLORS = ["red", "yellow", "green", "blue", "wild"]
    VALID_VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "drawtwo", "standard", "drawfour"]

    def __init__(self, color: str, value: str):
        if color not in self.VALID_COLORS:
            raise ValueError(f"Invalid color: {color}")
        if value not in self.VALID_VALUES:
            raise ValueError(f"Invalid value: {value}")
            
        self.color = color
        self.value = value
        
        # For wild cards, we need to use the special format
        if color == "wild":
            if value not in ["standard", "drawfour"]:
                raise ValueError("Wild cards can only have 'standard' or 'drawfour' values")
            self.name = f"wild_{value}"
        else:
            if value in ["standard", "drawfour"]:
                raise ValueError("Non-wild cards cannot have 'standard' or 'drawfour' values")
            self.name = f"{color}_{value}"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.color == other.color and self.value == other.value

    def __hash__(self):
        return hash((self.color, self.value))

    def can_play_on(self, other_card: 'Card', selected_color: Optional[str] = None) -> bool:
        # Wild cards can always be played
        if self.color == "wild":
            return True
        # If the other card is a wild and a color is selected, match color
        if other_card.color == "wild" and selected_color:
            return self.color == selected_color
        # If this card is not wild, match color or value
        result = self.color == other_card.color or self.value == other_card.value
        return result

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        self._initialize_deck()

    def _initialize_deck(self):
        colors = ["red", "yellow", "green", "blue"]
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "drawtwo"]
        
        # Add numbered and action cards
        for color in colors:
            self.cards.append(Card(color, "0"))  # One zero of each color
            for _ in range(2):  # Two of each other card
                for value in values[1:]:  # Skip "0" as we already added it
                    self.cards.append(Card(color, value))

        # Add wild cards
        for _ in range(4):
            self.cards.append(Card("wild", "standard"))
            self.cards.append(Card("wild", "drawfour"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self) -> Optional[Card]:
        if not self.cards:
            self._reshuffle_discard_pile()
        return self.cards.pop() if self.cards else None

    def _reshuffle_discard_pile(self):
        if len(self.discard_pile) > 1:
            top_card = self.discard_pile.pop()
            self.cards = self.discard_pile.copy()
            self.discard_pile = [top_card]
            self.shuffle()
        # If only one card in discard pile, we can't reshuffle
        # This should rarely happen as cards are constantly being played

    def play_card(self, card: Card):
        self.discard_pile.append(card)

    def get_top_card(self) -> Optional[Card]:
        return self.discard_pile[-1] if self.discard_pile else None

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.has_called_uno = False
        self.uno_penalties = 0  # Track how many times player forgot to call UNO

    def add_card(self, card: Card):
        self.hand.append(card)
        # Reset UNO call when cards are added (if more than 1 card)
        if len(self.hand) > 1:
            self.has_called_uno = False

    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
            # Check if player should call UNO after removing a card
            if len(self.hand) == 1 and not self.has_called_uno:
                # Player forgot to call UNO - will be penalized
                pass

    def call_uno(self) -> bool:
        """Player calls UNO. Returns True if it's a valid call."""
        if len(self.hand) == 1 and not self.has_called_uno:
            self.has_called_uno = True
            return True
        return False

    def check_uno_penalty(self) -> bool:
        """Check if player should be penalized for not calling UNO."""
        if len(self.hand) == 1 and not self.has_called_uno:
            return True
        return False

    def apply_uno_penalty(self):
        """Apply penalty for not calling UNO - draw 2 cards."""
        self.uno_penalties += 1
        self.has_called_uno = False

    def can_play_card(self, top_card: Card, selected_color: Optional[str] = None) -> bool:
        return any(card.can_play_on(top_card, selected_color) for card in self.hand)

    def get_playable_cards(self, top_card: Card, selected_color: Optional[str] = None) -> List[Card]:
        return [card for card in self.hand if card.can_play_on(top_card, selected_color)]

    def has_one_card(self) -> bool:
        return len(self.hand) == 1

    def has_won(self) -> bool:
        return len(self.hand) == 0

class Game:
    def __init__(self):
        self.deck = Deck()
        self.players: List[Player] = []
        self.current_player_index = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.game_started = False
        self.waiting_for_color = False
        self.waiting_for_uno_call = False  # New state for UNO call management
        self.last_played_card = None
        self.is_ai_turn = False
        self.selected_color = None
        self.skip_next_turn = False
        self.draw_cards_pending = 0
        self.draw_stack_active = False  # Track if draw stack is active
        self.uno_call_window = 3.0  # Time window in seconds to call UNO after playing a card
        self.last_card_played_time = 0  # Track when the last card was played

    def add_player(self, player: Player):
        self.players.append(player)

    def start_game(self):
        if len(self.players) < 2:
            raise ValueError("Need at least 2 players to start the game")
        
        self.deck.shuffle()
        
        # Deal 7 cards to each player
        for _ in range(7):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.add_card(card)

        # Start the discard pile with a non-wild card
        while True:
            card = self.deck.draw_card()
            if card and card.color != "wild":
                self.deck.play_card(card)
                break
            elif card:
                self.deck.cards.append(card)

        self.game_started = True
        self.is_ai_turn = self.current_player_index != 0  # True if first player is AI

    def call_uno(self, player: Player) -> bool:
        """Handle UNO call from a player. Returns True if valid call."""
        if not self.game_started:
            return False
            
        if player.call_uno():
            if self.waiting_for_uno_call:
                self.waiting_for_uno_call = False
                # Advance to next player after successful UNO call
                self.next_player()
            return True
        return False

    def check_uno_penalties(self, current_time: float) -> List[Player]:
        """Check for UNO penalties and return list of players who need to draw cards."""
        penalized_players = []
        
        for player in self.players:
            if player.check_uno_penalty():
                # Check if enough time has passed since the last card was played
                # If last_card_played_time is 0, it means no card has been played yet
                if self.last_card_played_time == 0 or current_time - self.last_card_played_time >= self.uno_call_window:
                    penalized_players.append(player)
        
        return penalized_players

    def apply_uno_penalty(self, player: Player):
        """Apply UNO penalty to a player - draw 2 cards."""
        player.apply_uno_penalty()
        for _ in range(2):
            drawn_card = self.deck.draw_card()
            if drawn_card:
                player.add_card(drawn_card)

    def handle_uno_timeout(self) -> bool:
        """Handle UNO call timeout - apply penalty and advance turn. Returns True if timeout was handled."""
        if not self.waiting_for_uno_call:
            return False
            
        current_player = self.get_current_player()
        current_time = time.time()
        
        # Check if enough time has passed since the last card was played
        if current_time - self.last_card_played_time >= self.uno_call_window:
            # Apply penalty for not calling UNO
            self.apply_uno_penalty(current_player)
            self.waiting_for_uno_call = False
            # Advance to next player after penalty
            self.next_player()
            return True
        return False

    def next_player(self):
        if self.skip_next_turn:
            self.skip_next_turn = False
            self.current_player_index = (self.current_player_index + self.direction * 2) % len(self.players)
        else:
            self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        
        self.is_ai_turn = self.current_player_index != 0  # True if current player is AI

    def reverse_direction(self):
        self.direction *= -1
        # If there are only 2 players, reverse acts like skip
        if len(self.players) == 2:
            self.skip_next_turn = True

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def play_card(self, player: Player, card: Card) -> bool:
        if not self.game_started or player != self.get_current_player():
            return False

        top_card = self.deck.get_top_card()
        if not top_card or not card.can_play_on(top_card, self.selected_color):
            return False

        # Handle draw cards stacking
        if self.draw_stack_active:
            if card.value not in ["drawtwo", "drawfour"]:
                # Stack is broken - apply penalties to current player who is breaking the stack
                for _ in range(self.draw_cards_pending):
                    drawn_card = self.deck.draw_card()
                    if drawn_card:
                        player.add_card(drawn_card)
                self.draw_cards_pending = 0
                self.draw_stack_active = False
                
                # Handle the played card normally and continue to normal flow
                # (no early return, let the normal card playing logic handle the rest)
            elif card.value == "drawtwo" and top_card.value == "drawtwo":
                self.draw_cards_pending += 2
            elif card.value == "drawfour" and top_card.value == "drawfour":
                self.draw_cards_pending += 4
            else:
                # Can't stack draw two on draw four or vice versa
                return False
        else:
            if card.value in ["drawtwo", "drawfour"]:
                self.draw_stack_active = True
                self.draw_cards_pending = 4 if card.value == "drawfour" else 2

        player.remove_card(card)
        self.deck.play_card(card)
        self.last_played_card = card
        self.selected_color = None
        
        # Record the time when card was played for UNO penalty checking
        self.last_card_played_time = time.time()

        # Check if player now has 1 card and needs to call UNO (for any player)
        needs_uno_call = player.has_one_card() and not player.has_called_uno
        if needs_uno_call:
            self.waiting_for_uno_call = True
            # For AI players, automatically call UNO
            if player != self.players[0]:  # Not the human player
                self.call_uno(player)
                self.waiting_for_uno_call = False
            else:
                # For human player, handle special cards but don't advance turn yet
                if card.value == "reverse":
                    self.reverse_direction()
                elif card.value == "drawfour":
                    self.waiting_for_color = True
                elif card.color == "wild":
                    self.waiting_for_color = True
                # Don't advance turn yet - wait for UNO call
                return True

        # Handle special cards normally when no UNO call is needed
        if card.value == "reverse":
            self.reverse_direction()
            # In 2-player games, reverse_direction() sets skip_next_turn = True
            # which will be handled by the normal next_player() call at the end
        elif card.value == "skip":
            self.skip_next_turn = True
            self.next_player()
            return True
        elif card.value == "drawtwo":
            # Draw Two cards use the stacking system - penalties applied when stack is broken or turn ends
            # The draw stack is already activated above, just advance to next player
            self.next_player()
            return True
        elif card.value == "drawfour":
            # Draw Four penalty is handled in select_color()
            self.waiting_for_color = True
            return True  # Don't advance to next player until color is chosen

        # Handle wild cards
        if card.color == "wild":
            self.waiting_for_color = True
            return True  # Don't advance to next player until color is chosen

        # For normal cards, advance to next player
        self.next_player()
        return True

    def select_color(self, color: str) -> bool:
        if not self.waiting_for_color or not self.last_played_card:
            return False

        # Validate color
        if color not in ["red", "yellow", "green", "blue"]:
            return False

        # Store the selected color
        self.selected_color = color
        
        # Get the current wild card
        current_wild = self.deck.discard_pile[-1]
        
        # Handle draw four penalty BEFORE changing the card
        if current_wild.value == "drawfour":
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            for _ in range(4):
                drawn_card = self.deck.draw_card()
                if drawn_card:
                    next_player.add_card(drawn_card)
            # Skip the next player's turn by advancing twice
            self.current_player_index = (self.current_player_index + self.direction * 2) % len(self.players)
            self.is_ai_turn = self.current_player_index != 0
        else:
            self.next_player()
        
        # Create a new normal card with the selected color (not a wild card anymore)
        # This represents the "resolved" wild card with its chosen color
        # Use a neutral numbered card that any card can be played on
        new_card = Card(color, "0")
        
        # Replace the wild card in the discard pile
        self.deck.discard_pile[-1] = new_card
        
        # Reset the waiting state
        self.waiting_for_color = False
        self.last_played_card = None
        
        return True

    def can_draw_card(self, player: Player) -> bool:
        """Check if a player can draw a card (i.e., they have no playable cards)."""
        if not self.game_started or player != self.get_current_player():
            return False
            
        # If draw stack is active, player must draw
        if self.draw_stack_active:
            return True
            
        # Check if player has any playable cards
        top_card = self.deck.get_top_card()
        if not top_card:
            return True
            
        return not player.can_play_card(top_card, self.selected_color)

    def draw_card(self, player: Player) -> Optional[Card]:
        if not self.game_started or player != self.get_current_player():
            return None

        # If draw stack is active, player must draw the accumulated cards and their turn is skipped
        if self.draw_stack_active:
            cards_drawn = 0
            for _ in range(self.draw_cards_pending):
                drawn_card = self.deck.draw_card()
                if drawn_card:
                    player.add_card(drawn_card)
                    cards_drawn += 1
            self.draw_cards_pending = 0
            self.draw_stack_active = False
            # Skip the current player's turn by advancing to the next player
            self.next_player()
            return None

        # Normal draw - player draws one card
        card = self.deck.draw_card()
        if card:
            player.add_card(card)
            # If player draws a card, they must play it if possible
            top_card = self.deck.get_top_card()
            if top_card and card.can_play_on(top_card, self.selected_color):
                return card
            else:
                self.next_player()
        return card

    def check_winner(self) -> Optional[Player]:
        for player in self.players:
            if player.has_won():
                return player
        return None

    def handle_ai_turn(self) -> bool:
        """Handle AI player's turn. Returns True if the turn is complete."""
        if not self.is_ai_turn or self.waiting_for_color:
            return False

        current_player = self.get_current_player()
        top_card = self.deck.get_top_card()
        
        if not top_card:
            return False

        # AI calls UNO if they have 1 card and haven't called it yet
        if current_player.has_one_card() and not current_player.has_called_uno:
            self.call_uno(current_player)

        # Get playable cards
        playable_cards = current_player.get_playable_cards(top_card, self.selected_color)
        
        if playable_cards:
            # Choose the best card to play
            chosen_card = self._choose_best_card(playable_cards, self.draw_stack_active)
            if self.play_card(current_player, chosen_card):
                # If it's a wild card, choose the most common color in hand
                if chosen_card.color == "wild":
                    chosen_color = self._choose_best_color(current_player)
                    self.select_color(chosen_color)
                return True
            else:
                # If card couldn't be played, draw a card
                drawn_card = self.draw_card(current_player)
                if drawn_card and drawn_card.can_play_on(top_card, self.selected_color):
                    self.play_card(current_player, drawn_card)
                    if drawn_card.color == "wild":
                        chosen_color = self._choose_best_color(current_player)
                        self.select_color(chosen_color)
                return True
        else:
            # No playable cards, draw a card
            drawn_card = self.draw_card(current_player)
            if drawn_card and drawn_card.can_play_on(top_card, self.selected_color):
                self.play_card(current_player, drawn_card)
                if drawn_card.color == "wild":
                    chosen_color = self._choose_best_color(current_player)
                    self.select_color(chosen_color)
            return True

    def _choose_best_card(self, playable_cards: List[Card], draw_stack_active: bool) -> Card:
        """Choose the best card to play based on strategy."""
        if draw_stack_active:
            # If draw stack is active, prioritize draw cards
            for card in playable_cards:
                if card.value in ["drawtwo", "drawfour"]:
                    return card
            return random.choice(playable_cards)
        
        # Normal strategy
        for card in playable_cards:
            if card.value in ["drawfour", "drawtwo", "skip", "reverse"]:
                return card
        return random.choice(playable_cards)

    def _choose_best_color(self, player: Player) -> str:
        """Choose the best color based on the cards in hand."""
        color_counts = {"red": 0, "yellow": 0, "green": 0, "blue": 0}
        for card in player.hand:
            if card.color != "wild":
                color_counts[card.color] += 1
        return max(color_counts.items(), key=lambda x: x[1])[0]
