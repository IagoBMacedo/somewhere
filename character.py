import pygame
import random
from utils import Colors

class Character:
    def __init__(self, sprites, x, y, scale):

        self.sprites = sprites
        self.scale = scale

        self.blink_sprite = sprites["blink"]

        # Character starts standing to the right, the eye offset is right for that
        self.current_anim_set = sprites['standing_right']
        self.current_anim_name = 'standing_right'
        self.last_direction = 'right'
        self.HUMAN_EYE_OFFSET = [8, 6]

        # Rect centerx and centery are affected by this
        self.man_x = x
        self.man_y = y

        # We store movement here before applying it to man_x and man_y so collision actually works
        self.dx = 0
        self.dy = 0

        self.rect = self.current_anim_set[0].get_rect(center=(x, y))

        # The collision rect is mainly used so the player has collision with the car for now
        self.collision_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, (2 * scale))
        self.car_collision = False

        # Animation timing
        self.man_frame_time = 100
        self.last_switch = pygame.time.get_ticks()
        self.current_man_frame = 0

    def handle_movement(self, keys, CONTROLS, dt, streets, screen_size, car_rect):
        # Reset movement each frame
        self.dx = 0
        self.dy = 0

        # Horizontal movement
        if keys[CONTROLS["forward"]] and self.rect.right <= screen_size:
            self.dx = 150 * dt
        elif keys[CONTROLS["backward"]] and self.rect.left >= 0:
            self.dx = -150 * dt
        else:
            self.dx = 0

        # Vertical movement (no car_collision check yet)
        if keys[CONTROLS["down"]] and self.rect.bottom <= streets.streets[0].bottom:
            self.dy += 150 * dt

        if keys[CONTROLS["up"]] and self.rect.bottom >= (streets.streets[0].top * 1.12):
            self.dy -= 150 * dt

        # Predictive collision logic!!!
        pred_rect = self.collision_rect.copy()

        # Horizontal collision prediction
        pred_rect.x += self.dx
        if pred_rect.colliderect(car_rect):
            self.dx = 0  # block only horizontal movement that would collide

        # Vertical collision prediction
        pred_rect.y += self.dy
        if pred_rect.colliderect(car_rect):
            self.dy = 0  # block only vertical movement that would collide

        # Actually apply movement
        self.man_x += self.dx
        self.man_y += self.dy
        self.update_position()

        # Update collision flag (for animation or other logic)
        self.car_collision = self.collision_rect.colliderect(car_rect)

        # Update animation
        self.select_animation()

    def update_position(self):

        """ Update rect position based on man_x and man_y. """

        self.rect.centerx = int(self.man_x)
        self.rect.centery = int(self.man_y)

        self.collision_rect.midbottom = self.rect.midbottom

    def update_animation(self, now):

        """ Advance animation frame if enough time has passed. """

        if now - self.last_switch >= self.man_frame_time:
            self.current_man_frame = (self.current_man_frame + 1) % len(self.current_anim_set)
            self.last_switch = now

    def set_animation(self, anim_name):

        """ This makes setting animation sets easier. """

        if anim_name in self.sprites and self.current_anim_name != anim_name:
            self.current_anim_set = self.sprites[anim_name]
            self.current_anim_name = anim_name
            self.current_man_frame = 0

    def select_animation(self):

        """ Actually run the proper animation according to the direction the character is looking at. """

        if self.dx > 0:
            direction = 'right'
        elif self.dx < 0:
            direction = 'left'
        else:
            direction = self.last_direction  # keep previous if not moving horizontally

        # Update last_direction for future reference
        self.last_direction = direction

        # Pick animation based on movement and direction
        if self.dx != 0 or self.dy != 0:  # moving
            if direction == 'right':
                self.set_animation('walking_right')
            else:
                self.set_animation('walking_left')
        else:  # standing
            if direction == 'right':
                self.set_animation('standing_right')
            else:
                self.set_animation('standing_left')

    def draw(self, screen, get_eye_draw_rect, blinking=False, blink_offset=0, character_blink=None):

        """ Draw character and eyes (if blinking). """

        extra_eye_offsetx = 0
        extra_eye_offsety = 0

        # Eye offsets based on current animation/frame
        if self.current_anim_name == 'standing_right' and self.current_man_frame == 1:
            extra_eye_offsety = 1
        elif self.current_anim_name == 'standing_left':
            extra_eye_offsetx = -2
        elif self.current_anim_name == 'walking_left':
            extra_eye_offsetx = -2
            if self.current_man_frame in [2, 5]:
                extra_eye_offsety = 1
        elif self.current_anim_name == 'walking_right':
            if self.current_man_frame in [2, 5]:
                extra_eye_offsety = 1

        # Draw the character sprite
        screen.blit(self.current_anim_set[self.current_man_frame], self.rect)

        # Draw blinking eyes if needed
        if blinking and character_blink:
            eye_rect = get_eye_draw_rect(
                self.rect, self.HUMAN_EYE_OFFSET, blink_offset,
                self.current_man_frame, extra_eye_offsetx, extra_eye_offsety, self.scale
            )
            screen.blit(self.blink_sprite[0], eye_rect)

