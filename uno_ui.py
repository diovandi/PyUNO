import pygame
import sys
import os
import random
import time
from uno_classes import Game, Player, Card

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PyUNO by Group 19")

uno_logo_original = pygame.image.load('uno_logo.png').convert_alpha()

# Colors
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def start_menu():
    global screen

    while True:
        current_width = screen.get_width()
        current_height = screen.get_height()

        screen.fill(BLACK)

        # Dynamic Logo Sizing
        logo_height = int(current_height * 0.5)
        logo_width = int(uno_logo_original.get_width() * (logo_height / uno_logo_original.get_height()))
        uno_logo_scaled = pygame.transform.scale(uno_logo_original, (logo_width, logo_height))
        logo_rect = uno_logo_scaled.get_rect(center=(current_width / 2, current_height * 0.35))
        screen.blit(uno_logo_scaled, logo_rect)
        
        credit_font_size = int(current_height * 0.04)
        credit_font = pygame.font.Font('fonts/Baksosapi.otf', credit_font_size)

        # Dynamic Button Sizing
        button_width = int(current_width * 0.25)
        button_height = int(current_height * 0.12)
        button_x = current_width / 2 - button_width / 2
        button_y = current_height * 0.7 - button_height / 2
        start_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        start_font_size = int(button_height * 0.6)
        start_font = pygame.font.Font('fonts/Arcadeclassic.ttf', start_font_size)

        draw_text("by Group 19", credit_font, WHITE, screen, current_width / 2, current_height * 0.95)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, BRIGHT_RED, start_button, border_radius=15)
        else:
            pygame.draw.rect(screen, RED, start_button, border_radius=15)
        
        draw_text("START", start_font, WHITE, screen, start_button.centerx, start_button.centery)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and start_button.collidepoint((mouse_x, mouse_y)):
                    return True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()

def load_card_images(card_width, card_height):
    card_images = {}
    card_path = 'cards'

    COLORS = ["red", "yellow", "green", "blue"]
    VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "drawtwo"]
    SPECIAL_CARDS = ["wild_standard", "wild_drawfour"]

    # Load numbered and action cards
    for color in COLORS:
        for value in VALUES:
            card_name = f"{color}_{value}"
            file_path = os.path.join(card_path, f"{card_name}.png")
            try:
                image = pygame.image.load(file_path).convert_alpha()
                card_images[card_name] = pygame.transform.scale(image, (card_width, card_height))
            except pygame.error as e:
                print(f"Error loading {file_path}: {e}")

    # Load special (wild) cards
    for card_name in SPECIAL_CARDS:
        file_path = os.path.join(card_path, f"{card_name}.png")
        try:
            image = pygame.image.load(file_path).convert_alpha()
            card_images[card_name] = pygame.transform.scale(image, (card_width, card_height))
        except pygame.error as e:
            print(f"Error loading {file_path}: {e}")
            
    # Load card back
    file_path = os.path.join(card_path, "card_back.png")
    try:
        image = pygame.image.load(file_path).convert_alpha()
        card_images["card_back"] = pygame.transform.scale(image, (card_width, card_height))
    except pygame.error as e:
        print(f"Error loading card_back.png: {e}")

    return card_images

def draw_color_selection_menu(screen, current_width, current_height, button_font):
    # Colors for the menu
    COLORS = {
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }
    
    # Create a semi-transparent overlay
    overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Draw title
    title_font = pygame.font.Font('fonts/Fishcrispy.otf', int(current_height * 0.05))
    draw_text("Choose a Color", title_font, WHITE, screen, current_width/2, current_height * 0.3)
    
    # Draw color buttons
    button_size = int(current_width * 0.1)
    spacing = int(current_width * 0.05)
    start_x = current_width/2 - (button_size * 2 + spacing * 1.5)
    y_pos = current_height * 0.5
    
    color_buttons = {}
    for i, (color_name, color) in enumerate(COLORS.items()):
        x_pos = start_x + (button_size + spacing) * i
        button_rect = pygame.Rect(x_pos, y_pos, button_size, button_size)
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)  # White border
        color_buttons[color_name] = button_rect
    
    return color_buttons

