import pygame


class ButtonGUI(pygame.Rect):
    """Class that describes button"""

    def __init__(self, x, y, width, height, command=lambda: None):
        super().__init__(x, y, width, height)
        self.command = command
        self.is_hovered = False
        self.activated = False

    def set_command(self, command):
        self.command = command

    def is_cursor_inside(self, x, y):
        return self.collidepoint(x, y)

    def press(self):
        self.command()

    def hover(self):
        self.is_hovered = True

    def unhover(self):
        self.is_hovered = False

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def draw(self, high_surface):
        pass


class ImageButtonGUI(ButtonGUI):
    """Class that describes button, that have images for unhovered, hovered and activated states"""

    def __init__(self, x, y, width, height, unhover_image, hover_image, activated_image, command=lambda: None):
        super().__init__(x, y, width, height, command)

        self.unhover_image = pygame.transform.smoothscale(unhover_image, (width, height))
        self.hover_image = pygame.transform.smoothscale(hover_image, (width, height))
        self.activated_image = pygame.transform.smoothscale(activated_image, (width, height))

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw(self, high_surface):
        self.surface.fill((0, 0, 0, 0))

        if self.activated:
            image_to_draw = self.activated_image
        else:
            image_to_draw = self.hover_image if self.is_hovered else self.unhover_image

        self.surface.blit(image_to_draw, (0, 0))
        high_surface.blit(self.surface, (self.x, self.y))


class ImagePreparedButton(ImageButtonGUI):
    """ImageButton class with prepared images"""

    unhover_image_src = ''
    hover_image_src = ''
    activated_image_src = ''

    def __init__(self, x, y, width, height, command=lambda: None):
        unhover_image = pygame.image.load(self.unhover_image_src).convert_alpha()
        hover_image = pygame.image.load(self.hover_image_src).convert_alpha()
        activated_image = pygame.image.load(self.activated_image_src).convert_alpha()

        super().__init__(x, y, width, height, unhover_image, hover_image, activated_image, command)


class QueenPromotionButton(ImagePreparedButton):
    """Button class for queen promotion"""

    unhover_image_src = 'Sprites/QueenPromotionButton/unhover.png'
    hover_image_src = 'Sprites/QueenPromotionButton/hover.png'
    activated_image_src = 'Sprites/QueenPromotionButton/activated.png'


class BishopPromotionButton(ImagePreparedButton):
    """Button class for bishop promotion"""

    unhover_image_src = 'Sprites/BishopPromotionButton/unhover.png'
    hover_image_src = 'Sprites/BishopPromotionButton/hover.png'
    activated_image_src = 'Sprites/BishopPromotionButton/activated.png'


class KnightPromotionButton(ImagePreparedButton):
    """Button class for knight promotion"""

    unhover_image_src = 'Sprites/KnightPromotionButton/unhover.png'
    hover_image_src = 'Sprites/KnightPromotionButton/hover.png'
    activated_image_src = 'Sprites/KnightPromotionButton/activated.png'


class RookPromotionButton(ImagePreparedButton):
    """Button class for rook promotion"""

    unhover_image_src = 'Sprites/RookPromotionButton/unhover.png'
    hover_image_src = 'Sprites/RookPromotionButton/hover.png'
    activated_image_src = 'Sprites/RookPromotionButton/activated.png'


class FullBackwardButton(ImagePreparedButton):
    """Button class for rewinding chess history (full backward)"""

    unhover_image_src = 'Sprites/FullBackwardButton/unhover.png'
    hover_image_src = 'Sprites/FullBackwardButton/hover.png'
    activated_image_src = 'Sprites/FullBackwardButton/hover.png'


class FullForwardButton(ImagePreparedButton):
    """Button class for rewinding chess history (full forward)"""

    unhover_image_src = 'Sprites/FullForwardButton/unhover.png'
    hover_image_src = 'Sprites/FullForwardButton/hover.png'
    activated_image_src = 'Sprites/FullForwardButton/hover.png'


class SkipBackwardButton(ImagePreparedButton):
    """Button class for rewinding chess history (one step back)"""

    unhover_image_src = 'Sprites/SkipBackButton/unhover.png'
    hover_image_src = 'Sprites/SkipBackButton/hover.png'
    activated_image_src = 'Sprites/SkipBackButton/hover.png'


class SkipButton(ImagePreparedButton):
    """Button class for rewinding chess history (one step forward)"""

    unhover_image_src = 'Sprites/SkipButton/unhover.png'
    hover_image_src = 'Sprites/SkipButton/hover.png'
    activated_image_src = 'Sprites/SkipButton/hover.png'


class RestartButton(ImagePreparedButton):
    """Button class for restarting the game"""

    unhover_image_src = 'Sprites/RestartButton/unhover.png'
    hover_image_src = 'Sprites/RestartButton/hover.png'
    activated_image_src = 'Sprites/RestartButton/hover.png'


class ImportFENButton(ImagePreparedButton):
    """Button class for restarting game with custom position"""

    unhover_image_src = 'Sprites/ImportFENButton/unhover.png'
    hover_image_src = 'Sprites/ImportFENButton/hover.png'
    activated_image_src = 'Sprites/ImportFENButton/hover.png'


class RestartInitialPositionButton(ImagePreparedButton):
    """Button class for restarting the initial position of game"""

    unhover_image_src = 'Sprites/RestartInitialPositionButton/unhover.png'
    hover_image_src = 'Sprites/RestartInitialPositionButton/hover.png'
    activated_image_src = 'Sprites/RestartInitialPositionButton/hover.png'


class FENCopyButtonGUI(ButtonGUI):
    """Button class for restarting the game"""

    def __init__(self, x, y, font, command=lambda: None):
        super().__init__(x, y, 1, 1, command)

        self.font = font
        self.fen = ''

    def set_fen(self, fen):
        self.fen = fen

    def draw(self, high_surface):
        text_surface = self.font.render('FEN: ' + self.fen, True, (0, 0, 0))

        self.width, self.height = text_surface.get_size()

        text_background_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        text_background_surface.fill((0, 0, 0, 50) if self.is_hovered else (0, 0, 0, 30))

        high_surface.blit(text_background_surface, (self.x, self.y))
        high_surface.blit(text_surface, (self.x, self.y))


__all__ = ['QueenPromotionButton',
           'BishopPromotionButton',
           'KnightPromotionButton',
           'RookPromotionButton',
           'FullBackwardButton',
           'SkipBackwardButton',
           'SkipButton',
           'FullForwardButton',
           'RestartButton',
           'ImportFENButton',
           'RestartInitialPositionButton',
           'FENCopyButtonGUI']
