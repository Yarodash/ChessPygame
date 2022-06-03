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


def make_hover_image(unhover_image, scale_factor=1.08):
    hover_image = pygame.Surface(unhover_image.get_size(), pygame.SRCALPHA).convert_alpha()
    hover_image.fill((0, 0, 0, 45))

    w, h = hover_image.get_size()
    shift_factor = (scale_factor - 1) / 2

    scaled = pygame.transform.smoothscale(unhover_image, (w * scale_factor, h * scale_factor))
    hover_image.blit(scaled, (-w * shift_factor, -h * shift_factor))

    return hover_image


class ImageButtonGUI(ButtonGUI):
    """Class that describes button, that have images for unhovered and hovered states"""

    def __init__(self, x, y, width, height, unhover_image, hover_image, command=lambda: None):
        super().__init__(x, y, width, height, command)

        self.unhover_image = pygame.transform.smoothscale(unhover_image, (width, height))
        self.hover_image = pygame.transform.smoothscale(hover_image, (width, height))

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw(self, high_surface):
        self.surface.fill((0, 0, 0, 0))

        image_to_draw = self.hover_image if self.is_hovered else self.unhover_image

        self.surface.blit(image_to_draw, (0, 0))
        high_surface.blit(self.surface, (self.x, self.y))


class ImagePreparedButtonGUI(ImageButtonGUI):
    """ImageButton class with prepared images"""

    unhover_image_src = ''

    def __init__(self, x, y, width, height, command=lambda: None):
        unhover_image = pygame.image.load(self.unhover_image_src).convert_alpha()
        hover_image = make_hover_image(unhover_image)

        super().__init__(x, y, width, height, unhover_image, hover_image, command)


class ImageRadioButtonGUI(ButtonGUI):
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


class ImagePreparedRadioButtonGUI(ImageRadioButtonGUI):
    """ImageRadioButton class with prepared images"""

    unhover_image_src = ''
    hover_image_src = ''
    activated_image_src = ''

    def __init__(self, x, y, width, height, command=lambda: None):
        unhover_image = pygame.image.load(self.unhover_image_src).convert_alpha()
        hover_image = pygame.image.load(self.hover_image_src).convert_alpha()
        activated_image = pygame.image.load(self.activated_image_src).convert_alpha()

        super().__init__(x, y, width, height, unhover_image, hover_image, activated_image, command)


class QueenPromotionButton(ImagePreparedRadioButtonGUI):
    """Button class for queen promotion"""

    unhover_image_src = 'Sprites/ButtonSprites/Promotion/QueenPromotion/unhover.png'
    hover_image_src = 'Sprites/ButtonSprites/Promotion/QueenPromotion/hover.png'
    activated_image_src = 'Sprites/ButtonSprites/Promotion/QueenPromotion/activated.png'


class BishopPromotionButton(ImagePreparedRadioButtonGUI):
    """Button class for bishop promotion"""

    unhover_image_src = 'Sprites/ButtonSprites/Promotion/BishopPromotion/unhover.png'
    hover_image_src = 'Sprites/ButtonSprites/Promotion/BishopPromotion/hover.png'
    activated_image_src = 'Sprites/ButtonSprites/Promotion/BishopPromotion/activated.png'


class KnightPromotionButton(ImagePreparedRadioButtonGUI):
    """Button class for knight promotion"""

    unhover_image_src = 'Sprites/ButtonSprites/Promotion/KnightPromotion/unhover.png'
    hover_image_src = 'Sprites/ButtonSprites/Promotion/KnightPromotion/hover.png'
    activated_image_src = 'Sprites/ButtonSprites/Promotion/KnightPromotion/activated.png'


class RookPromotionButton(ImagePreparedRadioButtonGUI):
    """Button class for rook promotion"""

    unhover_image_src = 'Sprites/ButtonSprites/Promotion/RookPromotion/unhover.png'
    hover_image_src = 'Sprites/ButtonSprites/Promotion/RookPromotion/hover.png'
    activated_image_src = 'Sprites/ButtonSprites/Promotion/RookPromotion/activated.png'


class FullBackwardButton(ImagePreparedButtonGUI):
    """Button class for rewinding chess history (full backward)"""

    unhover_image_src = 'Sprites/ButtonSprites/full_backward.png'


class FullForwardButton(ImagePreparedButtonGUI):
    """Button class for rewinding chess history (full forward)"""

    unhover_image_src = 'Sprites/ButtonSprites/full_forward.png'


class SkipBackwardButton(ImagePreparedButtonGUI):
    """Button class for rewinding chess history (one step back)"""

    unhover_image_src = 'Sprites/ButtonSprites/skip_back.png'


class SkipButton(ImagePreparedButtonGUI):
    """Button class for rewinding chess history (one step forward)"""

    unhover_image_src = 'Sprites/ButtonSprites/skip.png'


class RestartButton(ImagePreparedButtonGUI):
    """Button class for restarting the game"""

    unhover_image_src = 'Sprites/ButtonSprites/restart.png'


class ImportFENButton(ImagePreparedButtonGUI):
    """Button class for restarting game with custom position"""

    unhover_image_src = 'Sprites/ButtonSprites/import_fen.png'


class RestartInitialPositionButton(ImagePreparedButtonGUI):
    """Button class for restarting the initial position of game"""

    unhover_image_src = 'Sprites/ButtonSprites/full_restart.png'


class ExitButton(ImagePreparedButtonGUI):
    """Button class for exiting"""

    unhover_image_src = 'Sprites/ButtonSprites/exit.png'


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
           'ExitButton',
           'FENCopyButtonGUI']
