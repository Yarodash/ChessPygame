from .ChessPiece import ChessPiece
from .Colors import Color


class Pawn(ChessPiece):
    """Class for Pawn piece"""

    text = '♟♙'
    char = 'P'

    def get_possible_moves(self):
        """Pawn can move 1 cell forward (or 2 cells at first move) and attack diagonally"""

        possible_moves = []

        if self.color == Color.WHITE:  # White pawn moves
            if self.y == 1:  # First white pawn move (starts from y = 1)
                if self.board.is_empty_at(self.x, 2):  # Move 1 step forward
                    possible_moves.append((self.x, 2))

                    if self.board.is_empty_at(self.x, 3):  # Move 2 steps forward
                        possible_moves.append((self.x, 3))

            else:  # Not first move
                if self.board.is_empty_at(self.x, self.y + 1):  # Move 1 step forward
                    possible_moves.append((self.x, self.y + 1))

            # Attack diagonally or En passant
            if self.is_enemy_at(self.x - 1, self.y + 1) or (self.x - 1, self.y + 1) == self.board.en_passant:
                possible_moves.append((self.x - 1, self.y + 1))

            # Attack diagonally or En passant
            if self.is_enemy_at(self.x + 1, self.y + 1) or (self.x + 1, self.y + 1) == self.board.en_passant:
                possible_moves.append((self.x + 1, self.y + 1))

        else:  # Black pawn moves
            if self.y == 6:  # First black pawn move (starts from y = 6)
                if self.board.is_empty_at(self.x, 5):  # Move 1 step forward
                    possible_moves.append((self.x, 5))

                    if self.board.is_empty_at(self.x, 4):  # Move 2 steps forward
                        possible_moves.append((self.x, 4))

            else:  # Not first move
                if self.board.is_empty_at(self.x, self.y - 1):  # Move 1 step forward
                    possible_moves.append((self.x, self.y - 1))

            # Attack diagonally or En passant
            if self.is_enemy_at(self.x - 1, self.y - 1) or (self.x - 1, self.y - 1) == self.board.en_passant:
                possible_moves.append((self.x - 1, self.y - 1))

            # Attack diagonally or En passant
            if self.is_enemy_at(self.x + 1, self.y - 1) or (self.x + 1, self.y - 1) == self.board.en_passant:
                possible_moves.append((self.x + 1, self.y - 1))

        return possible_moves

    def get_attack_moves(self):
        """The difference from the other pieces is that the Pawn can only attack diagonally"""

        attack_moves = []

        if self.color == Color.WHITE:  # White pawn attack moves
            attack_moves.append((self.x - 1, self.y + 1))
            attack_moves.append((self.x + 1, self.y + 1))

        else:  # Black pawn attack moves
            attack_moves.append((self.x - 1, self.y - 1))
            attack_moves.append((self.x + 1, self.y - 1))

        return attack_moves


__all__ = ['Pawn']
