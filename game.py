# Standard library
import math
import os
import random

# Third-party
import pygame

# Local modules
import car
import character
import buildings
import terrain
import street
import sprites
from blink import Blink
from utils import color_change, Colors
from utils import Fader

pygame.init()

########################################################################################################################
#                                                    SETUP                                                             #
########################################################################################################################

# --- Display setup ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_size = screen.get_width()
pygame.display.set_caption('Driving Game')

# --- Sprites ---
scale = 7
player_on_foot_sprites = sprites.load_character_sprites(
    os.path.join("sprites", "man", "player_sheet.png"), scale)

#######################################################################################################################

fade_screen = Fader((SCREEN_WIDTH, SCREEN_HEIGHT))

#######################################################################################################################
# Load city man sprites
city_man_sprites = sprites.load_character_sprites(
    os.path.join("sprites", "man", "city_man_sheet.png"), scale)

# Load city woman sprites
city_woman_sprites = sprites.load_character_sprites(
    os.path.join("sprites", "man", "city_woman_sheet.png"), scale)

city_npc_sprites = [city_man_sprites, city_woman_sprites]

#######################################################################################################################

# Load man sprites
mountain_man_sprites = sprites.load_character_sprites(
    os.path.join("sprites", "man", "mountain_man_sheet.png"), scale)

# Load woman sprites
mountain_woman_sprites = sprites.load_character_sprites(
    os.path.join("sprites", "man", "mountain_woman_sheet.png"), scale)

mountain_npc_sprites = [mountain_man_sprites, mountain_woman_sprites]

#######################################################################################################################

npc_sprites = {
    "city": city_npc_sprites,
    "mountains": mountain_npc_sprites
}

player_in_car_sprites = sprites.load_player_car_sprites(scale)
world_sprites = sprites.load_world_sprites(scale)
billboard_sprites = sprites.load_billboard_sprites(scale)
blink = Blink()

