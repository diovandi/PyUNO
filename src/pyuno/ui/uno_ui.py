import pygame
import sys
import os
import time
from ..core.uno_classes import Game, Player, Card
from ..config.font_config import get_font_config

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PyUNO by Group 19")

# Get the path to assets directory relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
logo_path = os.path.join(project_root, 'assets', 'uno_logo.png')
uno_logo_original = pygame.image.load(logo_path).convert_alpha()
pygame.display.set_icon(uno_logo_original)

GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)

def get_font_path(font_filename):
    """
    Get the absolute path to a font file in the assets directory
    """
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # Join with assets directory and filename
    return os.path.join(project_root, 'assets', font_filename)

def load_font_safe(font_path, size, fallback_font=None):
    """
    Safely load a font with fallback options
    Args:
        font_path: Path to the custom font file (relative or absolute)
        size: Font size
        fallback_font: Optional specific fallback font name
    Returns:
        pygame.font.Font object
    """
    # If it's a relative path starting with 'fonts/', convert to absolute path
    if font_path.startswith('fonts/'):
        font_filename = font_path.replace('fonts/', '')
        font_path = get_font_path(font_filename)
    
    try:
        # Try to load the custom font
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
        else:
            print(f"Warning: Font file '{font_path}' not found. Using fallback.")
    except pygame.error as e:
        print(f"Warning: Could not load font '{font_path}': {e}. Using fallback.")
    
    # Fallback options
    try:
        if fallback_font:
            # Try specific fallback font
            return pygame.font.SysFont(fallback_font, size)
    except:
        pass
    
    # Try common system fonts as fallbacks
    fallback_fonts = ['arial', 'helvetica', 'calibri', 'segoeui', 'trebuchetms']
    for font_name in fallback_fonts:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    
    # Last resort: use default pygame font
    return pygame.font.Font(None, size)

