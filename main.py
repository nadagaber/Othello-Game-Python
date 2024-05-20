import pygame
import sys
import math

class OthelloBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]  # 8x8 empty grid

        # Initial state
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'

    def get_board(self):
        return self.board

    def display(self, screen, available_moves=None):
        screen.fill((0, 128, 0))  # Green background

        # Draw board grid
        for i in range(9):
            pygame.draw.line(screen, (0, 0, 0), (50 * i, 0), (50 * i, 400), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 50 * i), (400, 50 * i), 2)

        # Draw discs
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'B':
                    pygame.draw.circle(screen, (0, 0, 0), (25 + 50 * j, 25 + 50 * i), 20)
                elif self.board[i][j] == 'W':
                    pygame.draw.circle(screen, (255, 255, 255), (25 + 50 * j, 25 + 50 * i), 20)

        # Show available moves
        if available_moves is not None:
            for move in available_moves:
                pygame.draw.circle(screen, (0, 255, 0), (25 + 50 * move[1], 25 + 50 * move[0]), 5)

        #pygame.display.flip()

    def get_available_moves(self, color):
        moves = set()
        directions = [
            (0, -1),  # up
            (0, 1),  # down
            (1, 0),  # right
            (-1, 0),  # left
        ]
        opp_color = 'W' if color == 'B' else 'B'
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ':
                    for d in directions:
                        x, y = i + d[0], j + d[1]  # move to the cell in one of the possible directions
                        if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == opp_color:
                            while 0 <= x < 8 and 0 <= y < 8:  # continue traversing in the same direction to ensure that the cell is valid
                                if self.board[x][y] == ' ':
                                    break
                                elif self.board[x][y] == color:
                                    moves.add((i, j))
                                    break
                                x += d[0]
                                y += d[1]
        return moves

    def make_move(self, move, color):
        x, y = move
        self.board[x][y] = color
        self.outflank(move, color)

    def outflank(self, move, color):
        x, y = move
        opponent_color = 'W' if color == 'B' else 'B'
        directions = [
            (0, -1),  # up
            (0, 1),  # down
            (1, 0),  # right
            (-1, 0),  # left
        ]
        for dx, dy in directions:
            x_temp, y_temp = x + dx, y + dy
            to_flip = []
            while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent_color:
                to_flip.append((x_temp, y_temp))
                x_temp += dx
                y_temp += dy
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == color:
                for pos in to_flip:
                    self.board[pos[0]][pos[1]] = color

    def switch_player(self, current_player):
        return 'W' if current_player == 'B' else 'B'

    def count_discs(self):
        disc_counts = {'B': sum(row.count('B') for row in self.board),
                       'W': sum(row.count('W') for row in self.board)}
        return disc_counts['B'], disc_counts['W']


