from .ChessPiece import ChessPiece
from .Colors import Color


class King(ChessPiece):
    """Class for King piece"""

    text = '♚♔'
    char = 'K'

    diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    axis = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_possible_moves(self):
        """King can move 1 cell in any direction"""

        possible_moves = []

        for dx, dy in self.axis + self.diagonals:
            new_x, new_y = self.x + dx, self.y + dy

            if not self.is_inside_board(new_x, new_y):  # New position must be inside chess board
                continue

            if self.board.is_empty_at(new_x, new_y) or self.is_enemy_at(new_x, new_y):  # Cell is empty or contain enemy
                possible_moves.append((new_x, new_y))

        return possible_moves

    def calculate_valid_moves(self):
        """The difference between king and other pieces is that king can do castling move"""
        super().calculate_valid_moves()

        # King must stay at position for castling
        if self.color == Color.WHITE and self.position != (4, 0):
            return

        if self.color == Color.BLACK and self.position != (4, 7):
            return

        game_state = self.board.get_state()

        # King while castling cannot be under attack
        if self.color == Color.WHITE and game_state.white_king_under_attack:
            return

        if self.color == Color.BLACK and game_state.black_king_under_attack:
            return

        if self.color == Color.WHITE:  # White castling
            # Castling at king side
            if self.board.castling_state.white_king_side:
                # No pieces must be between king and rook
                if self.board.is_empty_at(5, 0) and self.board.is_empty_at(6, 0):
                    # Check that king is not under attack while castling
                    if (5, 0) not in game_state.black_attack and (6, 0) not in game_state.black_attack:
                        self.moves.append((6, 0))

            # Castling at queen side
            if self.board.castling_state.white_queen_side:
                # No pieces must be between king and rook
                if self.board.is_empty_at(3, 0) and self.board.is_empty_at(2, 0) and self.board.is_empty_at(1, 0):
                    # Check that king is not under attack while castling
                    if (3, 0) not in game_state.black_attack and (2, 0) not in game_state.black_attack:
                        self.moves.append((2, 0))

        else:  # Black castling
            # Castling at king side
            if self.board.castling_state.black_king_side:
                # No pieces must be between king and rook
                if self.board.is_empty_at(5, 7) and self.board.is_empty_at(6, 7):
                    # Check that king is not under attack while castling
                    if (5, 7) not in game_state.white_attack and (6, 7) not in game_state.white_attack:
                        self.moves.append((6, 7))

            # Castling at queen side
            if self.board.castling_state.black_queen_side:
                # No pieces must be between king and rook
                if self.board.is_empty_at(3, 7) and self.board.is_empty_at(2, 7) and self.board.is_empty_at(1, 7):
                    # Check that king is not under attack while castling
                    if (3, 7) not in game_state.white_attack and (2, 7) not in game_state.white_attack:
                        self.moves.append((2, 7))


__all__ = ['King']
