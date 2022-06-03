from .Colors import Color
from .ChessPosition import *


class ChessGame:
    """Class that describes single chess game"""

    initial_chess_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    def __init__(self, fen):
        self.initial_position = fen
        self.history = []
        self.index = 0

        self.restart_game()

    def restart_game(self, fen=None):
        if fen:
            self.initial_position = fen

        self.history = []
        self.index = 0

        self.history.append(ChessPosition.generate_from_fen(self.initial_position))
        self.history[-1].calculate_possible_moves()

    def restart_game_with_starting_position(self):
        self.restart_game(self.initial_chess_position)

    @classmethod
    def create_at_starting_position(cls):
        return cls(cls.initial_chess_position)

    @property
    def current_chess_position(self):
        return self.history[self.index]

    def make_move(self, x, y, new_x, new_y, promotion=None):
        self.history = self.history[: self.index + 1]
        new_chess_position = self.history[-1].copy()
        move_result = new_chess_position.make_move(x, y, new_x, new_y, promotion)
        new_chess_position.calculate_possible_moves()
        self.history.append(new_chess_position)
        self.index += 1

        return move_result

    def rewind(self):
        self.index = 0

    def skip_backward(self):
        self.index = max(0, self.index - 1)

    def skip(self):
        self.index = min(len(self.history) - 1, self.index + 1)

    def fast_forward(self):
        self.index = len(self.history) - 1

    def restart(self):
        self.restart_game()

    def get_possible_moves(self):
        return self.current_chess_position.get_possible_moves()

    def get_title(self):
        title = 'Chess'
        title += ' | Move Turn: ' + ('White' if self.current_chess_position.move_color == Color.WHITE else 'Black')

        if self.current_chess_position.is_stalemate():
            title += ' | Draw by stalemate'
            return title

        if self.current_chess_position.is_checkmate():
            title += f' | {"Black" if self.current_chess_position.move_color == Color.WHITE else "White"} won'
            return title

        game_state = self.current_chess_position.get_state()
        if game_state.white_king_under_attack or game_state.black_king_under_attack:
            title += ' | King under attack!'

        if self.index != len(self.history) - 1:
            title += f' | Watching game history {self.index + 1}/{len(self.history)}'

        return title


__all__ = ['ChessGame']