# --- World setup (must be before player position!) ---
streets = street.Street(world_sprites['street'], world_sprites['lightpole'], world_sprites['billboard'], billboard_sprites, SCREEN_WIDTH, scale)
land = terrain.Terrain(scale, SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Player setup ---
# Position depends on streets, so streets must exist first
x, y = 400, (streets.streets[1].centery - (8 * scale))
player_car = car.Car(player_in_car_sprites, x, y, scale)
player_on_foot = character.Character(player_on_foot_sprites, x, y, scale)
player = "man"

# --- UI ---
font1 = pygame.font.Font('freesansbold.ttf', 20)
sky_color = Colors.SKY_COLORS['light_yellow']
# ending = Ending(SCREEN_WIDTH, SCREEN_HEIGHT) - UNUSED

# --- Biome logic ---
biomes = ("mountains", "city")
biome = "mountains"
old_biome = None
biome_check = True
biome_change_distance = 500
next_biome_change = biome_change_distance

# --- Clock ---
clock = pygame.time.Clock()

# --- Buildings setup ---
building_layers = [
    {
        "buildings": [],
        "cumulative_x": SCREEN_WIDTH,
        "windows_x": (9, 12),
        "windows_y": lambda: int(random.triangular(12, 22, 21)),
        "scale": scale / 6.2,
        "fade": 0.1
    },
    {
        "buildings": [],
        "cumulative_x": SCREEN_WIDTH,
        "windows_x": (9, 12),
        "windows_y": lambda: random.randint(25, 26),
        "scale": scale / 7.5,
        "fade": 0.3
    },
    {
        "buildings": [],
        "cumulative_x": SCREEN_WIDTH,
        "windows_x": (12, 15),
        "windows_y": lambda: random.randint(35, 37),
        "scale": scale / 10,
        "fade": 0.5
    },
    {
        "buildings": [],
        "cumulative_x": SCREEN_WIDTH,
        "windows_x": (12, 15),
        "windows_y": lambda: random.randint(44, 46),
        "scale": scale / 12,
        "fade": 0.7
    }
]

# --- NPCs setup ---
NPCs = []

########################################################################################################################
#                                                  CONTROLS ZONE                                                       #
########################################################################################################################

CONTROLS = {
    "forward": pygame.K_d,
    "backward": pygame.K_a,
    "down": pygame.K_s,
    "up": pygame.K_w,
    "start_car": pygame.K_e,
    "light": pygame.K_q,
    "interact_car": pygame.K_f
}

########################################################################################################################
#                                                  GAME-LOOP ZONE                                                      #
########################################################################################################################

run = True

while run:
    dt = clock.tick(60) / 1000.0
    now = pygame.time.get_ticks()
    blink.update_blink(now, scale)

    streets.street_movement(dt, player_car.speed)
    streets.lightpole_movement(dt, player_car.speed)
    streets.billboard_movement(dt, player_car.speed, biome)

    player_car.distance_update(dt)
    land.terrain_movement(dt, player_car.speed)

    target_goal = 0
    # if player_car.distance >= 2000: - UNUSED
    #     target_goal = 255 - UNUSED

    fade_screen.update(dt, duration=5, target=target_goal)

    for layer in building_layers:

        layer_buildings = layer["buildings"]

        if layer_buildings:

            for b in layer_buildings:
                b.building_movement(dt, player_car.speed)

            layer["cumulative_x"] -= (player_car.speed * layer_buildings[0].movement_speed * dt)

            if layer_buildings[0].x < (-100 * scale):
                layer_buildings.pop(0)

    if player_car.distance >= next_biome_change:
        old_biome = biome
        biome = random.choice(biomes)

        if old_biome != "city" and biome == "city":
            for layer in building_layers:
                layer["buildings"].clear()
                layer["cumulative_x"] = SCREEN_WIDTH

        if old_biome!= "mountain" and biome == "mountain":
            land.chunks.clear()
            land.chunk_surfaces.clear()

        next_biome_change += biome_change_distance

    if len(NPCs) < 8:
        npc = character.NPC(npc_sprites, x, y, scale, SCREEN_WIDTH, biome)
        NPCs.append(npc)

    for npc in NPCs:
        npc.update_position()
        npc.update_ai(dt, player_car.speed)
        npc.update_animation(now)

        if npc.man_x < -50:
            NPCs.remove(npc)

        if npc.man_x > SCREEN_WIDTH + SCREEN_WIDTH:
            NPCs.remove(npc)

########################################################################################################################
#                                                  TERRAIN SPAWN                                                       #
########################################################################################################################
    if biome == "mountains":
        sky_color = color_change(sky_color, Colors.SKY_COLORS['light_yellow'], player_car.speed)
        screen.fill(sky_color)
        land.terrain_loop()

########################################################################################################################
#                                                    CITY AREA                                                         #
########################################################################################################################

    if biome == "city":

        sky_color = color_change(sky_color, Colors.SKY_COLORS['dark_blue'], player_car.speed)
        screen.fill(sky_color)

        for layer in building_layers:

            layer_buildings = layer["buildings"]

            if len(layer_buildings) == 0 or layer_buildings[-1].x + layer_buildings[-1].building_width < SCREEN_WIDTH:
                b = buildings.Building(
                    windows_in_x=random.randint(*layer["windows_x"]),
                    windows_in_y=layer["windows_y"](),
                    x=layer["cumulative_x"],
                    scale=layer["scale"],
                    color_fade=layer["fade"],
                    SCREEN_HEIGHT=SCREEN_HEIGHT,
                )

                layer_buildings.append(b)
                layer["cumulative_x"] += b.building_width + b.gap

########################################################################################################################
#                                                      TOGGLES                                                         #
########################################################################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        next_player = player

        if event.type == pygame.KEYDOWN:
            if player == "car":
                if event.key == CONTROLS["start_car"]:
                    player_car.toggle_car()
                elif event.key == CONTROLS["light"]:
                    player_car.toggle_light()
                elif event.key == CONTROLS["interact_car"] and player_car.speed == 0:
                    next_player = "man"

            elif player == "man":
                car_range = player_car.driver_x - 60, player_car.driver_x + 60
                if event.key == CONTROLS["interact_car"] and car_range[0] <= player_on_foot.rect.centerx <= car_range[
                    1]:
                    next_player = "car"

        player = next_player


    keys = pygame.key.get_pressed()
    ####################################################################################################################
    #                                               CAR GAMEPLAY                                                       #
    ####################################################################################################################

    if player == "car":

        player_car.handle_movement(keys, CONTROLS, dt, streets)


        # Lights!!!
        player_car.update_light_fade("front_light")
        player_car.update_light_fade("back_light")

        # Wheel rotation!!!
        player_car.update_wheels(dt)

        # Car jiggle!!!
        player_car.update_jiggle(now)


    ####################################################################################################################
    #                                               MAN GAMEPLAY                                                       #
    ####################################################################################################################

    if player == "man":
        # Update rect position and animation timing
        player_on_foot.update_position()
        player_on_foot.update_animation(now)

        # Handle character movement & animation internally
        player_on_foot.handle_movement(keys, CONTROLS, dt, streets, screen_size, player_car.collision_rect)

    ####################################################################################################################
    #                                             BLIT ZONE                                                            #
    ####################################################################################################################

    # Drawing terrain
    land.terrain_draw(screen, sky_color)

    for layer in reversed(building_layers):
        for b in layer["buildings"]:
            b.building_draw(screen, sky_color)

    # Drawing billboards
    streets.billboard_draw(screen, sky_color)

    # Drawing streets
    streets.street_draw(screen)

    # Prepare a list of drawable objects and their rect.bottom for sorting
    draw_order = []

    # Lightpoles
    for pole in streets.lightpoles:
        draw_order.append((streets.lightpole_sprite, pole.bottom, 'lightpole'))

    # Car
    draw_order.append((player_car, player_car.rect.bottom + (1 * scale), 'car'))

    # NPCs
    for npc in NPCs:
        draw_order.append((npc, npc.rect.bottom, 'npc'))

    # Player (if on foot)
    if player == "man":
        draw_order.append((player_on_foot, player_on_foot.rect.bottom, 'player'))

    # Sort by rect.bottom
    draw_order.sort(key=lambda x: x[1])

    '''Draw in order'''
    for obj, bottom, kind in draw_order:

        if kind == 'lightpole':
            for pole in streets.lightpoles:
                screen.blit(obj, pole)

        elif kind == 'car':
            obj.draw(
                screen,
                player_in_car_sprites,
                scale,
                blink.get_eye_draw_rect,
                player=player,
                blinking=blink.blinking,
                blink_offset=blink.blink_offset,
                character_blink=player_on_foot_sprites['blink'],
            )
        elif kind == 'player':
            obj.draw(
                screen,
                blink.get_eye_draw_rect,
                blinking=blink.blinking,
                blink_offset=blink.blink_offset,
                character_blink=player_on_foot_sprites['blink'],
            )

        elif kind == 'npc':
            obj.draw(
                screen,
                blink.get_eye_draw_rect,
                blinking=blink.blinking,
                blink_offset=blink.blink_offset,
                character_blink=player_on_foot_sprites['blink'],
            )


    if player_car.distance < 999:
        distance_text = font1.render(f"{int(player_car.distance)} m", True, (255, 255, 255))
        screen.blit(distance_text, (20, 20))
    else:
        distance_text = font1.render(f"{(player_car.distance / 1000): .2f} km", True, (255, 255, 255))
        screen.blit(distance_text, (20, 20))

    fade_screen.draw(screen)

    # if fade_screen.alpha == 255: - UNUSED
    #     ending.draw(screen) - UNUSED


    pygame.display.flip()
pygame.quit()