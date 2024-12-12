import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 1100  # Increased window size
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
HIGHLIGHT = (255, 255, 0, 50)
DARK_BROWN = (101, 67, 33)

# Initialize the window
screen = pygame.display.set_mode((WINDOW_SIZE, BOARD_SIZE))
pygame.display.set_caption('Chess1UP')

def load_piece(name, scale=SQUARE_SIZE):
    try:
        path = os.path.join('assets', f'{name}.png')
        if not os.path.exists(path):
            print(f"Error: Image file not found: {path}")
            return None
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (scale, scale))
    except Exception as e:
        print(f"Error loading {name}.png: {str(e)}")
        return None

class PowerupSystem:
    def __init__(self):
        self.white_powerups = []
        self.black_powerups = []
        self.icon_size = SQUARE_SIZE
        self.powerup_types = {
            'orange': load_piece('orange_powerup', self.icon_size),
            'blue': load_piece('blue_powerup', self.icon_size),
            'purple': load_piece('purple_powerup', self.icon_size),
            'green': load_piece('green_powerup', self.icon_size)
        }
        self.font = pygame.font.SysFont('Tiny5-Regular', 24, bold=True)

    def add_powerup(self, color):
        powerup_list = self.white_powerups if color == 'white' else self.black_powerups
        if len(powerup_list) < 5:
            powerup_list.append(random.choice(['orange', 'blue', 'purple', 'green']))

    def use_powerup(self, powerup_type, color, game, pos):
        powerup_list = self.white_powerups if color == 'white' else self.black_powerups
        if powerup_type in powerup_list:
            powerup_list.remove(powerup_type)
            return self.activate_powerup(powerup_type, game, pos)
        return False

    def activate_powerup(self, powerup_type, game, pos):
        x, y = pos
        if powerup_type == 'orange':
            return self.orange_blast(game, x, y)
        elif powerup_type == 'blue':
            return self.blue_random(game)
        elif powerup_type == 'purple':
            return self.purple_select(game)
        elif powerup_type == 'green':
            return self.green_double(game)
        return False

    def orange_blast(self, game, x, y):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = game.board[new_y][new_x]
                    if piece and piece.color != game.turn and piece.name not in ['king', 'queen']:
                        game.board[new_y][new_x] = None
        return True

    def blue_random(self, game):
        pieces = [(x, y) for y in range(8) for x in range(8) 
                 if game.board[y][x] and game.board[y][x].color != game.turn 
                 and game.board[y][x].name not in ['king', 'queen']]
        if pieces:
            x, y = random.choice(pieces)
            game.board[y][x] = None
            return True
        return False

    def purple_select(self, game):
        game.powerup_selection_mode = 'purple'
        return True

    def green_double(self, game):
        pieces = [(x, y) for y in range(8) for x in range(8) 
                 if game.board[y][x] and game.board[y][x].color != game.turn 
                 and game.board[y][x].name not in ['king', 'queen']]
        if len(pieces) >= 2:
            for _ in range(2):
                if pieces:
                    x, y = random.choice(pieces)
                    pieces.remove((x, y))
                    game.board[y][x] = None
            return True
        return False
