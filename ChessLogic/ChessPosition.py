from .Pieces import *
from .Colors import Color


class ChessState:
    """Class that describes some game states"""

    def __init__(self, **kwargs):
        self.move_color = Color.WHITE
        self.white_king_under_attack = False
        self.black_king_under_attack = False
        self.white_attack = set()
        self.black_attack = set()

        for k, v in kwargs.items():
            self.__setattr__(k, v)


class CastlingState:
    """Class that describes which castling are available"""

    def __init__(self, **kwargs):
        self.white_king_side = True
        self.white_queen_side = True
        self.black_king_side = True
        self.black_queen_side = True

        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def copy(self):
        return CastlingState(white_king_side=self.white_king_side,
                             white_queen_side=self.white_queen_side,
                             black_king_side=self.black_king_side,
                             black_queen_side=self.black_queen_side)

    def __str__(self):
        result = ''
        for castling, letter in [(self.white_king_side, 'K'), (self.white_queen_side, 'Q'),
                                 (self.black_king_side, 'k'), (self.black_queen_side, 'q')]:
            if castling:
                result += letter

        return result


def cell_to_coords(cell):  # "e7" -> 4, 6
    return ord(cell[0]) - 97, int(cell[1]) - 1


def coords_to_cell(x, y):  # 4, 6 -> "e7"
    return chr(x + 97) + str(y + 1)


