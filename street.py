import pygame
import random

class Street:

    """ Since the lightpoles are tightly related to the streets, both are treated inside of this class. """

    def __init__(self, street_sprite, lightpole_sprite, billboard_sprite, billboard_ads, SCREEN_WIDTH, scale):

        self.scale = scale
        self.SCREEN_WIDTH = SCREEN_WIDTH

        self.street_sprite = street_sprite
        self.lightpole_sprite = lightpole_sprite
        self.billboard_sprite = billboard_sprite

        self.street1 = street_sprite.get_rect(midleft=(0, self.SCREEN_WIDTH / 2.08))
        self.street2 = street_sprite.get_rect(midleft=(self.street1.midright))
        self.street3 = street_sprite.get_rect(midleft=(self.street2.midright))
        self.streets = [self.street1, self.street2, self.street3]

        self.lightpoles = []

        self.billboard_fade = 0.1

        self.billboard_rect = billboard_sprite.get_rect(midleft=(-9999, 90 * scale))

        self.billboard_sprite = billboard_sprite
        self.billboard_ads = billboard_ads
        self.billboard_ad_sprite = random.choice(list(self.billboard_ads.values()))
        self.billboard_ad_rect = self.billboard_ad_sprite.get_rect()
        self.billboard_ad_rect.topleft = (
            self.billboard_rect.x + 1.8 * self.scale,
            self.billboard_rect.y + 1.8 * self.scale
        )


        # Spacing refers to the spacing between each pole, while Y determines its Y position
        self.pole_spacing = 120 * self.scale
        y = self.street1.y - (35 * self.scale)

        # Start X at 0 then fill the screen with poles as needed
        x = 0
        while x < self.SCREEN_WIDTH * 3:
            rect = lightpole_sprite.get_rect(topleft=(x, y))
            self.lightpoles.append(rect)
            x += self.pole_spacing

    def street_movement(self, dt, speed):

        """ Move the street in the screen and reallocate it if it's not visible anymore. """

        movement_speed = 1.2

        for s in self.streets:
            s.x -= speed * movement_speed * dt

        # Lambda makes sure streets are being compared based on their .right property only
        for s in self.streets:
            if s.right <= 0:
                furthest_right = max(self.streets, key=lambda r: r.right)
                s.left = furthest_right.right

    def street_draw(self, screen):

        """ Draw the street on the screen. """

        for s in self.streets:
            screen.blit(self.street_sprite, s)



    def lightpole_movement(self, dt, speed):

        """ Move the street in the screen and reallocate it if it's not visible anymore """

        movement_speed = 1.2

        for pole in self.lightpoles:
            pole.x -= speed * movement_speed * dt

            if pole.right < 0:
                furthest = max(self.lightpoles, key=lambda p: p.right)
                pole.left = furthest.right + self.pole_spacing

    def lightpole_draw(self, screen):

        """ Draw the lightpole on the screen. """

        for pole in self.lightpoles:
            screen.blit(self.lightpole_sprite, pole)

    def billboard_movement(self, dt, speed, biome):

        """Move the billboard and respawn it only in city biome."""

        movement_speed = 0.9

        self.billboard_rect.x -= speed * movement_speed * dt
        self.billboard_ad_rect.x -= speed * movement_speed * dt

        if biome == "city":
            if self.billboard_rect.right < 0:
                self.billboard_ad_sprite = random.choice(list(self.billboard_ads.values()))
                self.billboard_rect.left = 500 * self.scale
                # Reset ad relative to billboard
                self.billboard_ad_rect.topleft = (
                    self.billboard_rect.x + 1.8 * self.scale,
                    self.billboard_rect.y + 1.8 * self.scale
                )

    def billboard_draw(self, screen, sky_color):

        """ Draw the billboard on the screen. """

        # Draw the main billboard frame
        screen.blit(self.billboard_sprite, self.billboard_rect)

        # Draw the ad using its own rect
        screen.blit(self.billboard_ad_sprite, self.billboard_ad_rect)







