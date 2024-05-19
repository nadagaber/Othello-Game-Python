# Othello-Game

1. OthelloBoard Class

The `OthelloBoard` class is responsible for managing the game board, displaying the board, determining available moves, making moves, and counting discs.

      - Initialization (`__init__`): Sets up the initial board configuration with two black ('B') and two white ('W') pieces in the center.

      - `get_board()`: Returns the current state of the board.

      - `display(screen, available_moves=None)`: Draws the board, pieces, and highlights available moves.

      - `get_available_moves(color)`: Determines all possible moves for the given player ('B' or 'W') by checking all directions from each empty cell.

      - `make_move(move, color)`: Places a piece on the board and flips outflanked opponent's pieces.

      - `outflank(move, color)`: Flips the opponent's pieces in all directions if they are outflanked by the newly placed piece.

      - `switch_player(current_player)`: Switches the current player from black to white or vice versa.

      - `count_discs()`: Counts the number of black and white discs on the board.

2. GameController Class

The GameController class manages the game flow, including initializing the game, handling player input, and implementing the game logic.

      - Initialization (`__init__`): Initializes the `OthelloBoard`.

      - `play_game()`: Sets up the Pygame window and manages the main game loop, including player interactions and game state updates.

      - `start_game(screen, current_player, difficulty)`: Begins the game with the selected difficulty and manages the main gameplay loop, including handling player moves and updating the display.

      - `minimax(player, depth, alpha=-math.inf, beta=math.inf)`: Implements the Minimax algorithm with alpha-beta pruning for the computer player's moves. This function has two helper functions (`max_value` and `min_value`) for the recursive Minimax algorithm.

      - `utility(board)`: Evaluates the board state by calculating the difference between the number of black and white discs.

      - `show_winner_popup(screen, winner, blackDiscCount, whiteDiscCount, time)`: Displays a popup message showing the winner and the final disc counts.
