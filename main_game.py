import pygame
import sys
from uno_classes import Game, Player, Card
from uno_ui import start_menu, main_game_ui

def initialize_game():
    # Create game instance
    game = Game()
    
    # Create players
    players = [
        Player("Player 1"),
        Player("Player 2"),
        Player("Player 3"),
        Player("Player 4")
    ]
    
    # Add players to game
    for player in players:
        game.add_player(player)
    
    # Start the game
    game.start_game()
    
    return game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Show start menu
    if start_menu():
        # Initialize game
        game = initialize_game()
        
        # Start main game UI
        main_game_ui(game)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
