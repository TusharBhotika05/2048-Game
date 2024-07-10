import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 800)
TITLE = "2048"
FPS = 60
MOVEMENT_SPEED = 20

# Colors
OUTLINE_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

# Font
FONT_STYLE = "clearsans"
FONT_SIZE = 150
font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE, bold=False)

# Setup the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Grid setup
GRID_SIZE = 4
TILE_SIZE = (WINDOW_SIZE[0] - (GRID_SIZE + 1) * 10) // GRID_SIZE
OUTLINE_THICKNESS = 10

# Initialize the grid with zeros
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Tile positions for smooth animation
tile_positions = [[(j * TILE_SIZE + (j + 1) * OUTLINE_THICKNESS,
                    i * TILE_SIZE + (i + 1) * OUTLINE_THICKNESS)
                   for j in range(GRID_SIZE)]
                  for i in range(GRID_SIZE)]

# Add two initial tiles
def add_new_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = 2 if random.random() < 0.9 else 4

add_new_tile()
add_new_tile()

# Draw the grid
def draw_grid():
    screen.fill(OUTLINE_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * TILE_SIZE + (j + 1) * OUTLINE_THICKNESS,
                               i * TILE_SIZE + (i + 1) * OUTLINE_THICKNESS,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect)
            if grid[i][j] != 0:
                # Smooth animation by interpolating between current and target positions
                x, y = tile_positions[i][j]
                current_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                draw_tile(current_rect, grid[i][j])

# Draw a single tile
def draw_tile(rect, value):
    # Draw tile background
    pygame.draw.rect(screen, get_tile_color(value), rect)

    # Draw tile text
    text_surface = font.render(str(value), True, FONT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Get the color of a tile based on its value
def get_tile_color(value):
    # Function to get color based on tile value
    colors = {
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
        4096: (237, 190, 30),
        8192: (237, 187, 13),
    }
    return colors.get(value, (205, 192, 180))

# Move and merge tiles in a given direction
def move_and_merge_tiles(direction):
    # Define a global variable grid
    global grid
    # Create a copy of the original grid
    original_grid = [row[:] for row in grid]

    # If the direction is left
    if direction == "left":
        # Loop through each row in the grid
        for i in range(GRID_SIZE):
            # Merge the tiles in the row
            grid[i] = merge_tiles(grid[i])
    # If the direction is right
    elif direction == "right":
        # Loop through each row in the grid
        for i in range(GRID_SIZE):
            # Reverse the row, merge the tiles, and reverse the row back
            grid[i] = merge_tiles(grid[i][::-1])[::-1]
    # If the direction is up
    elif direction == "up":
        # Transpose the grid
        grid = transpose(grid)
        # Loop through each row in the grid
        for i in range(GRID_SIZE):
            # Merge the tiles in the row
            grid[i] = merge_tiles(grid[i])
        # Transpose the grid back
        grid = transpose(grid)
    # If the direction is down
    elif direction == "down":
        # Transpose the grid
        grid = transpose(grid)
        # Loop through each row in the grid
        for i in range(GRID_SIZE):
            # Reverse the row, merge the tiles, and reverse the row back
            grid[i] = merge_tiles(grid[i][::-1])[::-1]
        # Transpose the grid back
        grid = transpose(grid)

    # Animate tile movement
    animate_tiles(original_grid)

    # Check if grid has changed, if so add new tile
    if any(grid[i][j] != original_grid[i][j] for i in range(GRID_SIZE) for j in range(GRID_SIZE)):
        add_new_tile()

# Animate tile movement to smooth transition
def animate_tiles(original_grid):
    # Animate tile movement to smooth transition
    # Loop through each tile in the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # If the current tile is not the same as the original tile
            if grid[i][j] != original_grid[i][j]:
                # Calculate the target position of the tile
                target_x, target_y = (j * TILE_SIZE + (j + 1) * OUTLINE_THICKNESS,
                                      i * TILE_SIZE + (i + 1) * OUTLINE_THICKNESS)
                # Get the current position of the tile
                current_x, current_y = tile_positions[i][j]
                # Calculate the change in x and y positions
                dx = (target_x - current_x) / MOVEMENT_SPEED
                dy = (target_y - current_y) / MOVEMENT_SPEED
                # While the current position is not the same as the target position
                while current_x != target_x or current_y != target_y:
                    # Update the current position
                    current_x += dx
                    current_y += dy
                    # Update the tile position
                    tile_positions[i][j] = (current_x, current_y)
                    # Draw the grid
                    draw_grid()
                    # Update the display
                    pygame.display.flip()
                    # Limit the frame rate
                    clock.tick(FPS)

# Merge tiles in a single row   
def merge_tiles(row):
    # Remove all zeros from the row
    row = [value for value in row if value != 0]
# Loop through the row and if two adjacent values are the same, double the first value and set the second value to 0
    for i in range(len(row) - 1):
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    # Remove all zeros from the row again
    row = [value for value in row if value != 0]
    # Add zeros to the end of the row to make it the same length as the GRID_SIZE
    row += [0] * (GRID_SIZE - len(row))
    # Return the row
    return row

# Transpose a grid
def transpose(grid):
    return [list(row) for row in zip(*grid)]

# Check if there are any possible moves left
def can_move():
    # Loop through each row in the grid
    for i in range(GRID_SIZE):
        # Loop through each column in the grid
        for j in range(GRID_SIZE):
            # Check if the current cell is empty
            if grid[i][j] == 0:
                # If the current cell is empty, return True
                return True
            # Check if the current cell is the same as the cell to its right
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                # If the current cell is the same as the cell to its right, return True
                return True
            # Check if the current cell is the same as the cell below it
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                # If the current cell is the same as the cell below it, return True
                return True
    # If no empty cells or matching cells are found, return False
    return False

# Main game loop
running = True
while running:
    # Loop through all events in the queue
    for event in pygame.event.get():
        # If the event is a quit event
        if event.type == pygame.QUIT:
            # Set running to False
            running = False
        # If the event is a keydown event
        elif event.type == pygame.KEYDOWN:
            # If the key pressed is the left arrow key
            if event.key == pygame.K_LEFT:
                # Call the move_and_merge_tiles function with the argument "left"
                move_and_merge_tiles("left")
            # If the key pressed is the right arrow key
            elif event.key == pygame.K_RIGHT:
                # Call the move_and_merge_tiles function with the argument "right"
                move_and_merge_tiles("right")
            # If the key pressed is the up arrow key
            elif event.key == pygame.K_UP:
                # Call the move_and_merge_tiles function with the argument "up"
                move_and_merge_tiles("up")
            # If the key pressed is the down arrow key
            elif event.key == pygame.K_DOWN:
                # Call the move_and_merge_tiles function with the argument "down"
                move_and_merge_tiles("down")

    # Check for game over (no possible moves)
    if not can_move():
        running = False

    # Draw the grid
    draw_grid()

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
