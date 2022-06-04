import tkinter
from tkinter import simpledialog, messagebox

import pygame
import pyperclip

from ChessLogic import *
from GUIButtons import *
from SoundEffects import *


class ChessSprites:
    chess_pieces_sprite_destination = 'Sprites/chess_pieces_sprite.png'
    chess_pieces_coord = {'K': (0, 0), 'Q': (1, 0), 'B': (2, 0), 'N': (3, 0), 'R': (4, 0), 'P': (5, 0),
                          'k': (0, 1), 'q': (1, 1), 'b': (2, 1), 'n': (3, 1), 'r': (4, 1), 'p': (5, 1)}
    chess_piece_size = 426

    def __init__(self, scaled_chess_piece_size):
        origin = pygame.image.load(self.chess_pieces_sprite_destination).convert_alpha()
        self.chess_pieces_images = {chess_piece: self.cut_image(origin,
                                                                x * self.chess_piece_size, y * self.chess_piece_size,
                                                                self.chess_piece_size, self.chess_piece_size)
                                    for chess_piece, (x, y) in self.chess_pieces_coord.items()}
        self.scaled_chess_pieces_images = {}
        self.prepare(scaled_chess_piece_size)

    def prepare(self, size):
        self.scaled_chess_pieces_images = {chess_piece: self.resize(image, size / self.chess_piece_size)
                                           for chess_piece, image in self.chess_pieces_images.items()}

    def resize(self, image, coef):
        return pygame.transform.smoothscale(image, (round(image.get_width() * coef), round(image.get_height() * coef)))

    @staticmethod
    def cut_image(image, x, y, width, height):
        return image.subsurface((x, y, width, height))

    def get_image(self, piece):
        return self.scaled_chess_pieces_images[piece]


