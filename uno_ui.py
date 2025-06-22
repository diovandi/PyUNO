import pygame
import sys
import os
import time
from uno_classes import Game, Player, Card

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PyUNO by Group 19")

uno_logo_original = pygame.image.load('uno_logo.png').convert_alpha()

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

        logo_height = int(current_height * 0.5)
        logo_width = int(uno_logo_original.get_width() * (logo_height / uno_logo_original.get_height()))
        uno_logo_scaled = pygame.transform.scale(uno_logo_original, (logo_width, logo_height))
        logo_rect = uno_logo_scaled.get_rect(center=(current_width / 2, current_height * 0.35))
        screen.blit(uno_logo_scaled, logo_rect)
        
        credit_font_size = int(current_height * 0.04)
        credit_font = pygame.font.Font('fonts/Baksosapi.otf', credit_font_size)

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

    for color in COLORS:
        for value in VALUES:
            card_name = f"{color}_{value}"
            file_path = os.path.join(card_path, f"{card_name}.png")
            try:
                image = pygame.image.load(file_path).convert_alpha()
                card_images[card_name] = pygame.transform.scale(image, (card_width, card_height))
            except pygame.error:
                pass

    for card_name in SPECIAL_CARDS:
        file_path = os.path.join(card_path, f"{card_name}.png")
        try:
            image = pygame.image.load(file_path).convert_alpha()
            card_images[card_name] = pygame.transform.scale(image, (card_width, card_height))
        except pygame.error:
            pass
            
    file_path = os.path.join(card_path, "card_back.png")
    try:
        image = pygame.image.load(file_path).convert_alpha()
        card_images["card_back"] = pygame.transform.scale(image, (card_width, card_height))
    except pygame.error:
        pass

    return card_images

def draw_color_selection_menu(screen, current_width, current_height, button_font):
    COLORS = {
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }
    
    overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font('fonts/Fishcrispy.otf', int(current_height * 0.05))
    draw_text("Choose a Color", title_font, WHITE, screen, current_width/2, current_height * 0.3)
    
    button_size = int(current_width * 0.1)
    spacing = int(current_width * 0.05)
    start_x = current_width/2 - (button_size * 2 + spacing * 1.5)
    y_pos = current_height * 0.5
    
    color_buttons = {}
    for i, (color_name, color) in enumerate(COLORS.items()):
        x_pos = start_x + (button_size + spacing) * i
        button_rect = pygame.Rect(x_pos, y_pos, button_size, button_size)
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)
        color_buttons[color_name] = button_rect
    
    return color_buttons

