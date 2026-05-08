# checkers_engine.py

EMPTY = 0
WHITE = 1
BLACK = 2
WHITE_KING = 3
BLACK_KING = 4


class Checkers:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = WHITE

    def create_board(self):
        board = [[EMPTY for _ in range(8)] for _ in range(8)]

        # Black pieces (oben)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = BLACK

        # White pieces (unten)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = WHITE

        return board

    def print_board(self):
        symbols = {
            EMPTY: ".",
            WHITE: "w",
            BLACK: "b",
            WHITE_KING: "W",
            BLACK_KING: "B"
        }

        for row in self.board:
            print(" ".join(symbols[cell] for cell in row))
        print()

    def switch_player(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE

    def inside_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def get_piece_moves(self, r, c):
        piece = self.board[r][c]
        if piece == EMPTY:
            return []

        directions = []

        if piece in (WHITE, WHITE_KING):
            directions += [(-1, -1), (-1, 1)]
        if piece in (BLACK, BLACK_KING):
            directions += [(1, -1), (1, 1)]
        if piece in (WHITE_KING, BLACK_KING):
            directions += [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        moves = []

        # normale moves + captures
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if self.inside_board(nr, nc):
                if self.board[nr][nc] == EMPTY:
                    moves.append((r, c, nr, nc))
                else:
                    # jump capture
                    jump_r, jump_c = r + 2*dr, c + 2*dc
                    if self.inside_board(jump_r, jump_c):
                        if self.board[jump_r][jump_c] == EMPTY:
                            if self.is_enemy(piece, self.board[nr][nc]):
                                moves.append((r, c, jump_r, jump_c))

        return moves

    def is_enemy(self, piece, other):
        if piece in (WHITE, WHITE_KING):
            return other in (BLACK, BLACK_KING)
        if piece in (BLACK, BLACK_KING):
            return other in (WHITE, WHITE_KING)
        return False

    def get_valid_moves(self, player):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] in (player, player + 2):  # king check
                    moves.extend(self.get_piece_moves(r, c))
        return moves

    def make_move(self, move):
        r1, c1, r2, c2 = move
        piece = self.board[r1][c1]

        self.board[r1][c1] = EMPTY
        self.board[r2][c2] = piece

        # capture check
        if abs(r2 - r1) == 2:
            mid_r = (r1 + r2) // 2
            mid_c = (c1 + c2) // 2
            self.board[mid_r][mid_c] = EMPTY

        # promotion to king
        if r2 == 0 and piece == WHITE:
            self.board[r2][c2] = WHITE_KING
        if r2 == 7 and piece == BLACK:
            self.board[r2][c2] = BLACK_KING

        self.switch_player()

    def is_game_over(self):
        white_moves = self.get_valid_moves(WHITE)
        black_moves = self.get_valid_moves(BLACK)

        return len(white_moves) == 0 or len(black_moves) == 0

    def get_winner(self):
        white_moves = self.get_valid_moves(WHITE)
        black_moves = self.get_valid_moves(BLACK)

        if len(white_moves) == 0:
            return "BLACK"
        if len(black_moves) == 0:
            return "WHITE"
        return None