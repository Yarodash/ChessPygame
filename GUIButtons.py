import pygame
import enum
import time


class TooltipPosition(enum.Enum):
    TOP = 0
    BOTTOM = 1

    @staticmethod
    def get_default():
        return TooltipPosition.TOP

    def __str__(self):
        return self.name


class ButtonGUI(pygame.Rect):
    """Class that describes button"""
    _tooltip_size_coefficient = 1.3
    _tooltip_width_coefficient = 2
    _full_hover_time = 0.35

    def __init__(self, x, y, width, height, command=lambda: None, **kwargs):
        super().__init__(x, y, width, height)
        self.command = command
        self.tooltip = kwargs.get("tooltip", "")
        self.tooltip_font = kwargs.get("tooltip_font", None)
        self.tooltip_position = kwargs.get("tooltip_position", TooltipPosition.get_default())
        self.hover_time = 0
        self.is_hovered = False
        self.activated = False

    def set_command(self, command):
        self.command = command

    def is_cursor_inside(self, x, y):
        return self.collidepoint(x, y)

    def press(self):
        self.command()

    def hover(self):
        if not self.is_hovered:
            self.hover_time = time.time()
        self.is_hovered = True

    def unhover(self):
        self.is_hovered = False

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def _draw(self, high_surface):
        pass

    @property
    def hover_percent(self):
        return min(1.0, (time.time() - self.hover_time) / self._full_hover_time)

    def draw_tooltip(self, high_surface):
        if (not self.is_hovered) or (self.tooltip_font is None) or (not self.tooltip):
            return

        text_surface = self.tooltip_font.render(self.tooltip, True, (200, 200, 200))

        added_size = (self._tooltip_size_coefficient - 1) * text_surface.get_height()
        background_width = text_surface.get_width() + self._tooltip_width_coefficient * added_size
        background_height = text_surface.get_height() + added_size

        text_background_surface = pygame.Surface((background_width, background_height), pygame.SRCALPHA)
        pygame.draw.rect(text_background_surface, (50, 50, 50), text_background_surface.get_rect(), border_radius=7)
        text_background_surface.blit(text_surface, text_surface.get_rect(center=text_background_surface.get_rect().center))

        if self.tooltip_position == TooltipPosition.BOTTOM:
            place = text_background_surface.get_rect(midtop=self.midbottom)
        else:
            place = text_background_surface.get_rect(midbottom=self.midtop)

        text_background_surface.set_alpha(int(self.hover_percent * 255))
        high_surface.blit(text_background_surface, place)

    def draw(self, high_surface):
        self._draw(high_surface)
        self.draw_tooltip(high_surface)


def make_hover_image(unhover_image, scale_factor=1.08, blackness=45):
    hover_image = pygame.Surface(unhover_image.get_size(), pygame.SRCALPHA).convert_alpha()
    hover_image.fill((0, 0, 0, blackness))

    w, h = hover_image.get_size()
    shift_factor = (scale_factor - 1) / 2

    scaled = pygame.transform.smoothscale(unhover_image, (w * scale_factor, h * scale_factor))
    hover_image.blit(scaled, (-w * shift_factor, -h * shift_factor))

    return hover_image


class ImageButtonGUI(ButtonGUI):
    """Class that describes button, that have images for unhovered and hovered states"""

    def __init__(self, x, y, width, height, unhover_image, hover_image, command=lambda: None, **kwargs):
        super().__init__(x, y, width, height, command, **kwargs)

        self.unhover_image = pygame.transform.smoothscale(unhover_image, (width, height))
        self.hover_image = pygame.transform.smoothscale(hover_image, (width, height))

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def _draw(self, high_surface):
        self.surface.fill((0, 0, 0, 0))

        if self.is_hovered:
            image_to_draw = make_hover_image(self.unhover_image, 1, int(45 * self.hover_percent ** 0.4))
        else:
            image_to_draw = self.unhover_image

        self.surface.blit(image_to_draw, (0, 0))
        high_surface.blit(self.surface, (self.x, self.y))


class ImagePreparedButtonGUI(ImageButtonGUI):
    """ImageButton class with prepared images"""

    unhover_image_src = ''

    def __init__(self, x, y, width, height, command=lambda: None, **kwargs):
        unhover_image = pygame.image.load(self.unhover_image_src).convert_alpha()
        hover_image = make_hover_image(unhover_image)

        super().__init__(x, y, width, height, unhover_image, hover_image, command, **kwargs)


class ImageRadioButtonGUI(ButtonGUI):
    """Class that describes button, that have images for unhovered, hovered and activated states"""

    def __init__(self, x, y, width, height, unhover_image, hover_image, activated_image, command=lambda: None,
                 **kwargs):
        super().__init__(x, y, width, height, command, **kwargs)

        self.unhover_image = pygame.transform.smoothscale(unhover_image, (width, height))
        self.hover_image = pygame.transform.smoothscale(hover_image, (width, height))
        self.activated_image = pygame.transform.smoothscale(activated_image, (width, height))

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def _draw(self, high_surface):
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

    def __init__(self, x, y, width, height, command=lambda: None, **kwargs):
        unhover_image = pygame.image.load(self.unhover_image_src).convert_alpha()
        hover_image = pygame.image.load(self.hover_image_src).convert_alpha()
        activated_image = pygame.image.load(self.activated_image_src).convert_alpha()

        super().__init__(x, y, width, height, unhover_image, hover_image, activated_image, command, **kwargs)


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

    def __init__(self, x, y, font, command=lambda: None, **kwargs):
        super().__init__(x, y, 1, 1, command, **kwargs)

        self.font = font
        self.fen = ''

    def set_fen(self, fen):
        self.fen = fen

    def _draw(self, high_surface):
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
           'FENCopyButtonGUI',
           'TooltipPosition']