def load_font_by_type(font_type, size):
    """
    Load a font using the font configuration system
    Args:
        font_type: Type of font from font_config ('credit', 'title', etc.)
        size: Font size
    Returns:
        pygame.font.Font object
    """
    config = get_font_config(font_type)
    font_path = get_font_path(config['file'])
    return load_font_safe(font_path, size, config['fallback'])

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
        credit_font = load_font_by_type('credit', credit_font_size)

        button_width = int(current_width * 0.25)
        button_height = int(current_height * 0.12)
        button_x = current_width / 2 - button_width / 2
        button_y = current_height * 0.7 - button_height / 2
        start_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        start_font_size = int(button_height * 0.6)
        start_font = load_font_by_type('start_button', start_font_size)

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
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    card_path = os.path.join(project_root, 'assets')

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
    
    title_font = load_font_by_type('title', int(current_height * 0.05))
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
    
    # UNO QTE variables
    uno_qte_active = False
    uno_qte_start_time = 0
    uno_qte_duration = 3.0  # 3 seconds to call UNO
    uno_qte_button_rect = None

    while running:
        current_width, current_height = screen.get_width(), screen.get_height()

        card_width = int(current_width * 0.06)
        card_height = int(card_width * 1.45)
        CARD_IMAGES = load_card_images(card_width, card_height)
        
        status_font = load_font_by_type('status', int(current_height * 0.03))
        button_font = load_font_by_type('button', int(current_height * 0.035))
        uno_font_size = int(current_height * 0.04)
        uno_button_font = load_font_by_type('button', uno_font_size)
        winner_font = load_font_by_type('winner', int(current_height * 0.05))

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

        # UNO QTE Logic
        current_player = game.get_current_player()
        if current_player == game.players[0]:  # Human player
            if current_player.has_one_card() and not current_player.has_called_uno:
                if not uno_qte_active:
                    # Start UNO QTE
                    uno_qte_active = True
                    uno_qte_start_time = current_time
                else:
                    # Check if QTE time expired
                    if current_time - uno_qte_start_time >= uno_qte_duration:
                        # QTE failed - apply penalty
                        game.apply_uno_penalty(current_player)
                        draw_message = "UNO QTE Failed! Drew 2 cards."
                        draw_message_time = current_time
                        uno_qte_active = False
                        # Now advance the turn since the QTE is complete
                        game.next_player()
            else:
                # Player doesn't need to call UNO anymore
                uno_qte_active = False
        else:
            # Not human player's turn
            uno_qte_active = False

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
                            # Define draw pile position and rect for click detection
                            draw_pile_pos = (current_width / 2 + card_width * 0.2, current_height / 2 - card_height / 2)
                            draw_pile_rect = pygame.Rect(draw_pile_pos[0], draw_pile_pos[1], card_width, card_height)
                            
                            # Check UNO button first (highest priority)
                            if uno_button_rect.collidepoint(mouse_pos):
                                if uno_qte_active:
                                    # QTE successful - call UNO
                                    if game.call_uno(current_player):
                                        draw_message = "UNO called!"
                                        draw_message_time = current_time
                                        uno_qte_active = False
                                        # Advance the turn since UNO was called successfully
                                        game.next_player()
                                    else:
                                        draw_message = "Invalid UNO call!"
                                        draw_message_time = current_time
                                else:
                                    draw_message = "No UNO QTE active!"
                                    draw_message_time = current_time
                            # Check if draw pile was clicked
                            elif draw_pile_rect.collidepoint(mouse_pos):
                                # Only allow drawing if player has no playable cards or draw stack is active
                                if game.can_draw_card(current_player):
                                    drawn_card = game.draw_card(current_player)
                                    if drawn_card and drawn_card.can_play_on(game.deck.get_top_card(), game.selected_color):
                                        # Only auto-play if it won't result in 1 card (to let QTE handle UNO calls)
                                        if len(current_player.hand) > 1:
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
                                        # If player would have 1 card after playing, don't auto-play - let QTE handle it
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
                                        # Don't automatically call UNO - let the QTE system handle it
                                        if game.is_ai_turn:  # Only add delay if next player is AI
                                            last_turn_time = current_time
                                            waiting_for_turn = True

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

                # Get playable cards for the human player
                playable_cards = []
                if is_current_player:
                    top_card = game.deck.get_top_card()
                    if top_card:
                        playable_cards = player.get_playable_cards(top_card, game.selected_color)

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
                        
                        # Check if this card is playable and highlight with green if so
                        if card in playable_cards:
                            pygame.draw.rect(screen, (0, 255, 0), highlight_rect, 3, border_radius=5)  # Green for eligible cards
                        else:
                            pygame.draw.rect(screen, WHITE, highlight_rect, 2, border_radius=5)  # White for non-eligible
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

        # UNO QTE Visual Elements
        if uno_qte_active:
            # Draw UNO button with timer
            remaining_time = max(0, uno_qte_duration - (current_time - uno_qte_start_time))
            time_percentage = remaining_time / uno_qte_duration
            
            # Button color changes based on remaining time
            if time_percentage > 0.6:
                button_color = (0, 255, 0)  # Green - plenty of time
            elif time_percentage > 0.3:
                button_color = (255, 255, 0)  # Yellow - warning
            else:
                button_color = (255, 0, 0)  # Red - almost out of time
            
            # Draw button with color
            pygame.draw.rect(screen, button_color, uno_button_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, uno_button_rect, 3, border_radius=10)  # White border
            
            # Draw UNO text
            draw_text("UNO!", uno_button_font, WHITE, screen, uno_button_rect.centerx, uno_button_rect.centery)
            
            # Draw timer bar
            timer_bar_width = int(uno_button_width * 0.8)
            timer_bar_height = 8
            timer_bar_x = uno_button_rect.centerx - timer_bar_width // 2
            timer_bar_y = uno_button_rect.bottom + 10
            
            # Background bar
            pygame.draw.rect(screen, (100, 100, 100), (timer_bar_x, timer_bar_y, timer_bar_width, timer_bar_height), border_radius=4)
            # Progress bar
            progress_width = int(timer_bar_width * time_percentage)
            if progress_width > 0:
                pygame.draw.rect(screen, button_color, (timer_bar_x, timer_bar_y, progress_width, timer_bar_height), border_radius=4)
            
            # Draw warning message
            warning_text = f"CALL UNO! {remaining_time:.1f}s"
            warning_surface = status_font.render(warning_text, True, button_color)
            warning_rect = warning_surface.get_rect(center=(current_width / 2, current_height / 2 + card_height + 100))
            screen.blit(warning_surface, warning_rect)

        if game.waiting_for_color:
            draw_color_selection_menu(screen, current_width, current_height, button_font)

        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    if start_menu():
        from main_game import initialize_game
        game = initialize_game()
        main_game_ui(game)