class ChessPieceGUI(pygame.Rect):
    def __init__(self, chess_board, piece, moves, _x, _y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chess_board = chess_board
        self.piece = piece
        self.moves = moves
        self.piece_x = _x
        self.piece_y = _y

    def is_cursor_inside(self, x, y):
        return self.collidepoint(x, y)

    def draw(self, surface, attack_cell):
        if attack_cell is not None and attack_cell == (self.piece_x, self.piece_y):
            surface.blit(self.chess_board.KING_UNDER_ATTACK, (self.x, self.y))

        surface.blit(self.chess_board.sprites.get_image(self.piece), (self.x, self.y))

    def move_to(self, x, y):
        self.x, self.y = x, y


class ChessBoardGUI:
    WHITE_CELL_COLOR = (240, 217, 181)
    BLACK_CELL_COLOR = (181, 136, 99)

    def load_image(self, src, width=None, height=None):
        if width is None:
            width = self.chess_program.SQUARE

        if height is None:
            height = self.chess_program.SQUARE

        return pygame.transform.smoothscale(
            pygame.image.load(src),
            (width, height)
        )

    def __init__(self, chess_program):
        self.chess_program = chess_program
        self.sprites = ChessSprites(self.chess_program.SQUARE)

        self.WHITE_CELL_MOVE = self.load_image('Sprites/white_cell_movement.png')
        self.BLACK_CELL_MOVE = self.load_image('Sprites/black_cell_movement.png')
        self.WHITE_CELL_ATTACK = self.load_image('Sprites/white_cell_attack.png')
        self.BLACK_CELL_ATTACK = self.load_image('Sprites/black_cell_attack.png')
        self.KING_UNDER_ATTACK = self.load_image('Sprites/king_under_attack_aura.png')

        self.surface = pygame.Surface((chess_program.SQUARE * 8, chess_program.SQUARE * 8))
        self.pieces = []
        self.attack_cell = None

        self.selected_piece = None

    def is_piece_at(self, x, y):
        for piece in self.pieces:
            if (x, y) == (piece.piece_x, piece.piece_y):
                return True

        return False

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.surface,
                                 self.WHITE_CELL_COLOR if (i + j) % 2 else self.BLACK_CELL_COLOR,
                                 (i * self.chess_program.SQUARE, j * self.chess_program.SQUARE,
                                  self.chess_program.SQUARE, self.chess_program.SQUARE))

        if self.selected_piece:
            for x, y in self.selected_piece.moves:
                image = [self.WHITE_CELL_MOVE, self.BLACK_CELL_MOVE, self.WHITE_CELL_ATTACK, self.BLACK_CELL_ATTACK][
                    (x + y) % 2 + 2 * self.is_piece_at(x, y)]

                self.surface.blit(image, (x * self.chess_program.SQUARE, (7 - y) * self.chess_program.SQUARE))

    def press_mouse(self, x, y):
        for piece in self.pieces:
            if piece.is_cursor_inside(x, y) and piece.moves:
                self.selected_piece = piece

    def drag_mouse(self, x, y):
        if self.selected_piece:
            self.selected_piece.move_to(x - self.chess_program.SQUARE // 2, y - self.chess_program.SQUARE // 2)

    def release_mouse(self, x, y):
        if self.selected_piece:
            move_coord_x = x // self.chess_program.SQUARE
            move_coord_y = 7 - y // self.chess_program.SQUARE

            if (move_coord_x, move_coord_y) in self.selected_piece.moves:
                self.chess_program.make_move(self.selected_piece.piece_x,
                                             self.selected_piece.piece_y,
                                             move_coord_x,
                                             move_coord_y)
            else:
                self.selected_piece.move_to(self.selected_piece.piece_x * self.chess_program.SQUARE,
                                            (7 - self.selected_piece.piece_y) * self.chess_program.SQUARE)

        self.selected_piece = None

    def move_mouse(self, x, y):
        pass

    def update(self):
        pieces_info = self.chess_program.chess_game.get_possible_moves()

        self.pieces.clear()
        for piece_info in pieces_info:
            self.pieces.append(ChessPieceGUI(self,
                                             piece_info['type'],
                                             piece_info['moves'],
                                             piece_info['x'],
                                             piece_info['y'],
                                             piece_info['x'] * self.chess_program.SQUARE,
                                             (7 - piece_info['y']) * self.chess_program.SQUARE,
                                             self.chess_program.SQUARE,
                                             self.chess_program.SQUARE))

        game_state = self.chess_program.chess_game.current_chess_position.get_state()
        self.attack_cell = None

        if game_state.white_king_under_attack:
            for piece in self.pieces:
                if piece.piece == 'K':
                    self.attack_cell = (piece.piece_x, piece.piece_y)

        if game_state.black_king_under_attack:
            for piece in self.pieces:
                if piece.piece == 'k':
                    self.attack_cell = (piece.piece_x, piece.piece_y)

    def draw(self):
        self.draw_board()

        for piece in self.pieces:
            piece.draw(self.surface, self.attack_cell)

        if self.selected_piece:
            self.selected_piece.draw(self.surface, self.attack_cell)

        return self.surface


class ChessProgramGUI:
    SQUARE = 60
    WIDTH = 15.5 * SQUARE
    HEIGHT = 9.3 * SQUARE

    FPS = 60

    BACKGROUND_COLOR = (127, 127, 127)

    class QuitException(Exception):
        pass

    def __init__(self):
        self.chess_game = ChessGame.create_at_starting_position()

        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")

        self.font = pygame.font.SysFont('Courier New', int(self.SQUARE / 4.5))
        self.font_big = pygame.font.SysFont('Courier New', int(self.SQUARE / 2.2))
        self.font_tooltip = pygame.font.SysFont('Tahoma', int(self.SQUARE / 4.8))
        self.fen = ''

        self.sound_effects = SoundEffects()

        self.board = ChessBoardGUI(self)
        self.pieces = []
        self.is_board_choosed = False

        self.buttons = []
        self.fen_copy_button = None
        self.create_buttons()

        self.update()
        self.promotion = 'Q'

    def create_buttons(self):
        self.create_promotion_buttons()
        self.create_history_buttons()
        self.create_special_buttons()

    def set_promotion(self, new_promotion):
        self.promotion = new_promotion

    def create_promotion_buttons(self):
        queen_promotion_btn = QueenPromotionButton(self.SQUARE * 10, self.SQUARE * 2, self.SQUARE, self.SQUARE,
                                                   tooltip="Promote to Queen", tooltip_font=self.font_tooltip,
                                                   tooltip_position=TooltipPosition.BOTTOM)
        bishop_promotion_btn = BishopPromotionButton(self.SQUARE * 11, self.SQUARE * 2, self.SQUARE, self.SQUARE,
                                                     tooltip="Promote to Bishop", tooltip_font=self.font_tooltip,
                                                     tooltip_position=TooltipPosition.BOTTOM)
        knight_promotion_btn = KnightPromotionButton(self.SQUARE * 12, self.SQUARE * 2, self.SQUARE, self.SQUARE,
                                                     tooltip="Promote to Knight", tooltip_font=self.font_tooltip,
                                                     tooltip_position=TooltipPosition.BOTTOM)
        rook_promotion_btn = RookPromotionButton(self.SQUARE * 13, self.SQUARE * 2, self.SQUARE, self.SQUARE,
                                                 tooltip="Promote to Rook", tooltip_font=self.font_tooltip,
                                                 tooltip_position=TooltipPosition.BOTTOM)
        queen_promotion_btn.activate()

        queen_promotion_btn.set_command(lambda: (queen_promotion_btn.activate(),
                                                 bishop_promotion_btn.deactivate(),
                                                 knight_promotion_btn.deactivate(),
                                                 rook_promotion_btn.deactivate(),
                                                 self.set_promotion('Q')))

        bishop_promotion_btn.set_command(lambda: (bishop_promotion_btn.activate(),
                                                  queen_promotion_btn.deactivate(),
                                                  knight_promotion_btn.deactivate(),
                                                  rook_promotion_btn.deactivate(),
                                                  self.set_promotion('B')))

        knight_promotion_btn.set_command(lambda: (knight_promotion_btn.activate(),
                                                  bishop_promotion_btn.deactivate(),
                                                  queen_promotion_btn.deactivate(),
                                                  rook_promotion_btn.deactivate(),
                                                  self.set_promotion('N')))

        rook_promotion_btn.set_command(lambda: (rook_promotion_btn.activate(),
                                                bishop_promotion_btn.deactivate(),
                                                knight_promotion_btn.deactivate(),
                                                queen_promotion_btn.deactivate(),
                                                self.set_promotion('R')))

        self.buttons.append(queen_promotion_btn)
        self.buttons.append(bishop_promotion_btn)
        self.buttons.append(rook_promotion_btn)
        self.buttons.append(knight_promotion_btn)

    def create_history_buttons(self):
        full_backward_button = FullBackwardButton(self.SQUARE * 10, self.SQUARE * 5, self.SQUARE, self.SQUARE,
                                                  lambda: (self.chess_game.rewind(), self.update(),
                                                           self.sound_effects.move_sound.play()),
                                                  tooltip="Move to history start", tooltip_font=self.font_tooltip,
                                                  tooltip_position=TooltipPosition.TOP)

        skip_backward_button = SkipBackwardButton(self.SQUARE * 11, self.SQUARE * 5, self.SQUARE, self.SQUARE,
                                                  lambda: (self.chess_game.skip_backward(), self.update(),
                                                           self.sound_effects.move_sound.play()),
                                                  tooltip="Previous turn", tooltip_font=self.font_tooltip,
                                                  tooltip_position=TooltipPosition.TOP)

        skip_button = SkipButton(self.SQUARE * 12, self.SQUARE * 5, self.SQUARE, self.SQUARE,
                                 lambda: (self.chess_game.skip(), self.update(), self.sound_effects.move_sound.play()),
                                 tooltip="Next turn", tooltip_font=self.font_tooltip,
                                 tooltip_position=TooltipPosition.TOP)

        full_forward_button = FullForwardButton(self.SQUARE * 13, self.SQUARE * 5, self.SQUARE, self.SQUARE,
                                                lambda: (self.chess_game.fast_forward(), self.update(),
                                                         self.sound_effects.move_sound.play()), tooltip="Current turn",
                                                tooltip_font=self.font_tooltip, tooltip_position=TooltipPosition.TOP)

        self.buttons.append(full_backward_button)
        self.buttons.append(skip_backward_button)
        self.buttons.append(skip_button)
        self.buttons.append(full_forward_button)

    def create_special_buttons(self):
        restart_button = RestartButton(self.SQUARE * 10, self.SQUARE * 6, self.SQUARE, self.SQUARE,
                                       lambda: (
                                           self.chess_game.restart(), self.update(),
                                           self.sound_effects.move_sound.play()),
                                       tooltip="Restart game", tooltip_font=self.font_tooltip,
                                       tooltip_position=TooltipPosition.BOTTOM)
        self.buttons.append(restart_button)

        def import_fen_button_impl():
            root = tkinter.Tk()
            root.withdraw()
            answer = simpledialog.askstring("FEN", "Enter FEN:", parent=root)

            try:
                if answer is not None:
                    self.chess_game.restart_game(answer)
                    self.update()
                    self.sound_effects.move_sound.play()

            except Exception as e:
                root.destroy()
                raise e

            finally:
                root.destroy()

        import_fen_button = ImportFENButton(self.SQUARE * 11, self.SQUARE * 6, self.SQUARE, self.SQUARE,
                                            import_fen_button_impl, tooltip="Import FEN",
                                            tooltip_font=self.font_tooltip, tooltip_position=TooltipPosition.BOTTOM)
        self.buttons.append(import_fen_button)

        restart_initial_position_button = RestartInitialPositionButton(self.SQUARE * 12, self.SQUARE * 6,
                                                                       self.SQUARE, self.SQUARE,
                                                                       lambda: (
                                                                           self.chess_game.restart_game_with_starting_position(),
                                                                           self.update(),
                                                                           self.sound_effects.move_sound.play()),
                                                                       tooltip="Set to initial position",
                                                                       tooltip_font=self.font_tooltip,
                                                                       tooltip_position=TooltipPosition.BOTTOM)
        self.buttons.append(restart_initial_position_button)

        def copy_fen_to_clipboard():
            fen = self.chess_game.current_chess_position.generate_fen()
            pyperclip.copy(fen)

        self.fen_copy_button = FENCopyButtonGUI(self.SQUARE * 0.6, self.SQUARE * 8.7, self.font, copy_fen_to_clipboard,
                                                tooltip="Tap to copy", tooltip_font=self.font_tooltip,
                                                tooltip_position=TooltipPosition.BOTTOM)
        self.buttons.append(self.fen_copy_button)

        def exit_button_impl():
            raise self.QuitException

        exit_button = ExitButton(self.SQUARE * 13, self.SQUARE * 6, self.SQUARE, self.SQUARE, exit_button_impl,
                                 tooltip="Exit", tooltip_font=self.font_tooltip,
                                 tooltip_position=TooltipPosition.BOTTOM)
        self.buttons.append(exit_button)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.is_board_choosed:
                if event.buttons[0] == 0:
                    self.board.move_mouse(event.pos[0] - self.SQUARE // 2, event.pos[1] - self.SQUARE // 2)
                else:
                    self.board.drag_mouse(event.pos[0] - self.SQUARE // 2, event.pos[1] - self.SQUARE // 2)
            else:
                for button in self.buttons:
                    if button.is_cursor_inside(event.pos[0], event.pos[1]):
                        button.hover()
                    else:
                        button.unhover()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] - self.SQUARE // 2 <= self.SQUARE * 8 \
                    and 0 <= event.pos[1] - self.SQUARE // 2 <= self.SQUARE * 8:
                self.is_board_choosed = True
                self.board.press_mouse(event.pos[0] - self.SQUARE // 2, event.pos[1] - self.SQUARE // 2)
            else:
                for button in self.buttons:
                    if button.is_cursor_inside(event.pos[0], event.pos[1]):
                        button.press()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_board_choosed:
                self.is_board_choosed = False
                self.board.release_mouse(event.pos[0] - self.SQUARE // 2, event.pos[1] - self.SQUARE // 2)
            else:
                pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise self.QuitException

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self.handle_mouse_event(event)

    def play_sound(self, move_result):
        if move_result['is_piece_captured']:
            self.sound_effects.capture_sound.play()
        else:
            self.sound_effects.move_sound.play()

        if self.chess_game.current_chess_position.is_checkmate():
            self.sound_effects.victory_sound.play()
            return

        if self.chess_game.current_chess_position.is_stalemate():
            self.sound_effects.stalemate_sound.play()
            return

        if self.chess_game.current_chess_position.is_check():
            self.sound_effects.check_sound.play()

    def make_move(self, x, y, new_x, new_y):
        move_result = self.chess_game.make_move(x, y, new_x, new_y, self.promotion)
        self.play_sound(move_result)
        self.update()

    def update(self):
        pygame.display.set_caption(self.chess_game.get_title())
        self.board.update()
        self.fen_copy_button.set_fen(self.chess_game.current_chess_position.generate_fen())

    def draw_chessboard(self):
        pygame.draw.rect(self.screen, (110, 110, 110), (self.SQUARE * 0.4, self.SQUARE * 0.4,
                                                        self.SQUARE * 8.2, self.SQUARE * 8.2))
        board_surface = self.board.draw()
        self.screen.blit(board_surface, (self.SQUARE / 2, self.SQUARE / 2))

    def draw_gui(self):
        pygame.draw.rect(self.screen, (110, 110, 110), (self.SQUARE * 9.5, self.SQUARE * 1.25,
                                                        self.SQUARE * 5, self.SQUARE * 6.25))

        pygame.draw.rect(self.screen, (100, 100, 100), (self.SQUARE * 9.75, self.SQUARE * 1.5,
                                                        self.SQUARE * 4.5, self.SQUARE * 1.75))
        promotion_label = self.font.render('Promotion piece:', True, (0, 0, 0))
        self.screen.blit(promotion_label, (self.SQUARE * 10, self.SQUARE * 1.70))

        pygame.draw.rect(self.screen, (100, 100, 100), (self.SQUARE * 9.75, self.SQUARE * 4.75,
                                                        self.SQUARE * 4.5, self.SQUARE * 2.5))

        for button in self.buttons:
            button.draw(self.screen)

        if self.chess_game.current_chess_position.is_checkmate():
            if self.chess_game.current_chess_position.move_color == Color.BLACK:
                status = 'White won!'
            else:
                status = 'Black won!'

        elif self.chess_game.current_chess_position.is_stalemate():
            status = 'Stalemate'

        else:
            if self.chess_game.current_chess_position.move_color == Color.WHITE:
                status = 'Move for white'
            else:
                status = 'Move for black'

        status_label = self.font_big.render(status, True, (0, 0, 0))
        self.screen.blit(status_label, status_label.get_rect(center=(self.SQUARE * 12, self.SQUARE * 4)))

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)

        self.draw_gui()
        self.draw_chessboard()

    def mainloop(self):
        clock = pygame.time.Clock()

        while True:
            try:
                self.handle_events()
                self.draw()

            except self.QuitException as e:
                raise e

            except Exception as e:
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showerror('Error', 'Error with chess position occured.\nRestarting game...')
                root.destroy()

                self.chess_game.restart_game_with_starting_position()
                self.update()

            pygame.display.flip()
            clock.tick(self.FPS)

    def run(self):
        try:
            self.mainloop()
        except self.QuitException:
            pygame.quit()


__all__ = ['ChessProgramGUI']
