import pygame
import os

def load_frame(folder_path, filename):

    """ This is a helper function that loads a frame from the specified folder and converts it to alpha. """

    return pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()

def load_character_sprites(path, scale):

    """
    Load and prepare all character sprites from a sprite sheet.

    This includes:
    - Standing right/left
    - Walking right/left (multiple frames)
    - Blinking sprite

    All sprites are scaled by the provided scale factor.
    Returns a dictionary of sprite lists keyed by animation name.
    """

    # Load the sprite sheet
    player_sheet = pygame.image.load(path).convert_alpha()

    # Size of each individual sprite on the sheet
    character_sheet_x = 15
    character_sheet_y = 30

    # Standing sprites
    standing_right = [pygame.transform.scale(
        player_sheet.subsurface((0, 0, character_sheet_x, character_sheet_y)),
        (character_sheet_x * scale, character_sheet_y * scale)
    )]
    standing_left = [pygame.transform.flip(f, True, False) for f in standing_right]

    # Walking frames (precompute coordinates)
    walking_right_base = []

    # Walking right starts in the first row as the second element in the sheet
    for i in range(3):
        walking_right_base.append(
            [character_sheet_x * (i + 1), 0,
             character_sheet_x, character_sheet_y])

    # Plus the second row!
    for i in range(3):
        walking_right_base.append([character_sheet_x * i, character_sheet_y,
                                   character_sheet_x, character_sheet_y])

    # Generate walking sprites
    walking_right = [
        pygame.transform.scale(player_sheet.subsurface(frame),
        (character_sheet_x * scale, character_sheet_y * scale))
        for frame in walking_right_base]

    # Walking_left is walking right but inverted
    walking_left = [pygame.transform.flip(f, True, False) for f in walking_right]

    # Load blinking sprite (single frame)
    blinking_base = os.path.join(
        os.path.dirname(__file__),
        "sprites",
        "man",
        "blinking"
    )

    blink_frame = load_frame(blinking_base, "character_blink.png")
    character_blink = pygame.transform.scale(
        blink_frame,
        (blink_frame.get_width() * scale, blink_frame.get_height() * scale)
    )

    return {
        "standing_right": standing_right,
        "standing_left": standing_left,
        "walking_right": walking_right,
        "walking_left": walking_left,
        "blink": [character_blink]
    }

def load_player_car_sprites(scale):

    car_base = os.path.join(os.path.dirname(__file__), 'sprites', 'car')
    car_sprites = {
        'body': load_frame(car_base, 'carframe.png'),
        'wheel': load_frame(car_base, 'wheel1.png'),
        'front_light': load_frame(car_base, 'carlight.png'),
        'back_light': load_frame(car_base, 'carbacklight.png'),
        'driver': load_frame(car_base, 'character1.png'),
    }

    for key in car_sprites:
        img = car_sprites[key]
        car_sprites[key] = pygame.transform.scale(
            img,
            (int(img.get_width() * scale), int(img.get_height() * scale))
        )

    return car_sprites

scale_multipliers = {
    'street': 1.0,
    'lightpole': 1.0,
    'billboard': 1.8   # billboard bigger
}

def load_world_sprites(scale):
    world_base = os.path.join(
        os.path.dirname(__file__),
        'sprites',
        'world'
    )

    world_sprites = {
        'street': load_frame(world_base, 'street1.png'),
        'lightpole': load_frame(world_base, 'lightpole1.png'),
        'billboard': load_frame(world_base, 'billboard.png')
    }

    for key in world_sprites:
        img = world_sprites[key]
        s = scale * scale_multipliers.get(key, 1)

        world_sprites[key] = pygame.transform.scale(
            img,
            (int(img.get_width() * s), int(img.get_height() * s))
        )

    return world_sprites

def load_billboard_sprites(scale):

    billboard_base = os.path.join(
        os.path.dirname(__file__),
        "sprites",
        "world",
        "billboard"
    )

    scale_multiplier = scale_multipliers['billboard'] / 3

    billboard_images = {
        "ad1": load_frame(billboard_base, "dental_records.png"),
        "ad2": load_frame(billboard_base, "why_keep_going.png"),
        "ad3": load_frame(billboard_base, "zhiguli.png"),
        "ad4": load_frame(billboard_base, "mudman_blues.png"),
    }

    for key in billboard_images:
        img = billboard_images[key]
        s = scale * scale_multiplier
        billboard_images[key] = pygame.transform.scale(
            img,
            (int(img.get_width() * s), int(img.get_height() * s))
        )

    return billboard_images