class NPC(Character):

    def replace_color(self, surface, old_color, new_color):

        """ Replace color of certain pixels in order to get a higher variety of NPCs. """

        surface = surface.copy()

        px = pygame.PixelArray(surface)
        px.replace(old_color, new_color)
        del px

        return surface

    def recolor_frame(self, frame, colors_map):

        """ Applies all color replacements in a loop. """

        for old_color, new_color in colors_map.items():
            frame = self.replace_color(frame, old_color, new_color)
        return frame

    def __init__(self, npc_sprites, x, y, scale, SCREEN_WIDTH, biome):

        sprites = random.choice(npc_sprites[biome])

        # This allows independent recoloring for each NPC (weirdly, all NPCs will look the same without it)
        sprites = {
            k: [frame.copy() for frame in v] if isinstance(v, list) else v.copy()
            for k, v in sprites.items()
        }

        if biome == "city":
            # City biome specific colors
            jacket_color = random.choice(list(Colors.CITY_NPC_CLOTHES_COLORS.values()))
            pants_color = random.choice(list(Colors.CITY_NPC_CLOTHES_COLORS.values()))
            detail_color = random.choice(list(Colors.CITY_NPC_DETAIL_COLORS.values()))

        elif biome == "mountains":
            jacket_color = random.choice(list(Colors.MOUNTAIN_NPC_JACKET_COLORS.values()))
            pants_color = random.choice(list(Colors.MOUNTAIN_NPC_PANTS_COLORS.values()))
            detail_color = random.choice(list(Colors.MOUNTAIN_NPC_DETAIL_COLORS.values()))

        # General colors
        shoes_color = random.choice(list(Colors.NPC_SHOES_COLORS.values()))
        skin_color = random.choice(list(Colors.NPC_SKIN_COLORS.values()))
        hair_color = random.choices(list(Colors.NPC_HAIR_COLORS.values()), weights=[5,3,2,1], k=1)[0]

        colors_map = {
            (73, 44, 39): shoes_color,
            (238, 195, 154): skin_color,
            (21, 21, 28): hair_color,
            (50, 50, 77): jacket_color,
            (35, 35, 46): pants_color,
            (172, 50, 50): detail_color
        }

        # Apply colors on frame, replacing colors declared in the colors_map dict
        for animation in sprites.values():
            for i, frame in enumerate(animation):
                animation[i] = self.recolor_frame(frame, colors_map)

        super().__init__(sprites, x, y, scale)

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.speed = 100

        self.blink_sprite = sprites["blink"]

        # Each NPC will be either walking left or right
        self.direction_options = ["right", "left"]
        self.direction = random.choice(self.direction_options)

        # Each NPC will randomly spawn at the left or right of the street
        self.man_y_options = [132 * scale, 103 * scale]
        self.man_y = random.choice(self.man_y_options)
        if self.direction == "right":
            self.man_y += (2 * scale)

        # NPCs always spawn foward, where the player cannot see
        self.man_x = random.randint(self.SCREEN_WIDTH, self.SCREEN_WIDTH + self.SCREEN_WIDTH)

    def npc_movement(self, dt, speed):

        """ Identify movement as the car moves forward, or else just return 0. """

        movement_speed = 1.2

        if speed > 0:
            return -speed * movement_speed * dt
        return 0

    def update_ai(self, dt, speed):

        """
        Update NPC position and animation each frame.

        Moves the NPC according to its own direction and the scrolling speed of the world,
        updates the collision/rect position, and sets the appropriate animation based on movement.
        """

        # NPC walking direction
        self.dx = self.speed * dt if self.direction == "right" else -self.speed * dt

        # Combine NPC movement + world movement
        self.man_x += self.dx + self.npc_movement(dt, speed)

        # Update rect after final position
        self.update_position()

        # Animation automatically chooses based on dx
        self.select_animation()





