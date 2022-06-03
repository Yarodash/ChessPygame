from .ChessPiece import ChessPiece


class Rook(ChessPiece):
    """Class for Rook piece"""

    text = '♜♖'
    char = 'R'

    axis = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_possible_moves(self):
        """Rook can move any number of cells horizontally or vertically without jumping"""

        possible_moves = []

        for dx, dy in self.axis:
            for i in range(1, 8):
                new_x, new_y = self.x + i * dx, self.y + i * dy

                if not self.is_inside_board(new_x, new_y):  # New position must be inside chess board
                    break

                if self.board.is_empty_at(new_x, new_y):  # If cell is empty, we can continue moving by this axis
                    possible_moves.append((new_x, new_y))

                else:  # Cell is not empty, so we stop moving
                    if self.is_enemy_at(new_x, new_y):  # If cell containing enemy, then we can attack it
                        possible_moves.append((new_x, new_y))
                    break

        return possible_moves


__all__ = ['Rook']