def main_game_ui(game):
    global screen

    running = True
    last_turn_time = 0
    turn_delay = 2.0
    waiting_for_turn = False
    draw_message = ""
    draw_message_time = 0
    draw_message_duration = 2.0

    while running:
        current_width, current_height = screen.get_width(), screen.get_height()

        card_width = int(current_width * 0.06)
        card_height = int(card_width * 1.45)
        CARD_IMAGES = load_card_images(card_width, card_height)
        
        status_font = pygame.font.Font('fonts/Fishcrispy.otf', int(current_height * 0.03))
        button_font = pygame.font.Font('fonts/Chunq.ttf', int(current_height * 0.035))
        uno_font_size = int(current_height * 0.04)
        uno_button_font = pygame.font.Font('fonts/Chunq.ttf', uno_font_size)
        winner_font = pygame.font.Font('fonts/Fishcrispy.otf', int(current_height * 0.05))

        mouse_pos = pygame.mouse.get_pos()
        current_time = time.time()

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

        # Check for UNO penalties
        penalized_players = game.check_uno_penalties(current_time)
        for player in penalized_players:
            game.apply_uno_penalty(player)
            if player == game.players[0]:  # Human player
                draw_message = "Forgot to call UNO! Drew 2 cards."
                draw_message_time = current_time

        if draw_message and current_time - draw_message_time >= draw_message_duration:
            draw_message = ""

        uno_button_width = int(current_width * 0.1)
        uno_button_height = int(current_height * 0.07)
        uno_button_rect = pygame.Rect(0, 0, uno_button_width, uno_button_height)
        
        player_hand_y_start = current_height - card_height - 20
        uno_button_rect.center = (int(current_width / 2), int(player_hand_y_start - uno_button_height / 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (not waiting_for_turn or not game.is_ai_turn):
                    if game.waiting_for_color:
                        color_buttons = draw_color_selection_menu(screen, current_width, current_height, button_font)
                        for color, button_rect in color_buttons.items():
                            if button_rect.collidepoint(mouse_pos):
                                game.select_color(color)
                                if game.is_ai_turn:
                                    last_turn_time = current_time
                                    waiting_for_turn = True
                                break
                    else:
                        current_player = game.get_current_player()
                        if current_player == game.players[0]:
                            # Check if draw pile was clicked
                            draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
                            draw_pile_rect = pygame.Rect(draw_pile_pos[0], draw_pile_pos[1], card_width, card_height)
                            if draw_pile_rect.collidepoint(mouse_pos):
                                # Only allow drawing if player has no playable cards or draw stack is active
                                if game.can_draw_card(current_player):
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
                                    # Player has playable cards but tried to draw
                                    draw_message = "You have playable cards!"
                                    draw_message_time = current_time
                            else:
                                # Handle card selection for current player
                                hovered_card_to_play_index = -1
                                base_y_for_human_click_detection = current_height - card_height - 20

                                for j in range(len(current_player.hand) - 1, -1, -1):
                                    card_rect_for_click = pygame.Rect(
                                        current_width/2 - (len(current_player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                                        base_y_for_human_click_detection,
                                        card_width,
                                        card_height
                                    )
                                    if card_rect_for_click.collidepoint(mouse_pos):
                                        hovered_card_to_play_index = j
                                        break
                                
                                if hovered_card_to_play_index != -1:
                                    card_to_play = current_player.hand[hovered_card_to_play_index]
                                    if game.play_card(current_player, card_to_play):
                                        # Check if player now has 1 card and needs to call UNO
                                        if current_player.has_one_card() and not current_player.has_called_uno:
                                            # Automatically call UNO for the player
                                            if game.call_uno(current_player):
                                                draw_message = "UNO called!"
                                                draw_message_time = current_time
                                        if game.is_ai_turn:  # Only add delay if next player is AI
                                            last_turn_time = current_time
                                            waiting_for_turn = True
                        if uno_button_rect.collidepoint(mouse_pos):
                            current_player = game.get_current_player()
                            if current_player == game.players[0]:  # Human player
                                if game.call_uno(current_player):
                                    draw_message = "UNO called!"
                                    draw_message_time = current_time
                                else:
                                    draw_message = "Invalid UNO call!"
                                    draw_message_time = current_time

        screen.fill(RED)

        current_player = game.get_current_player()
        status_text = f"{current_player.name}'s Turn"
        if waiting_for_turn and game.is_ai_turn:
            status_text += " (Thinking...)"
        text_surface = status_font.render(status_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(current_width / 2, current_height * 0.35))
        bg_rect = text_rect.copy().inflate(20, 10)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_surface, text_rect)

        if draw_message:
            draw_text_surface = status_font.render(draw_message, True, (255, 255, 255))
            draw_text_rect = draw_text_surface.get_rect(center=(current_width / 2, current_height * 0.35))
            draw_bg_rect = draw_text_rect.copy().inflate(20, 10)
            draw_bg_surface = pygame.Surface(draw_bg_rect.size, pygame.SRCALPHA)
            draw_bg_surface.fill((0, 0, 0, 150))
            screen.blit(draw_bg_surface, draw_bg_rect)
            screen.blit(draw_text_surface, draw_text_rect)

        discard_pile_pos = (current_width / 2 - card_width * 1.2, current_height / 2 - card_height / 2)
        draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
        
        # Check if draw pile should be clickable
        draw_pile_clickable = game.can_draw_card(current_player) and current_player == game.players[0]
        
        # Draw draw pile with visual feedback
        if draw_pile_clickable:
            # Highlight draw pile when clickable
            highlight_rect = pygame.Rect(draw_pile_pos[0] - 5, draw_pile_pos[1] - 5, card_width + 10, card_height + 10)
            pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 2, border_radius=5)
        
        screen.blit(CARD_IMAGES['card_back'], draw_pile_pos)
        draw_text("DRAW", button_font, (255, 255, 255), screen, draw_pile_pos[0] + card_width/2, draw_pile_pos[1] + card_height + 20)
        
        top_card = game.deck.get_top_card()
        if top_card:
            COLOR_MAP = {
                "red": (255, 0, 0),
                "yellow": (255, 255, 0),
                "green": (0, 255, 0),
                "blue": (0, 0, 255)
            }
            screen.blit(CARD_IMAGES[str(top_card)], discard_pile_pos)
            if top_card.color == "wild" and game.selected_color:
                color_indicator_size = int(card_width * 0.3)
                color_pos = (discard_pile_pos[0] + card_width - color_indicator_size/2,
                           discard_pile_pos[1] + card_height - color_indicator_size/2)
                color_rect = pygame.Rect(0, 0, color_indicator_size, color_indicator_size)
                color_rect.center = (int(color_pos[0]), int(color_pos[1]))
                pygame.draw.rect(screen, COLOR_MAP[game.selected_color], color_rect, border_radius=int(color_indicator_size/2))
                pygame.draw.rect(screen, WHITE, color_rect, 2, border_radius=int(color_indicator_size/2))

        for i, player in enumerate(game.players):
            is_current_player = player == current_player
            
            if i == 0:
                hovered_card_index = -1 
                base_y_for_card_row = current_height - card_height - 20 

                for j in range(len(player.hand) - 1, -1, -1):
                    card_rect_for_hover = pygame.Rect(
                        current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                        base_y_for_card_row,
                        card_width,
                        card_height
                    )
                    if card_rect_for_hover.collidepoint(mouse_pos) and is_current_player:
                        hovered_card_index = j 
                        break 

                for j, card in enumerate(player.hand):
                    card_draw_y = base_y_for_card_row
                    
                    if is_current_player:
                        card_draw_y -= 20

                    if j == hovered_card_index:
                        card_draw_y -= 20
     
                    screen.blit(CARD_IMAGES[str(card)], (
                        current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6,
                        card_draw_y 
                    ))
                    
                    if is_current_player:
                        highlight_rect = pygame.Rect(
                            current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6 - 5,
                            card_draw_y - 5, 
                            card_width + 10,
                            card_height + 10
                        )
                        pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
            else:  
                current_player_shift_x = 0
                current_player_shift_y = 0

                if is_current_player:
                    if i == 1: # Left AI Player: move right (towards center)
                        current_player_shift_x = 20
                    elif i == 2: # Top AI Player: move down (towards center)
                        current_player_shift_y = 20
                    else: # i == 3, Right AI Player: move left (towards center)
                        current_player_shift_x = -20 

                for j in range(len(player.hand)):
                    if i == 1: # Left
                        rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], -90)
                        pos = (20 + current_player_shift_x, current_height/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6 + current_player_shift_y)
                        screen.blit(rotated_card, pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_height + 10, card_width + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
                    elif i == 2: # Top
                        pos = (current_width/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6 + current_player_shift_x,
                               20 + current_player_shift_y)
                        screen.blit(CARD_IMAGES['card_back'], pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_width + 10, card_height + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)
                    else: # Right
                        rotated_card = pygame.transform.rotate(CARD_IMAGES['card_back'], 90)
                        pos = (current_width - card_height - 20 + current_player_shift_x,
                              current_height/2 - (len(player.hand) * card_width * 0.6)/2 + j * card_width * 0.6 + current_player_shift_y)
                        screen.blit(rotated_card, pos)
                        if is_current_player:
                            highlight_rect = pygame.Rect(pos[0] - 5, pos[1] - 5, card_height + 10, card_width + 10)
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)

        # Check if current player has 1 card and hasn't called UNO
        needs_uno_call = current_player.has_one_card() and not current_player.has_called_uno
        
        # Only show UNO button when player needs to call UNO
        if needs_uno_call and current_player == game.players[0]:  # Human player needs to call UNO
            pygame.draw.rect(screen, (255, 255, 0), uno_button_rect, border_radius=10)  # Yellow for warning
            draw_text("UNO!", uno_button_font, WHITE, screen, uno_button_rect.centerx, uno_button_rect.centery)
            
            # Show UNO warning message
            warning_text = "CALL UNO!"
            warning_surface = status_font.render(warning_text, True, (255, 255, 0))
            warning_rect = warning_surface.get_rect(center=(current_width / 2, current_height / 2 + card_height + 100))
            screen.blit(warning_surface, warning_rect)

        if game.waiting_for_color:
            draw_color_selection_menu(screen, current_width, current_height, button_font)

        winner = game.check_winner()
        if winner:
            winner_text = f"{winner.name} wins!"
            winner_surface = winner_font.render(winner_text, True, (255, 255, 255))
            winner_rect = winner_surface.get_rect(center=(current_width / 2, current_height * 0.25))
            winner_bg_rect = winner_rect.copy().inflate(20, 10)
            winner_bg_surface = pygame.Surface(winner_bg_rect.size, pygame.SRCALPHA)
            winner_bg_surface.fill((0, 0, 0, 150))
            screen.blit(winner_bg_surface, winner_bg_rect)
            screen.blit(winner_surface, winner_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    if start_menu():
        from main_game import initialize_game
        game = initialize_game()
        main_game_ui(game)