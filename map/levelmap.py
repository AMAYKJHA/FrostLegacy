import pygame as pg

pg.init()

info = pg.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 65

# Create the screen
screen = pg.display.set_mode((screen_width, screen_height))

pg.display.set_caption("Levels map")

background = pg.image.load("assets/map/b3.png")
# Resizing the image
background = pg.transform.scale(background, (screen_width, screen_height))

#background music
pg.mixer.music.load('assets/map/background.mp3')
pg.mixer.music.set_volume(0.6)  # Adjust volume
pg.mixer.music.play(-1)  # Loop indefinitely

def load_image(path, size):
    """Loads, optimizes, and resizes an image."""
    img = pg.image.load(path).convert_alpha()
    return pg.transform.scale(img, size)

# Load and resize images using the function
island = load_image("assets/map/island.png", (200, 200))
ruin = load_image("assets/map/ruin1.png", (150, 150))
cave = load_image("assets/map/cave.png", (150, 150))
spire = load_image("assets/map/ruin.png", (150, 150))
heart = load_image("assets/map/heart.png", (150, 150))

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BROWN = (181, 101, 29)
LIGHTBLUE = (208, 212, 230)
GREEN = (126, 204, 0)
YELLOW = (255, 255, 0)

# Levels and their positions
level_positions = {
    "Frozen Village": (screen_width * 0.08, screen_height * 0.33),
    "Glacial Ruin": (screen_width * 0.375, screen_height * 0.165),
    "Cavern of Frost": (screen_width * 0.20, screen_height * 0.66),
    "Frozen Spire": (screen_width * 0.559, screen_height * 0.825),
    "Heart of Frozen Wastes": (screen_width * 0.90, screen_height * 0.55)
}

# Load sound
click_sound = pg.mixer.Sound('assets/map/levelup.mp3')
click_sound.set_volume(0.5)  # Reduce volume to 30%

# Store original images for restoring later
original_images = {
    "island": island.copy(),
    "ruin": ruin.copy(),
    "cave": cave.copy(),
    "spire": spire.copy(),
    "heart": heart.copy(),
}

level_images = [
    (island,(screen_width * 0.08, screen_height * 0.13)),
    (ruin,(screen_width * 0.404, screen_height * 0.105)),
    (cave,(screen_width * 0.15, screen_height * 0.73)),
    (spire,(screen_width * 0.600, screen_height * 0.725)),
    (heart,(screen_width * 0.90, screen_height * 0.35))
]

def darken_images():
    """Darken all images in level_images."""
    for img_var, _ in level_images:
        img_var.fill((50, 50, 50), special_flags=pg.BLEND_RGBA_MULT)

def restore_images():
    """Restore all images to their original colors."""
    for i, (img_var, pos) in enumerate(level_images):
        # Find the corresponding original image from the dictionary
        restored_image = original_images[list(original_images.keys())[i]].copy()
        # Replace the image in level_images with the restored one
        level_images[i] = (restored_image, pos)

# Path connections (pairs of level names)
level_paths = [
    ("Frozen Village", "Glacial Ruin"),
    ("Glacial Ruin", "Cavern of Frost"),
    ("Cavern of Frost", "Frozen Spire"),
    ("Frozen Spire", "Heart of Frozen Wastes")
]

# Locked levels (only Frozen Village is unlocked at the start)
unlocked_levels = ["Frozen Village"]

# Fonts
font = pg.font.SysFont('Comic Sans MS', 18)


def draw_map():
    """Draw the level map with paths and nodes."""

    # Draw paths (dotted lines)
    for path in level_paths:
        start = level_positions[path[0]]
        end = level_positions[path[1]]
        draw_dotted_line(screen, BROWN, start, end, 10)

    # Draw level nodes
    for level, position in level_positions.items():
        if level in unlocked_levels:
            pg.draw.circle(screen, GREEN, position, 10)  # circle for unlocked levels

            # Render and display the level name
            label = font.render(level, True, BLACK)
            screen.blit(label, (position[0] - label.get_width() // 2, position[1] + 25))

            # display unlocked darkened images
            for img_var, img_pos in level_images:
                if img_pos != position:  # Check if the image's position matches the current level position
                    restore_images()
                    screen.blit(img_var, img_pos)

        else:
            pg.draw.circle(screen, LIGHTBLUE, position, 10)  # Locked levels
            label = font.render(level, True, LIGHTBLUE)
            screen.blit(label, (position[0] - label.get_width() // 2, position[1] + 25))
            for img_var, img_pos in level_images:
                 if img_pos != position:
                     darken_images()  # Darken the image
                     screen.blit(img_var, img_pos)

# def draw_map():
#     """Draw the level map with paths and nodes."""

#     # Restore images before drawing the map
#     restore_images()

#     # Draw paths (dotted lines)
#     for path in level_paths:
#         start = level_positions[path[0]]
#         end = level_positions[path[1]]
#         draw_dotted_line(screen, BROWN, start, end, 10)

#     # Draw level nodes
#     for level, position in level_positions.items():
#         if level in unlocked_levels:
#             pg.draw.circle(screen, GREEN, position, 10)  # circle for unlocked levels

#             # Render and display the level name
#             label = font.render(level, True, BLACK)
#             screen.blit(label, (position[0] - label.get_width() // 2, position[1] + 25))

#         else:
#             pg.draw.circle(screen, LIGHTBLUE, position, 10)  # Locked levels
#             label = font.render(level, True, LIGHTBLUE)
#             screen.blit(label, (position[0] - label.get_width() // 2, position[1] + 25))
#             darken_images()  # Darken the image

#     # Display images
#     for img_var, img_pos in level_images:
#         screen.blit(img_var, img_pos)

def draw_dotted_line(surface, color, start_pos, end_pos, dash_length):
    """Draw a dotted line between two points."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if length == 0:  # Prevent division by zero
        return
    dx = (x2 - x1) / length * dash_length
    dy = (y2 - y1) / length * dash_length

    for i in range(0, int(length // dash_length), 2):
        start = (x1 + i * dx, y1 + i * dy)
        end = (x1 + (i + 1) * dx, y1 + (i + 1) * dy)
        pg.draw.line(surface, color, start, end, 2)

'''
def handle_click(pos):
    """Handle mouse clicks on level nodes."""
    global unlocked_levels

    for level, position in level_positions.items():
        if level in unlocked_levels:  # Only unlocked levels are clickable
            dist = ((pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2) ** 0.5
            if dist < 60:  # Click inside the circle
                print(f"{level} clicked!")
                unlock_next_level(level)
                return
'''

def unlock_next_level(current_level):
    """Unlock the next level in the path."""
    global unlocked_levels

    for path in level_paths:
        if path[0] == current_level and path[1] not in unlocked_levels:
            unlocked_levels.append(path[1])
            break

def handle_click(pos):
    """Handle mouse clicks on level nodes."""
    global unlocked_levels

    for level, position in level_positions.items():
        if level in unlocked_levels:  # Only unlocked levels are clickable
            dist = ((pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2) ** 0.5  # Fix applied
            if dist < 60:  # Click inside the circle
                print(f"{level} clicked!")
                click_sound.play()  # Play sound when level is clicked
                unlock_next_level(level)
                return


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                handle_click(event.pos)

    # Background
    screen.blit(background, (0, 0))
    draw_map()

    pg.display.flip()

pg.mixer.music.stop()

pg.quit()
