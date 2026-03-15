import pygame

class Fader:
    def __init__(self, size, color=(0, 0, 0)):
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.alpha = 255  # Start fully opaque (black)

    def update(self, dt, duration, target=0):

        """ Decreases alpha until it hits 0, or increases it until it hits 255 """

        rate = 255 / duration

        if self.alpha < target:
            self.alpha = min(target, self.alpha + rate * dt)
        elif self.alpha > target:
            self.alpha = max(target, self.alpha - rate * dt)

        self.surface.set_alpha(int(self.alpha))

    def draw(self, screen):

        """ Blits the surface if it's still visible """

        if self.alpha > 0:
            screen.blit(self.surface, (0, 0))

# class Ending:
#     This was used for the CS50 video.
#     def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
#
#         self.font = pygame.font.Font('freesansbold.ttf', 30)
#
#         self.final_text2 = self.font.render("This is CS50.", True, (255, 255, 255))
#         self.final_text2_rect = self.final_text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
#
#
#     def draw(self, screen):
#         screen.blit(self.final_text2, self.final_text2_rect)


def color_change(color1, color2, speed):

    """ Make transitions between two colors nice and smooth. """

    step = max(0.05, speed / 800)

    def inc(c1, c2):
        if c1 < c2:
            return min(c1 + step, c2)
        elif c1 > c2:
            return max(c1 - step, c2)
        return c1

    return [int(inc(c1, c2)) for c1, c2 in zip(color1, color2)]

class Colors:

    """ These are all the colors used in world generation, sprite colors are not stored in this class. """

    SKY_COLORS = {
        'light_yellow': (225, 235, 143),
        'dark_blue': (31, 100, 150),
    }

    MOUNTAINS_COLORS = {
    "green": (102, 168, 127),
    "brown": (90, 84, 109)
    }

    BUILDING_COLOR = (51, 26, 44)

    WINDOW_COLORS = {
        "dark_purple": (51, 22, 93),
        "medium_purple": (51, 22, 138),
        "bright_purple": (51, 22, 187),
        "yellow": (255, 200, 50),
        "yellow2": (255, 200, 50),
    }

    NPC_SHOES_COLORS = {
        'brown' : (73, 44, 39),
        'red' : (102, 55, 55),
        'black' : (21, 21, 27)
    }

    NPC_SKIN_COLORS = {
        'white': (238, 195, 154),
        'honey': (215, 160, 115),
        'olive': (186, 145, 102),
        'black': (107, 77, 73),
    }

    NPC_HAIR_COLORS = {
        'black': (21, 21, 28),
        'brown': (64, 29, 29),
        'blond': (171, 150, 87),
        'white': (191, 190, 186)
    }

    MOUNTAIN_NPC_JACKET_COLORS = {
        'forest_green': (70, 92, 58),
        'olive': (116, 125, 66),
        'dark_brown': (92, 65, 50),
        'tan': (146, 120, 85),
        'navy': (35, 42, 80),
        'slate': (80, 88, 96),
        'dusty_red': (125, 70, 60),
    }

    MOUNTAIN_NPC_PANTS_COLORS = {
        'blue' : (64, 59, 117),
        'black' : (21, 21, 21)
    }

    MOUNTAIN_NPC_DETAIL_COLORS = {
        'cream': (220, 210, 180),
        'light_green': (150, 180, 110),
        'light_blue': (120, 150, 200),
        'mustard': (210, 180, 90),
        'rust': (180, 95, 70)
    }

    CITY_NPC_CLOTHES_COLORS = {
        'black' : (25, 25, 33),
        'gray' : (50, 50, 77),
        'brown' : (73, 41, 38)
    }

    CITY_NPC_DETAIL_COLORS = {
        'red' : (172, 50, 50),
        'blue' : (61, 54, 172)
    }


