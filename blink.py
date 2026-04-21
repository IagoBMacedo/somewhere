import pygame
import math

class Blink:
    def __init__(self):

        """Handles eye blinking logic for characters, including timing and offsets."""

        self.blink_interval = 3000
        self.blink_duration = 150
        self.blink_last = pygame.time.get_ticks()
        self.blinking = False
        self.blink_offset = 0
        self.blink_start = 0
        self.extra_eye_offsetx = 0
        self.extra_eye_offsety = 0

    def update_blink(self, now, scale):

        """ Update the blinking state. If it's time to blink, this function calls it! """

        if not self.blinking and now - self.blink_last >= self.blink_interval:
            self.blinking = True
            self.blink_start = now

        if self.blinking:
            elapsed = now - self.blink_start
            t = min(1.0, elapsed / self.blink_duration)

            self.blink_offset = round(math.sin(t * math.pi) * scale)

            if elapsed >= self.blink_duration:
                self.blinking = False
                self.blink_last = now
                self.blink_offset = 0
        else:
            self.blink_offset = 0

    def get_eye_draw_rect(self, driver_rect, eye_base_offset,
                          b_offset=None,
                          current_frame=None,
                          extra_eye_offsetx=0,
                          extra_eye_offsety=0,
                          scale=1):

        """
        Find out where the blinking animation should take place
        Since animation might vary eye Y and X, this function also takes into account the offsets needed.
        """

        # Use internal blink offset if none provided
        if b_offset is None:
            b_offset = self.blink_offset

        x = round(driver_rect.x + (eye_base_offset[0] + extra_eye_offsetx) * scale)
        y = round(driver_rect.y + (eye_base_offset[1] + extra_eye_offsety) * scale + b_offset)

        width = round(2 * scale)
        height = round(2 * scale)

        return pygame.Rect(x, y, width, height)
