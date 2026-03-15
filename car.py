import pygame
import math

class Car:

    def __init__(self, sprites, x, y, scale):

        """
        Initialize a car with sprites, position, and scale.

        sprites: dict containing 'body', 'wheel', 'driver', 'front_light', 'back_light'
        x, y: initial center position of the car
        scale: scaling factor for offsets and sizes
        """

        self.sprites = sprites
        self.scale = scale

        self.car_offsets = {
            'body': (0, 0),
            'light': (24.5, 2),
            'backlight': (-25.5, 2),
            'wheel_l': (-18, 7.5),
            'wheel_r': (13, 7.5),
            'driver': [-2, -4]
        }

        self.rect = self.sprites['body'].get_rect(center=(x, y))
        self.driver_x = self.rect.centerx + self.car_offsets['driver'][0] * scale
        self.driver_y = self.rect.centery + self.car_offsets['driver'][1] * scale

        # This is basically the anchor so the car doesn't accumulate incorrectly due to jiggle
        self.y_home = float(y)

        self.left_inset = 6 * scale
        self.right_inset = 10 * scale
        self.bottom_inset = 1.3 * scale

        # Collision rect is mainly created so the character doesn't go through the car!
        self.collision_rect = pygame.Rect(
            self.rect.left + self.left_inset,
            self.rect.bottom + self.bottom_inset,
            self.rect.width - self.right_inset,
            (2 * scale))

        self.collision_rect.midbottom = (
            self.rect.centerx,
            self.rect.bottom + self.bottom_inset
        )

        self.DRIVER_EYE_OFFSET = [10, 4]

        # Movement settings
        self.speed = 0
        self.car_on = False
        self.distance = 0

        # Wheel settings
        self.wheel_angle = 0
        self.rotated_wheel = self.sprites['wheel']

        # Jiggle settings
        self.start_jiggle_speed = 0
        self.start_jiggle_intensity = 0

        # Light settings
        self.front_light_fade_rate = 30
        self.back_light_fade_rate = 30
        self.front_light_on = False
        self.front_light_alpha = 0
        self.back_light_on = False
        self.back_light_alpha = 0

    def handle_movement(self, keys, CONTROLS, dt, streets):

        """ Move the car forward and adjust its vertical position only if it's within the allowed street limits. """

        car_y_movement = 0

        # Accelerate forward
        if keys[CONTROLS["forward"]] and self.car_on:
            if self.speed < 800:
                self.speed += 120 * dt

            # Vertical control (predictive, only moves if within street limits)
            if keys[CONTROLS["up"]]:
                max_up = streets.streets[0].top + (8 * self.scale)
                if self.y_home >= max_up:
                    car_y_movement -= (self.speed * dt) / 2

            if keys[CONTROLS["down"]]:
                max_down = streets.streets[0].bottom - (33 * self.scale)
                if self.y_home <= max_down:
                    car_y_movement += (self.speed * dt) / 2

        else:
            # Natural deceleration
            self.speed *= math.pow(0.5, dt)
            if abs(self.speed) < 10:
                self.speed = 0

        # Backward/brake, the back light only turns on if the speed is not zero
        if keys[CONTROLS["backward"]] and self.car_on and self.speed > 0:
            self.back_light_on = True
            self.speed *= math.pow(0.1, dt)

        else:
            self.back_light_on = False

        self.update_position(car_y_movement)

    def update_position(self, y_movement):

        """ Apply vertical movement to car, update main rect and collision rect accordingly. """

        self.y_home += y_movement
        self.rect.centery = int(self.y_home)
        self.collision_rect.midbottom = (self.rect.centerx, self.rect.bottom + self.bottom_inset)

    def update_jiggle(self, now):

        """ Apply some shaking to the car based on speed and time for visual effect. """

        jiggle_speed = self.start_jiggle_speed
        jiggle_intensity = self.start_jiggle_intensity + (abs(self.speed) * 0.0004)

        jiggle_amount = round(math.sin(now * jiggle_speed) * (jiggle_intensity * self.scale))
        self.rect.centery = int(self.y_home + jiggle_amount)

    def update_wheels(self, dt):

        """ Make wheel sprite rotate smoothly """

        self.wheel_angle -= self.speed * dt
        self.wheel_angle %= 360
        self.rotated_wheel = pygame.transform.rotate(
            self.sprites['wheel'], int(self.wheel_angle)
        )

    def toggle_car(self):

        """
        This is attached to the toggle car key.
        Once pressed, the car turns off and stops shaking, works the other way around too.
        """

        self.car_on = not self.car_on

        if self.car_on:
            self.start_jiggle_speed = 0.030
            self.start_jiggle_intensity = 0.10
        else:
            self.start_jiggle_speed = 0
            self.start_jiggle_intensity = 0

    def toggle_light(self):

        """ This is attached to the toggle light key. Once pressed, the front light turns on or off. """

        self.front_light_on = not self.front_light_on

    def toggle_backlight(self):

        """ This is attached to the toggle backlight key. Once pressed, the backlight turns on or off. """

        self.back_light_on = not self.back_light_on

    def update_light_fade(self, light):

        """ This creates a smooth transition for front lights, when turning it in or off. """

        alpha = getattr(self, light + "_alpha")
        fade = getattr(self, light + "_fade_rate")

        if getattr(self, light + "_on"):
            alpha = min(255, alpha + fade)
        else:
            alpha = max(0, alpha - fade)

        setattr(self, light + "_alpha", alpha)

    def draw(self, screen, sprites, scale, get_eye_draw_rect,
             player=None, blinking=False, blink_offset=0, character_blink=None):

        """Draw all parts of the car and its driver, including lights, wheels, and blinking eyes."""

        for name, offset in self.car_offsets.items():

            part_x = int(self.rect.centerx + offset[0] * scale)
            part_y = int(self.rect.centery + offset[1] * scale)

            if name == 'body':
                screen.blit(sprites['body'], self.rect)

            elif name == 'light' and self.front_light_alpha > 0:
                sprites['front_light'].set_alpha(self.front_light_alpha)
                l_rect = sprites['front_light'].get_rect(center=(part_x, part_y))
                screen.blit(sprites['front_light'], l_rect)

            elif name == 'backlight' and self.back_light_alpha > 0:
                sprites['back_light'].set_alpha(self.back_light_alpha)
                l_rect = sprites['back_light'].get_rect(center=(part_x, part_y))
                screen.blit(sprites['back_light'], l_rect)

            elif 'wheel' in name:
                base_rect = sprites['wheel'].get_rect(center=(part_x, part_y))
                rotated_rect = self.rotated_wheel.get_rect(center=base_rect.center)
                screen.blit(self.rotated_wheel, rotated_rect)

            elif name == 'driver' and player == "car":
                d_rect = sprites['driver'].get_rect(center=(part_x, part_y))
                screen.blit(sprites['driver'], d_rect)

                if blinking:
                    eye_rect = get_eye_draw_rect(
                        d_rect,
                        self.DRIVER_EYE_OFFSET,
                        blink_offset,
                        None,
                        0,
                        0,
                        scale
                    )
                    screen.blit(character_blink[0], eye_rect)

    def distance_update(self, dt):

        """ Updates distance based on speed and delta time. This info is displayed to the player. """

        self.distance += (self.speed * dt) / 20


