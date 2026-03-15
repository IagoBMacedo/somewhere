import pygame
import random
from utils import Colors

class Building:
    def __init__(self, windows_in_x, windows_in_y, x, scale, color_fade, SCREEN_HEIGHT):

        """
        Initialize a building with procedural windows and optional fade overlay.

        windows_in_x, windows_in_y: number of windows horizontally/vertically
        x: starting X position
        scale: scaling factor for windows
        color_fade: opacity multiplier for fog effect (0–1)
        SCREEN_HEIGHT: total screen height for ground alignment
        """

        self.scale = scale

        # Window related stuff
        self.window_w = 24 * self.scale
        self.window_h = 24 * self.scale
        self.spacing_x = 6 * self.scale
        self.spacing_y = 10 * self.scale
        self.margin = 6 * self.scale
        self.windows_in_x = windows_in_x
        self.windows_in_y = windows_in_y

        # Self.gap is used in the game loop within "cumulative_x", in order to make buildings have an empty space between each other
        self.gap = int(random.triangular(15, 200, 50) * scale)

        self.movement_speed = 0.4 * self.scale

        # Building width and height totally rely on window generation, not the other way around
        self.building_width = (
                self.margin * 2 +
                self.windows_in_x * self.window_w +
                (self.windows_in_x - 1) * self.spacing_x)

        self.building_height = (
                self.margin * 2 +
                self.windows_in_y * self.window_h +
                (self.windows_in_y - 1) * self.spacing_y)

        self.x = x
        self.ground_y = SCREEN_HEIGHT - 140

        # Since it's procedural, all colors derive from utils.py
        self.body_color = Colors.BUILDING_COLOR
        self.window_color = list(Colors.WINDOW_COLORS.values())

        # The overlay is created to apply the fade effect later
        self.color_fade = color_fade
        self.overlay = pygame.Surface((self.building_width, self.building_height), pygame.SRCALPHA)

        # Here we draw the building body
        self.image = pygame.Surface((self.building_width, self.building_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.body_color, (0, 0, self.building_width, self.building_height))

        # Here we draw the windows
        for r in range(self.windows_in_y):
            for c in range(self.windows_in_x):
                wx = self.margin + c * (self.window_w + self.spacing_x)
                wy = self.margin + r * (self.window_h + self.spacing_y)

                color = self.window_color[round(random.triangular(0, 4, 0))]
                pygame.draw.rect(self.image, color, (wx, wy, self.window_w, self.window_h))

    def building_draw(self, surface, sky_color):

        """ Draw the building on the surface and apply the overlay color in order to create a foggy effect. """

        pos = (self.x, self.ground_y - self.building_height)

        surface.blit(self.image, pos)

        # Update overlay color dynamically
        self.overlay.fill((*sky_color, round(self.color_fade * 255)))

        surface.blit(self.overlay, pos)

    def building_movement(self, dt, speed):

        """ Update the X coordinate of the buildings based on the car speed """

        if speed > 0:
            self.x -= (speed * self.movement_speed * dt)