def main_game_ui(game: Game):
    global screen

    # Game Setup
    card_width = int(screen.get_width() * 0.06)
    card_height = int(card_width * 1.45)
    CARD_IMAGES = load_card_images(card_width, card_height)
    
    status_font = pygame.font.Font('fonts/Fishcrispy.otf', int(screen.get_height() * 0.03))
    button_font = pygame.font.Font('fonts/Chunq.ttf', int(screen.get_height() * 0.035))

    # Color mapping for RGB values
    COLOR_MAP = {
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }

    # Game Loop
    running = True
    last_turn_time = 0
    turn_delay = 2.0  # Delay in seconds between turns
    waiting_for_turn = False
    draw_message = ""
    draw_message_time = 0
    draw_message_duration = 2.0  # How long to show the draw message

    while running:
        current_width, current_height = screen.get_width(), screen.get_height()
        mouse_pos = pygame.mouse.get_pos()
        current_time = time.time()

        # Handle turn delays
        if waiting_for_turn:
            if current_time - last_turn_time >= turn_delay:
                waiting_for_turn = False
                if game.is_ai_turn and not game.waiting_for_color:
                    game.handle_ai_turn()
                    last_turn_time = current_time
                    waiting_for_turn = True
        elif game.is_ai_turn and not game.waiting_for_color:
            last_turn_time = current_time
            waiting_for_turn = True

        # Clear draw message if it's expired
        if draw_message and current_time - draw_message_time >= draw_message_duration:
            draw_message = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (not waiting_for_turn or not game.is_ai_turn):  # Left click
                    # Handle color selection menu
                    if game.waiting_for_color:
                        color_buttons = draw_color_selection_menu(screen, current_width, current_height, button_font)
                        for color, button_rect in color_buttons.items():
                            if button_rect.collidepoint(mouse_pos):
                                game.select_color(color)
                                if game.is_ai_turn:  # Only add delay if next player is AI
                                    last_turn_time = current_time
                                    waiting_for_turn = True
                                break
                    else:
                        # Check if draw pile was clicked
                        draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
                        draw_pile_rect = pygame.Rect(draw_pile_pos[0], draw_pile_pos[1], card_width, card_height)
                        if draw_pile_rect.collidepoint(mouse_pos):
                            current_player = game.get_current_player()
                            if current_player == game.players[0]:  # Human player
                                drawn_card = game.draw_card(current_player)
                                if drawn_card and drawn_card.can_play_on(game.deck.get_top_card(), game.selected_color):
                                    # Auto-play the drawn card if it can be played
                                    game.play_card(current_player, drawn_card)
                                    if drawn_card.color == "wild":
                                        # Auto-choose the most common color in hand
                                        color_counts = {"red": 0, "yellow": 0, "green": 0, "blue": 0}
                                        for card in current_player.hand:
                                            if card.color != "wild":
                                                color_counts[card.color] += 1
                                        chosen_color = max(color_counts.items(), key=lambda x: x[1])[0]
                                        game.select_color(chosen_color)
                                if game.is_ai_turn:  # Only add delay if next player is AI
                                    last_turn_time = current_time
                                    waiting_for_turn = True
                        else:
                            # Handle card selection for current player
                            current_player = game.get_current_player()
                            if current_player == game.players[0]:  # Human player
                                # Check if a card was clicked
                                for i, card in enumerate(current_player.hand):
                                    card_rect = pygame.Rect(
                                        current_width/2 - (len(current_player.hand) * card_width * 0.6)/2 + i * card_width * 0.6,
                                        current_height - card_height - 20,
                                        card_width,
                                        card_height
                                    )
                                    if card_rect.collidepoint(mouse_pos):
                                        if game.play_card(current_player, card):
                                            # Handle draw cards
                                            if card.value in ["drawtwo", "drawfour"]:
                                                next_player = game.players[(game.current_player_index + game.direction) % len(game.players)]
                                                if next_player == game.players[0]:  # If next player is human
                                                    cards_to_draw = 2 if card.value == "drawtwo" else 4
                                                    for _ in range(cards_to_draw):
                                                        game.draw_card(next_player)
                                                    draw_message = f"Drew {cards_to_draw} cards!"
                                                    draw_message_time = current_time
                                            if game.is_ai_turn:  # Only add delay if next player is AI
                                                last_turn_time = current_time
                                                waiting_for_turn = True
                                            break

        screen.fill(RED)

        # Status Update Box
        current_player = game.get_current_player()
        status_text = f"{current_player.name}'s Turn"
        if waiting_for_turn and game.is_ai_turn:  # Only show thinking for AI players
            status_text += " (Thinking...)"
        text_surface = status_font.render(status_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(current_width / 2, current_height * 0.28))
        bg_rect = text_rect.copy().inflate(20, 10)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_surface, text_rect)

        # Draw message
        if draw_message:
            draw_text_surface = status_font.render(draw_message, True, (255, 255, 255))
            draw_text_rect = draw_text_surface.get_rect(center=(current_width / 2, current_height * 0.35))
            draw_bg_rect = draw_text_rect.copy().inflate(20, 10)
            draw_bg_surface = pygame.Surface(draw_bg_rect.size, pygame.SRCALPHA)
            draw_bg_surface.fill((0, 0, 0, 150))
            screen.blit(draw_bg_surface, draw_bg_rect)
            screen.blit(draw_text_surface, draw_text_rect)

        # Draw Discard and Draw Piles
        discard_pile_pos = (current_width / 2 - card_width * 1.2, current_height / 2 - card_height / 2)
        draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
        
        screen.blit(CARD_IMAGES['card_back'], draw_pile_pos)
        draw_text("DRAW", button_font, (255, 255, 255), screen, draw_pile_pos[0] + card_width/2, draw_pile_pos[1] + card_height + 20)
        
        top_card = game.deck.get_top_card()
        if top_card:
            screen.blit(CARD_IMAGES[str(top_card)], discard_pile_pos)
            # Draw selected color indicator if it's a wild card
            if top_card.color == "wild" and game.selected_color:
                color_indicator_size = int(card_width * 0.3)
                color_pos = (discard_pile_pos[0] + card_width - color_indicator_size/2,
                           discard_pile_pos[1] + card_height - color_indicator_size/2)
                color_rect = pygame.Rect(0, 0, color_indicator_size, color_indicator_size)
                color_rect.center = color_pos
                pygame.draw.rect(screen, COLOR_MAP[game.selected_color], color_rect, border_radius=int(color_indicator_size/2))
                pygame.draw.rect(screen, WHITE, color_rect, 2, border_radius=int(color_indicator_size/2))

        # Draw player hands
        for i, player in enumerate(game.players):
            # Highlight current player's hand
            is_current_player = player == current_player
            highlight_offset = 20 if is_current_player else 0
            
            if i == 0:  # Human player (bottom)
                for j, card in enumerate(player.hand):
                    card_y = current_height - card_height - 20 - highlight_offset
                    if pygame.Rect(
                        current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                        card_y,
                        card_width,
                        card_height
                    ).collidepoint(mouse_pos):
                        card_y -= 20
                    screen.blit(CARD_IMAGES[str(card)], (
                        current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                        card_y
                    ))
                    if is_current_player:
                        # Draw highlight rectangle
                        highlight_rect = pygame.Rect(
                            current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6 - 5,
                            card_y - 5,
                            card_width + 10,
                            card_height + 10
                        )
                        pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
            else:  # AI players
                for j in range(len(player.hand)):
                    if i == 1:  # Left
                        rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], -90)  # Rotate -90 degrees
                        pos = (20 - highlight_offset, current_height/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6)
                        screen.blit(rotated_card, pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_height + 10, card_width + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
                    elif i == 2:  # Top
                        pos = (current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                               20 - highlight_offset)
                        screen.blit(CARD_IMAGES['card_back'], pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_width + 10, card_height + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
                    else:  # Right
                        rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], 90)  # Rotate 90 degrees
                        pos = (current_width - card_height - 20 + highlight_offset,
                              current_height/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6)
                        screen.blit(rotated_card, pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_height + 10, card_width + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)

        # UNO Button
        button_width = 120
        button_height = 50
        button_center_x = current_width / 2
        button_center_y = current_height / 2 + card_height + 50

        uno_button_rect = pygame.Rect(0, 0, button_width, button_height)
        uno_button_rect.center = (button_center_x, button_center_y)

        pygame.draw.rect(screen, (BLACK), uno_button_rect, border_radius=10)
        draw_text("UNO!", button_font, (WHITE), screen, uno_button_rect.centerx, uno_button_rect.centery)

        # Draw color selection menu if waiting for color
        if game.waiting_for_color:
            draw_color_selection_menu(screen, current_width, current_height, button_font)

        # Check for winner
        winner = game.check_winner()
        if winner:
            status_text = f"{winner.name} wins!"
            text_surface = status_font.render(status_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(current_width / 2, current_height * 0.28))
            bg_rect = text_rect.copy().inflate(20, 10)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 150))
            screen.blit(bg_surface, bg_rect)
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait 3 seconds
            running = False

        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    if start_menu():
        main_game_ui()