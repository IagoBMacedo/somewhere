import pygame
import random

from utils import Colors

class Terrain:
    def __init__(self, scale, SCREEN_WIDTH, SCREEN_HEIGHT):

        """Initialize procedural terrain with multiple chunks and pre-drawn surfaces for performance."""

        self.scale = scale
        self.movement_speed = 0.02 * self.scale

        # Colors are taken from utils.py
        self.grass_color = Colors.MOUNTAINS_COLORS["green"]
        self.mountain_color = Colors.MOUNTAINS_COLORS["brown"]

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # Tile size takes into account scale, and tiles per chunk is used to define how many tiles fill the screen width
        self.tile_size = 1 * self.scale
        self.tiles_per_chunk = self.SCREEN_WIDTH // self.tile_size
        self.size = (self.tile_size, self.tile_size)

        # This ensures that when the next chunk is generated, it starts at the height where the previous chunk ended
        self.last_y = self.SCREEN_HEIGHT // 2

        # The overlay is used to apply a color filter later on
        self.overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)

        self.chunks = []  # List of rectangles representing positions of terrain chunks on screen
        self.chunk_surfaces = []  # List of surfaces containing the pre-drawn terrain for each chunk

        for i in range(2):
            chunk_rect = pygame.Rect(i * SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.chunks.append(chunk_rect)
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            self.last_y = self.generate_chunk(surface)
            self.chunk_surfaces.append(surface)


    def generate_chunk(self, surface):

        ''' When generating a new chunk, we start at the exact height where the last one ended to keep the path continuous.
        Each step, we move X to the right of the previous tile while the Y axis randomly climbs, drops, or stays level.
        Finally, we fill everything below that point to the bottom of the screen to create solid ground '''

        x = 0
        y = self.last_y

        while x < self.SCREEN_WIDTH:

            tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
            pygame.draw.rect(surface, self.grass_color, tile_rect)
            previous_rect = tile_rect

            fill_rect = pygame.Rect(x, tile_rect.bottom, self.tile_size, self.SCREEN_HEIGHT - (y + self.tile_size))
            pygame.draw.rect(surface, self.mountain_color, fill_rect)

            x = previous_rect.right
            y += random.randint(-1, 1) * self.scale
            y = max(20 * self.scale, min(y, self.SCREEN_HEIGHT - self.tile_size - (50 * self.scale)))

        return y


    def terrain_loop(self):

        '''The loop deals with movement by forcing X offset by movement speed for each chunk,
        it also makes sure the chunk that goes too far to the left is always recycled to the right with new data'''

        for i, chunk in enumerate(self.chunks):

            if chunk.right < 0:
                furthest_right = max(self.chunks, key=lambda r: r.right)
                chunk.left = furthest_right.right

                self.chunk_surfaces[i] = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
                self.last_y = self.generate_chunk(self.chunk_surfaces[i])



    def terrain_draw(self, surface, sky_color):

        '''Here we are making sure the second chunk is always exactly at the right of the left chunk'''

        # update overlay color
        self.overlay.fill((*sky_color, 100))

        for i, chunk in enumerate(self.chunks):
            # draw terrain chunk
            surface.blit(self.chunk_surfaces[i], (chunk.x, chunk.y))

            # draw overlay on that chunk
            surface.blit(self.overlay, (chunk.x, chunk.y))

    def terrain_movement(self, dt, speed):

        '''Moves the terrain as the player drives'''

        for i, chunk in enumerate(self.chunks):
            chunk.x -= (speed * self.movement_speed * dt)