import random
from typing import List, Optional

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

    def can_play_on(self, other_card: 'Card', selected_color: Optional[str] = None) -> bool:
        # If this is a wild card, it can always be played
        if self.color == "wild":
            return True
            
        # If the other card is a wild card and has a selected color
        if other_card.color == "wild" and selected_color:
            # Can play if this card matches the selected color
            return self.color == selected_color
            
        # Special case for draw cards: can stack draw cards
        if self.value in ["drawtwo", "drawfour"] and other_card.value in ["drawtwo", "drawfour"]:
            return True
            
        # Normal case: match color or value
        return self.color == other_card.color or self.value == other_card.value

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
            self.cards = self.discard_pile
            self.discard_pile = [top_card]
            self.shuffle()

    def play_card(self, card: Card):
        self.discard_pile.append(card)

    def get_top_card(self) -> Optional[Card]:
        return self.discard_pile[-1] if self.discard_pile else None

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.has_called_uno = False

    def add_card(self, card: Card):
        self.hand.append(card)
        self.has_called_uno = False

    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)

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
        self.last_played_card = None
        self.is_ai_turn = False
        self.selected_color = None
        self.skip_next_turn = False
        self.draw_cards_pending = 0
        self.draw_stack_active = False  # Track if draw stack is active

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
            else:
                self.deck.cards.append(card)

        self.game_started = True
        self.is_ai_turn = self.current_player_index != 0  # True if first player is AI

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
                # Stack is broken - apply penalties to next player
                next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
                for _ in range(self.draw_cards_pending):
                    drawn_card = self.deck.draw_card()
                    if drawn_card:
                        next_player.add_card(drawn_card)
                self.draw_cards_pending = 0
                self.draw_stack_active = False
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

        # Handle special cards
        if card.value == "reverse":
            self.reverse_direction()
        elif card.value == "skip":
            self.skip_next_turn = True
        elif card.value == "drawfour":
            self.waiting_for_color = True
            return True  # Don't advance to next player until color is chosen

        # Handle wild cards
        if card.color == "wild":
            self.waiting_for_color = True
            return True  # Don't advance to next player until color is chosen

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
        
        # Create a new wild card with the same value but updated color
        if current_wild.value == "drawfour":
            new_card = Card("wild", "drawfour")
        else:
            new_card = Card("wild", "standard")
        
        # Replace the wild card in the discard pile
        self.deck.discard_pile[-1] = new_card
        
        # Reset the waiting state
        self.waiting_for_color = False
        self.last_played_card = None
        
        # Handle draw four penalty
        if new_card.value == "drawfour":
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            for _ in range(4):
                drawn_card = self.deck.draw_card()
                if drawn_card:
                    next_player.add_card(drawn_card)
            self.next_player()
        else:
            self.next_player()
        
        return True

    def draw_card(self, player: Player) -> Optional[Card]:
        if not self.game_started or player != self.get_current_player():
            return None

        # If draw stack is active, player must draw the accumulated cards
        if self.draw_stack_active:
            for _ in range(self.draw_cards_pending):
                drawn_card = self.deck.draw_card()
                if drawn_card:
                    player.add_card(drawn_card)
            self.draw_cards_pending = 0
            self.draw_stack_active = False
            self.next_player()
            return None

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
