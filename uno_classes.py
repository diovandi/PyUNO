import random
from typing import List, Optional

class Card:
    def __init__(self, color: str, value: str):
        self.color = color
        self.value = value
        self.name = f"{color}_{value}"

    def __str__(self) -> str:
        return self.name

    def can_play_on(self, other_card: 'Card') -> bool:
        if self.color == "wild":
            return True
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

    def can_play_card(self, top_card: Card) -> bool:
        return any(card.can_play_on(top_card) for card in self.hand)

    def get_playable_cards(self, top_card: Card) -> List[Card]:
        return [card for card in self.hand if card.can_play_on(top_card)]

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

    def next_player(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def reverse_direction(self):
        self.direction *= -1

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def play_card(self, player: Player, card: Card) -> bool:
        if not self.game_started:
            return False

        top_card = self.deck.get_top_card()
        if not top_card or not card.can_play_on(top_card):
            return False

        player.remove_card(card)
        self.deck.play_card(card)

        # Handle special cards
        if card.value == "reverse":
            self.reverse_direction()
        elif card.value == "skip":
            self.next_player()
        elif card.value == "drawtwo":
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            for _ in range(2):
                drawn_card = self.deck.draw_card()
                if drawn_card:
                    next_player.add_card(drawn_card)
            self.next_player()
        elif card.color == "wild":
            if card.value == "drawfour":
                next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
                for _ in range(4):
                    drawn_card = self.deck.draw_card()
                    if drawn_card:
                        next_player.add_card(drawn_card)
                self.next_player()

        self.next_player()
        return True

    def draw_card(self, player: Player) -> Optional[Card]:
        card = self.deck.draw_card()
        if card:
            player.add_card(card)
        return card

    def check_winner(self) -> Optional[Player]:
        for player in self.players:
            if player.has_won():
                return player
        return None
