import pygame
import sys
import os
import random

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

game_state = "start_menu"

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def start_menu():
    global game_state, screen

    while game_state == "start_menu":

        current_width = screen.get_width()
        current_height = screen.get_height()

        screen.fill(BLACK)

        # Dynamic Logo Sizing
        logo_height = int(current_height * 0.3)
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
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and start_button.collidepoint((mouse_x, mouse_y)):
                    game_state = "in_game"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     pygame.quit()
                     sys.exit()

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

def main_game():
    global screen

    # Game Setup
    card_width = int(screen.get_width() * 0.06)
    card_height = int(card_width * 1.45)
    CARD_IMAGES = load_card_images(card_width, card_height)
    
    status_font = pygame.font.Font('fonts/Fishcrispy.otf', int(screen.get_height() * 0.03))
    button_font = pygame.font.Font('fonts/Chunq.ttf', int(screen.get_height() * 0.035))

    full_deck = []
    COLORS = ["red", "yellow", "green", "blue"]
    VALUES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "drawtwo"]
    
    for color in COLORS:
        full_deck.append(f"{color}_0")
        for _ in range(2):
            for value in VALUES:
                full_deck.append(f"{color}_{value}")

    for _ in range(4): # Four of each wild card
        full_deck.append("wild_standard")
        full_deck.append("wild_drawfour")

    # Shuffle the deck
    random.shuffle(full_deck)

    # Deal 7 cards to each player
    player1_hand = [full_deck.pop() for _ in range(7)]
    player2_hand = [full_deck.pop() for _ in range(7)]
    player3_hand = [full_deck.pop() for _ in range(7)]
    player4_hand = [full_deck.pop() for _ in range(7)]

    # Setup the discard pile
    discard_pile = []
    # Flip cards from the deck to the discard pile until a non-wild card is found
    while True:
        top_card = full_deck.pop()
        if 'wild' not in top_card:
            discard_pile.append(top_card)
            break
        else:
            full_deck.insert(0, top_card)

    # Game Loop
    running = True
    while running:
        current_width, current_height = screen.get_width(), screen.get_height()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(RED)

        # Status Update Box
        status_text = "Player 1's Turn. Choose a card to play."
        text_surface = status_font.render(status_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(current_width / 2, current_height * 0.28))
        bg_rect = text_rect.copy().inflate(20, 10)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_surface, text_rect)
        
        # Draw Discard and Draw Piles
        discard_pile_pos = (current_width / 2 - card_width * 1.2, current_height / 2 - card_height / 2)
        draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
        
        screen.blit(CARD_IMAGES['card_back'], draw_pile_pos)
        draw_text("DRAW", button_font, (255, 255, 255), screen, draw_pile_pos[0] + card_width/2, draw_pile_pos[1] + card_height + 20)
        
        if discard_pile:
             screen.blit(CARD_IMAGES[discard_pile[-1]], discard_pile_pos)

        # Define card spacing and padding
        card_spacing = card_width * 0.6
        padding = 20

        # Player 1 (Bottom)
        player1_card_rects = []
        hand_width = (len(player1_hand) - 1) * card_spacing + card_width
        start_x = current_width / 2 - hand_width / 2
        
        for i, card_name in enumerate(player1_hand):
            card_rect = pygame.Rect(start_x + i * card_spacing, current_height - card_height - padding, card_width, card_height)
            player1_card_rects.append(card_rect)

        # Determine which card is being hovered over
        hovered_card_index = None
        # Iterate in reverse order so the top-most card is detected first
        for i in range(len(player1_card_rects) - 1, -1, -1):
            if player1_card_rects[i].collidepoint(mouse_pos):
                hovered_card_index = i
                break
        # Apply the hover effect
        for i, card_name in enumerate(player1_hand):
            card_y = current_height - card_height - padding
            # If this card is the one being hovered over, draw it lifted up
            if i == hovered_card_index:
                card_y -= 20
            screen.blit(CARD_IMAGES[card_name], (player1_card_rects[i].x, card_y))

        # Player 2 (Left)
        hand_height = (len(player2_hand) - 1) * card_spacing + card_height
        start_y = current_height / 2 - hand_height / 2
        for i, card_name in enumerate(player2_hand):
            rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], 90)
            screen.blit(rotated_card, (padding, start_y + i * card_spacing))
            
        # Player 3 (Top)
        hand_width = (len(player3_hand) - 1) * card_spacing + card_width
        start_x = current_width / 2 - hand_width / 2
        for i, card_name in enumerate(player3_hand):
            # REVISED: Drawing card_back at normal size
            screen.blit(CARD_IMAGES['card_back'], (start_x + i * card_spacing, padding))

        # Player 4 (Right)
        hand_height = (len(player4_hand) - 1) * card_spacing + card_height
        start_y = current_height / 2 - hand_height / 2
        for i, card_name in enumerate(player4_hand):
            rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], -90)
            card_x = current_width - card_height - padding
            screen.blit(rotated_card, (card_x, start_y + i * card_spacing))
            
        # UNO Button
        button_width = 120
        button_height = 50
        button_center_x = current_width * 0.7
        button_center_y = current_height - padding - (card_height/2)

        uno_button_rect = pygame.Rect(0, 0, button_width, button_height)
        uno_button_rect.center = (button_center_x, button_center_y)

        pygame.draw.rect(screen, (BLACK), uno_button_rect, border_radius=10)
        draw_text("UNO!", button_font, (WHITE), screen, uno_button_rect.centerx, uno_button_rect.centery)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    if game_state == "start_menu":
        start_menu()
    
    main_game()