class ChessPosition:
    """Class that describes single chess position, and can generate new positions from it"""

    promotions = {'knight': Knight,
                  'rook': Rook,
                  'bishop': Bishop,
                  'queen': Queen}

    def __init__(self,
                 move_color: Color,
                 castling_state: CastlingState,
                 en_passant=None):

        self.pieces = []
        self.move_color = move_color
        self.castling_state = castling_state
        self.en_passant = en_passant

        self.board = [[None for _ in range(8)] for _ in range(8)]

    def add_piece(self, piece):
        self.pieces.append(piece)
        self.board[piece.y][piece.x] = piece

    def calculate_possible_moves(self):
        for piece in self.pieces:
            if piece.color == self.move_color:
                piece.calculate_valid_moves()

    def get_piece_at(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]

        return None

    def is_empty_at(self, x, y):
        return self.get_piece_at(x, y) is None

    def get_state(self):
        white_attack_cells, black_attack_cells = set(), set()
        white_king, black_king = None, None
        state = ChessState(move_color=self.move_color)

        for piece in self.pieces:
            if isinstance(piece, King):
                if piece.color == Color.WHITE:
                    white_king = piece
                else:
                    black_king = piece

            if piece.color == Color.WHITE:
                white_attack_cells.update(piece.get_attack_moves())
            else:
                black_attack_cells.update(piece.get_attack_moves())

        if white_king.position in black_attack_cells:
            state.white_king_under_attack = True

        if black_king.position in white_attack_cells:
            state.black_king_under_attack = True

        state.white_attack = white_attack_cells
        state.black_attack = black_attack_cells

        return state

    def generate_position_after_move(self, x, y, new_x, new_y, promotion=None):
        chess_position = self.copy()
        chess_position.make_move(x, y, new_x, new_y, promotion)
        return chess_position

    def make_move(self, x, y, new_x, new_y, promotion=None):
        moved_piece = self.get_piece_at(x, y)
        captured_piece = self.get_piece_at(new_x, new_y)

        if captured_piece:
            self.pieces.remove(captured_piece)

        # En passant capturing
        if isinstance(moved_piece, Pawn):
            if (new_x, new_y) == self.en_passant:
                if new_y == 2:
                    captured_en_passant = self.get_piece_at(new_x, 3)
                else:
                    captured_en_passant = self.get_piece_at(new_x, 4)

                self.board[captured_en_passant.y][captured_en_passant.x] = None
                self.pieces.remove(captured_en_passant)

        # En passant
        self.en_passant = None
        if isinstance(moved_piece, Pawn) and abs(y - new_y) == 2:
            self.en_passant = (x, (y + new_y) // 2)

        # Promotion to higher piece
        if promotion and isinstance(moved_piece, Pawn) and \
                ((self.move_color == Color.WHITE and new_y == 7) or (self.move_color == Color.BLACK and new_y == 0)):

            promotion_class = {'Q': Queen, 'B': Bishop, 'N': Knight, 'R': Rook}[promotion]
            self.pieces.remove(moved_piece)
            moved_piece = moved_piece.copy(promotion_class, self)
            self.pieces.append(moved_piece)

        moved_piece.set_position(new_x, new_y)

        self.board[y][x] = None
        self.board[new_y][new_x] = moved_piece

        # Castling
        if isinstance(moved_piece, King):

            if moved_piece.color == Color.WHITE:
                self.castling_state.white_king_side = False
                self.castling_state.white_queen_side = False
            else:
                self.castling_state.black_king_side = False
                self.castling_state.black_queen_side = False

            if (x, y, new_x, new_y) == (4, 0, 6, 0):  # White king side castling
                moved_rook = self.board[0][7]
                moved_rook.set_position(5, 0)
                self.board[0][7] = None
                self.board[0][5] = moved_rook

            if (x, y, new_x, new_y) == (4, 0, 2, 0):  # White queen side castling
                moved_rook = self.board[0][0]
                moved_rook.set_position(3, 0)
                self.board[0][0] = None
                self.board[0][3] = moved_rook

            if (x, y, new_x, new_y) == (4, 7, 6, 7):  # Black king side castling
                moved_rook = self.board[7][7]
                moved_rook.set_position(5, 7)
                self.board[7][7] = None
                self.board[7][5] = moved_rook

            if (x, y, new_x, new_y) == (4, 7, 2, 7):  # Black queen side castling
                moved_rook = self.board[7][0]
                moved_rook.set_position(3, 7)
                self.board[7][0] = None
                self.board[7][3] = moved_rook

        # If rook moved, castling with no longer available
        if isinstance(moved_piece, Rook):
            if (x, y) == (0, 0):
                self.castling_state.white_queen_side = False

            if (x, y) == (7, 0):
                self.castling_state.white_king_side = False

            if (x, y) == (0, 7):
                self.castling_state.black_queen_side = False

            if (x, y) == (7, 7):
                self.castling_state.black_king_side = False

        # If something moved at rook position, castling no longer available
        if (new_x, new_y) == (0, 0):
            self.castling_state.white_queen_side = False

        if (new_x, new_y) == (7, 0):
            self.castling_state.white_king_side = False

        if (new_x, new_y) == (0, 7):
            self.castling_state.black_queen_side = False

        if (new_x, new_y) == (7, 7):
            self.castling_state.black_king_side = False

        self.move_color = self.move_color.opposite()
        return {'is_piece_captured': captured_piece is not None}

    def copy(self):
        chess_position = ChessPosition(self.move_color, self.castling_state.copy(), self.en_passant)
        for piece in self.pieces:
            chess_position.add_piece(piece.copy(None, chess_position))

        return chess_position

    @classmethod
    def generate_from_fen(cls, fen):
        pieces, move_color, castling, en_passant, *other = fen.split()

        castling_state = CastlingState(white_king_side='K' in castling,
                                       white_queen_side='Q' in castling,
                                       black_king_side='k' in castling,
                                       black_queen_side='q' in castling)

        en_passant = None if en_passant == '-' else cell_to_coords(en_passant)

        chess_position = ChessPosition([Color.WHITE, Color.BLACK][move_color == 'b'], castling_state, en_passant)

        for row, row_text in zip(range(7, -1, -1), pieces.split('/')):
            column = 0

            for char in row_text:
                if char in '12345678':
                    column += int(char)
                else:
                    piece_class = dict(k=King,
                                       q=Queen,
                                       r=Rook,
                                       b=Bishop,
                                       n=Knight,
                                       p=Pawn)[char.lower()]

                    piece_color = [Color.BLACK, Color.WHITE][char.isupper()]

                    chess_position.add_piece(piece_class(column, row, piece_color, chess_position))
                    column += 1

        return chess_position

    def generate_fen(self):
        pieces = ''

        for row in range(7, -1, -1):
            empty_spaces = 0
            for column in range(8):
                if self.board[row][column] is None:
                    empty_spaces += 1

                else:
                    if empty_spaces > 0:
                        pieces += f'{empty_spaces}'

                    empty_spaces = 0
                    pieces += self.board[row][column].char_repr

            if empty_spaces > 0:
                pieces += f'{empty_spaces}'

            pieces += '/'

        pieces = pieces[:-1]

        move_color = 'w' if self.move_color == Color.WHITE else 'b'

        castling = str(self.castling_state)

        en_passant = coords_to_cell(*self.en_passant) if self.en_passant else '-'

        return ' '.join([pieces, move_color, castling, en_passant])

    def show_board(self):
        pieces = [[' ' + (piece.text_repr if piece else '▰▱'[(i + j) % 2]) + ' '
                   for j, piece in enumerate(row)]
                  for i, row in enumerate(self.board[::-1])]

        rows = ['|' + '|'.join(row) + '|' for row in pieces]
        return '\n+------------------------------------+\n'.join(['', *rows, '']).strip('\n') \
               + f'\nCastling: {self.castling_state} ' \
                 f'\nEn passant: {coords_to_cell(*self.en_passant) if self.en_passant else None}' \
                 f'\nMovement: {self.move_color}'

    def is_any_movement_possible(self):
        for piece in self.pieces:
            if piece.moves:
                return True

        return False

    def is_stalemate(self):
        state = self.get_state()
        any_movement_possible = self.is_any_movement_possible()

        if any_movement_possible:
            return False

        if not state.white_king_under_attack and self.move_color == Color.WHITE:
            return True

        if not state.black_king_under_attack and self.move_color == Color.BLACK:
            return True

        return False

    def is_checkmate(self):
        state = self.get_state()
        any_movement_possible = self.is_any_movement_possible()

        if any_movement_possible:
            return False

        if state.white_king_under_attack and self.move_color == Color.WHITE:
            return True

        if state.black_king_under_attack and self.move_color == Color.BLACK:
            return True

        return False

    def is_check(self):
        state = self.get_state()

        if state.white_king_under_attack and self.move_color == Color.WHITE:
            return True

        if state.black_king_under_attack and self.move_color == Color.BLACK:
            return True

        return False

    def get_possible_moves(self):
        result = []

        for piece in self.pieces:
            result.append({'type': piece.char_repr,
                           'x': piece.x,
                           'y': piece.y,
                           'moves': piece.moves[:]})

        return result


__all__ = ['ChessPosition', 'cell_to_coords', 'coords_to_cell']