class GameController:
    def __init__(self):
        self.othello = OthelloBoard()

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 450))
        pygame.display.set_caption("Othello")

        current_player = 'B'  # Black always starts
        difficulty = None

        # Drawing buttons
        font = pygame.font.Font(None, 36)
        easy_button = pygame.Rect(100, 150, 200, 50)
        medium_button = pygame.Rect(100, 225, 200, 50)
        hard_button = pygame.Rect(100, 300, 200, 50)

        # Render label
        label_font = pygame.font.Font(None, 24)
        label_text = label_font.render("Choose difficulty", True, (0, 0, 0))
        label_rect = label_text.get_rect(center=(200, 100))

        while True:
            screen.fill((255, 255, 255))  # White background

            # Draw label
            screen.blit(label_text, label_rect)

            pygame.draw.rect(screen, (0, 255, 0), easy_button)
            pygame.draw.rect(screen, (0, 255, 0), medium_button)
            pygame.draw.rect(screen, (0, 255, 0), hard_button)

            easy_text = font.render("Easy", True, (0, 0, 0))
            medium_text = font.render("Medium", True, (0, 0, 0))
            hard_text = font.render("Hard", True, (0, 0, 0))
            screen.blit(easy_text, (150, 165))
            screen.blit(medium_text, (135, 240))
            screen.blit(hard_text, (150, 315))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        difficulty = 1
                    elif medium_button.collidepoint(event.pos):
                        difficulty = 3
                    elif hard_button.collidepoint(event.pos):
                        difficulty = 5
                    if difficulty is not None:
                        return self.start_game(screen, current_player, difficulty)

    def start_game(self, screen, current_player, difficulty):
        # Render disc count labels off-screen
        font = pygame.font.Font(None, 24)
        black_discs_label_offscreen = font.render("Black Discs: 0", True, (0, 0, 0))
        white_discs_label_offscreen = font.render("White Discs: 0", True, (0, 0, 0))

        white_discs_left, black_discs_left = 30, 30

        prev_black_count, prev_white_count = 0, 0

        while True:
            black_count, white_count = self.othello.count_discs()  # Calculate the disc counts before each move

            available_moves = self.othello.get_available_moves(current_player)
            if not available_moves:
                if current_player == 'B':
                    self.show_winner_popup(screen, "No available moves for black.", 0, 0, 2000)
                else:
                    self.show_winner_popup(screen, "No available moves for white.", 0, 0, 2000)

                current_player = self.othello.switch_player(current_player)
                available_moves = self.othello.get_available_moves(current_player)
                if not available_moves:  # no available moves for both white and black
                    black_count, white_count = self.othello.count_discs()
                    self.othello.display(screen)
                    if black_count > white_count:
                        self.show_winner_popup(screen, "Black Wins!", black_count, white_count, 10000)
                    elif white_count > black_count:
                        self.show_winner_popup(screen, "White Wins!", black_count, white_count, 10000)
                    else:
                        self.show_winner_popup(screen, "It's a tie!", black_count, white_count, 10000)
                    break

            self.othello.display(screen, available_moves if current_player == 'B' else None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_player == 'B':
                        if available_moves:
                            pos = pygame.mouse.get_pos()
                            row = math.floor(pos[1] / 50)
                            col = math.floor(pos[0] / 50)
                            if (row, col) in available_moves:
                                if black_discs_left > 0:
                                    black_discs_left -= 1
                                    self.othello.make_move((row, col), 'B')
                                    current_player = self.othello.switch_player(current_player)
                                else:
                                    black_count, white_count = self.othello.count_discs()
                                    self.othello.display(screen)
                                    self.show_winner_popup(screen, "Black ran out of discs",
                                                           0, 0, 2000)
                                    if black_count > white_count:
                                        self.show_winner_popup(screen, "Black wins!", black_count, white_count, 10000)
                                    elif white_count > black_count:
                                        self.show_winner_popup(screen, "White wins!", black_count, white_count, 10000)
                                    else:
                                        self.show_winner_popup(screen, "It's a tie", black_count, white_count, 10000)
                                    pygame.quit()
                                    sys.exit()
                    else:
                        if available_moves:
                            # Computer (white) player with Minimax algorithm
                            move = self.minimax(current_player, difficulty)
                            if move:
                                if white_discs_left > 0:
                                    white_discs_left -= 1
                                    self.othello.make_move(move, 'W')
                                    current_player = self.othello.switch_player(current_player)
                                else:
                                    black_count, white_count = self.othello.count_discs()
                                    self.othello.display(screen)
                                    if black_count > white_count:
                                        self.show_winner_popup(screen, "White ran out of discs",
                                                               0, 0, 2000)
                                        self.show_winner_popup(screen, "Black wins!", black_count, white_count, 10000)
                                    elif white_count > black_count:
                                        self.show_winner_popup(screen, "White wins!", black_count, white_count, 10000)
                                    else:
                                        self.show_winner_popup(screen, "It's a tie", black_count, white_count, 10000)
                                    pygame.quit()
                                    sys.exit()

            # Check if disc counts have changed
            if black_count != prev_black_count:
                black_discs_label_offscreen = font.render(f"Black Discs: {black_count}", True, (0, 0, 0))
                prev_black_count = black_count
            if white_count != prev_white_count:
                white_discs_label_offscreen = font.render(f"White Discs: {white_count}", True, (0, 0, 0))
                prev_white_count = white_count

            # Blit off-screen labels onto the main screen
            screen.blit(black_discs_label_offscreen, (20, 410))
            screen.blit(white_discs_label_offscreen, (20, 430))
            pygame.display.update()

    def minimax(self, player, depth, alpha=-math.inf, beta=math.inf):
        def max_value(board, depth, alpha, beta):
            if depth == 0 or not board.get_available_moves(player):
                return self.utility(board)
            max_val = -math.inf
            for move in board.get_available_moves(player):
                new_board = [row[:] for row in board.get_board()]
                new_game = OthelloBoard()
                new_game.board = new_board
                new_game.make_move(move, player)
                val = min_value(new_game, depth - 1, alpha, beta)
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break
            return max_val

        def min_value(board, depth, alpha, beta):
            if depth == 0 or not board.get_available_moves(board.switch_player(player)):
                return self.utility(board)
            min_val = math.inf
            for move in board.get_available_moves(board.switch_player(player)):
                new_board = [row[:] for row in board.get_board()]
                new_game = OthelloBoard()
                new_game.board = new_board
                new_game.make_move(move, board.switch_player(player))
                val = max_value(new_game, depth - 1, alpha, beta)
                min_val = min(min_val, val)
                beta = min(beta, min_val)
                if beta <= alpha:
                    break
            return min_val

        best_move = None
        best_value = -math.inf
        available_moves = self.othello.get_available_moves(player)
        for move in available_moves:
            new_board = [row[:] for row in self.othello.get_board()]
            new_game = OthelloBoard()
            new_game.board = new_board
            new_game.make_move(move, player)
            val = min_value(new_game, depth - 1, alpha, beta)
            if val > best_value:
                best_value = val
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move

    def utility(self, board):
        black_count, white_count = board.count_discs()
        return black_count - white_count

    def show_winner_popup(self, screen, winner, blackDiscCount, whiteDiscCount, time):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 20)

        # Draw a white rectangle for the popup
        popup_rect = pygame.Rect(50, 100, 300, 200)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect)

        # Render winner message
        textsurface_winner = myfont.render(winner, False, (0, 0, 0))
        winner_rect = textsurface_winner.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(textsurface_winner, winner_rect)

        # Render disc counts
        if blackDiscCount != 0:
            textsurface_blackDiscCount = myfont.render("Black:" + str(blackDiscCount), False, (0, 0, 0))
            blackDiscCount_rect = textsurface_blackDiscCount.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(textsurface_blackDiscCount, blackDiscCount_rect)

            textsurface_whiteDiscCount = myfont.render("White:" + str(whiteDiscCount), False, (0, 0, 0))
            whiteDiscCount_rect = textsurface_whiteDiscCount.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(textsurface_whiteDiscCount, whiteDiscCount_rect)

        pygame.display.update()
        pygame.time.wait(time)

game_controller = GameController()
game_controller.play_game()
