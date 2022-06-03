from .ChessPiece import ChessPiece


class Queen(ChessPiece):
    """Class for Queen piece"""

    text = '♛♕'
    char = 'Q'

    diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    axis = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_possible_moves(self):
        """Queen movement combines Rook and Bishop movements"""

        possible_moves = []

        for dx, dy in self.axis + self.diagonals:
            for i in range(1, 8):
                new_x, new_y = self.x + i * dx, self.y + i * dy

                if not self.is_inside_board(new_x, new_y):  # New position must be inside chess board
                    break

                if self.board.is_empty_at(new_x, new_y):  # If cell is empty, we can continue moving
                    possible_moves.append((new_x, new_y))

                else:  # Cell is not empty, so we stop moving
                    if self.is_enemy_at(new_x, new_y):  # If cell containing enemy, then we can attack it
                        possible_moves.append((new_x, new_y))
                    break

        return possible_moves


__all__ = ['Queen']