class Piece:
    def __init__(self, name, color, pos):
        self.name = name
        self.color = color
        self.pos = pos
        self.has_moved = False
        self.image = load_piece(f'{color}_{name}')

    def get_valid_moves(self, board):
        moves = []
        x, y = self.pos
        
        if self.name == 'pawn':
            direction = 1 if self.color == 'black' else -1
            # Forward move
            if 0 <= y + direction < 8 and board[y + direction][x] is None:
                moves.append((x, y + direction))
                # Initial two-square move
                if not self.has_moved and 0 <= y + 2*direction < 8 and board[y + 2*direction][x] is None:
                    moves.append((x, y + 2*direction))
            # Captures
            for dx in [-1, 1]:
                new_x = x + dx
                new_y = y + direction
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] and board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
        
        elif self.name == 'rook':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None:
                        moves.append((new_x, new_y))
                    elif board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                    new_x += dx
                    new_y += dy
        
        elif self.name == 'knight':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dx, dy in knight_moves:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None or board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
        
        elif self.name == 'bishop':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None:
                        moves.append((new_x, new_y))
                    elif board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                    new_x += dx
                    new_y += dy
        
        elif self.name == 'queen':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None:
                        moves.append((new_x, new_y))
                    elif board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break
                    new_x += dx
                    new_y += dy
        
        elif self.name == 'king':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None or board[new_y][new_x].color != self.color:
                        moves.append((new_x, new_y))
        
        return moves

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'white'
        self.powerups = PowerupSystem()
        self.powerup_selection_mode = None
        self.setup_board()

    def setup_board(self):
        # Setup pawns
        for x in range(8):
            self.board[1][x] = Piece('pawn', 'black', (x, 1))
            self.board[6][x] = Piece('pawn', 'white', (x, 6))

        # Setup other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for x in range(8):
            self.board[0][x] = Piece(piece_order[x], 'black', (x, 0))
            self.board[7][x] = Piece(piece_order[x], 'white', (x, 7))

    def draw(self, screen):
        # Draw board
        board_offset = (WINDOW_SIZE - BOARD_SIZE) // 2
        for y in range(8):
            for x in range(8):
                color = WHITE if (x + y) % 2 == 0 else GRAY
                pygame.draw.rect(screen, color, 
                               (x * SQUARE_SIZE + board_offset, 
                                y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    screen.blit(piece.image, 
                              (x * SQUARE_SIZE + board_offset, 
                               y * SQUARE_SIZE))

        # Draw valid moves
        for x, y in self.valid_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, HIGHLIGHT, s.get_rect())
            screen.blit(s, (x * SQUARE_SIZE + board_offset, 
                          y * SQUARE_SIZE))

        # Draw powerup labels
        white_label = self.powerups.font.render("White Powerups", True, DARK_BROWN)
        black_label = self.powerups.font.render("Black Powerups", True, DARK_BROWN)
        screen.blit(white_label, (10, 10))
        screen.blit(black_label, (WINDOW_SIZE - 180, 10))

        # Draw powerups
        for i, powerup in enumerate(self.powerups.white_powerups):
            screen.blit(self.powerups.powerup_types[powerup], 
                       (10, 50 + i * (self.powerups.icon_size + 10)))
        
        for i, powerup in enumerate(self.powerups.black_powerups):
            screen.blit(self.powerups.powerup_types[powerup], 
                       (WINDOW_SIZE - self.powerups.icon_size - 10, 
                        50 + i * (self.powerups.icon_size + 10)))

    def animate_powerup(self, powerup_color, powerup_type):
        if powerup_type == 'purple':
            # Pulsate effect with gradient
            for i in range(20):
                overlay = pygame.Surface((WINDOW_SIZE, BOARD_SIZE), pygame.SRCALPHA)
                alpha = 255 - (i * 12) if i < 10 else (i * 12) - 255
                color = (128, 0, 128, alpha)  # Ensure color is in RGBA format
                overlay.fill((0, 0, 0, 0))  # Clear the overlay first
                pygame.draw.circle(overlay, (128, 0, 128), (WINDOW_SIZE // 2, BOARD_SIZE // 2), 300 - (i * 15), 0)
                screen.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(100)

        elif powerup_type == 'orange':
            # Fire effect with flickering
            for _ in range(20):
                overlay = pygame.Surface((WINDOW_SIZE, BOARD_SIZE))
                overlay.fill((255, 69, 0))  # Fire color
                pygame.draw.rect(overlay, (255, 140, 0), (0, 0, WINDOW_SIZE, BOARD_SIZE), 0)
                screen.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(100)
                screen.fill(WHITE)  # Clear the overlay
                pygame.display.flip()
                pygame.time.delay(100)

        elif powerup_type == 'green':
            # Flash different green shades with smooth transition
            for _ in range(10):
                overlay = pygame.Surface((WINDOW_SIZE, BOARD_SIZE))
                shade = random.choice([(0, 255, 0), (0, 200, 0), (0, 150, 0), (0, 100, 0)])
                overlay.fill(shade)
                overlay.set_alpha(150)  # Semi-transparent
                screen.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(200)

        elif powerup_type == 'blue':
            # Flood effect with wave-like animation
            for i in range(20):
                overlay = pygame.Surface((WINDOW_SIZE, BOARD_SIZE), pygame.SRCALPHA)
                wave_height = 20 * (1 + 0.5 * (i % 2))  # Create a wave effect
                overlay.fill((0, 0, 255, 100))  # Light blue flood
                pygame.draw.rect(overlay, (0, 0, 255, 100), (0, wave_height, WINDOW_SIZE, BOARD_SIZE - wave_height))
                screen.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(100)

    def handle_click(self, pos):
        # Check powerup clicks
        if pos[0] < self.powerups.icon_size + 20:  # Left side (white powerups)
            if self.turn == 'white' and pos[1] > 50:
                powerup_index = (pos[1] - 50) // (self.powerups.icon_size + 10)
                if powerup_index < len(self.powerups.white_powerups):
                    self.powerup_selection_mode = self.powerups.white_powerups[powerup_index]
                    return
        elif pos[0] > WINDOW_SIZE - self.powerups.icon_size - 20:  # Right side (black powerups)
            if self.turn == 'black' and pos[1] > 50:
                powerup_index = (pos[1] - 50) // (self.powerups.icon_size + 10)
                if powerup_index < len(self.powerups.black_powerups):
                    self.powerup_selection_mode = self.powerups.black_powerups[powerup_index]
                    return

        # Convert click to board coordinates
        board_offset = (WINDOW_SIZE - BOARD_SIZE) // 2
        board_x = pos[0] - board_offset
        board_y = pos[1]
        x, y = board_x // SQUARE_SIZE, board_y // SQUARE_SIZE

        # Handle powerup selection mode
        if self.powerup_selection_mode and 0 <= x < 8 and 0 <= y < 8:
            if self.powerups.use_powerup(self.powerup_selection_mode, self.turn, self, (x, y)):
                # Call the animation with the color of the used powerup
                powerup_color = {
                    'orange': (255, 165, 0),  # Orange
                    'blue': (0, 0, 255),      # Blue
                    'purple': (128, 0, 128),  # Purple
                    'green': (0, 255, 0)       # Green
                }.get(self.powerup_selection_mode, (255, 255, 255))  # Default to white
                self.animate_powerup(powerup_color, self.powerup_selection_mode)
                
                self.turn = 'black' if self.turn == 'white' else 'white'
            self.powerup_selection_mode = None
            return

        # Handle normal piece movement
        if 0 <= x < 8 and 0 <= y < 8:
            if self.selected_piece:
                if (x, y) in self.valid_moves:
                    if self.board[y][x]:
                        self.powerups.add_powerup(self.turn)
                    
                    # Move piece
                    old_x, old_y = self.selected_piece.pos
                    self.board[y][x] = self.selected_piece
                    self.board[old_y][old_x] = None
                    self.selected_piece.pos = (x, y)
                    self.selected_piece.has_moved = True
                    
                    # Change turn
                    self.turn = 'black' if self.turn == 'white' else 'white'
                    self.selected_piece = None
                    self.valid_moves = []
                else:
                    piece = self.board[y][x]
                    if piece and piece.color == self.turn:
                        self.selected_piece = piece
                        self.valid_moves = piece.get_valid_moves(self.board)
            else:
                piece = self.board[y][x]
                if piece and piece.color == self.turn:
                    self.selected_piece = piece
                    self.valid_moves = piece.get_valid_moves(self.board)

def main():
    clock = pygame.time.Clock()
    game = ChessGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)

        screen.fill(WHITE)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()