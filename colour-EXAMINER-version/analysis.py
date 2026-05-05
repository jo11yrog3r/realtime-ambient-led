from config import GRID_COLS, GRID_ROWS, RANDOM_NUM_SAMPLES
import random

def get_midpoint(num_1, num_2):
    return (num_1 + num_2) // 2

def sample_rgb_fixed_grid(img, img_width, img_height):
    cell_w = img_width // GRID_COLS
    cell_h = img_height // GRID_ROWS

    samples = []

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell_left = col * cell_w
            cell_top = row * cell_h

            cell_right = img_width if col == GRID_COLS - 1 else (col + 1) * cell_w
            cell_bottom = img_height if row == GRID_ROWS - 1 else (row + 1) * cell_h

            x = get_midpoint(cell_left, cell_right)
            y = get_midpoint(cell_top, cell_bottom)

            rgb = img.getpixel((x, y))
            samples.append(rgb)

    avg_r = sum(c[0] for c in samples) // len(samples)
    avg_g = sum(c[1] for c in samples) // len(samples)
    avg_b = sum(c[2] for c in samples) // len(samples)

    return (avg_r, avg_g, avg_b)

def sample_rgb_grid_random(img, img_width, img_height):
    cell_w = img_width // GRID_COLS
    cell_h = img_height // GRID_ROWS

    samples = []

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell_left = col * cell_w
            cell_top = row * cell_h

            cell_right = img_width if col == GRID_COLS - 1 else (col + 1) * cell_w
            cell_bottom = img_height if row == GRID_ROWS - 1 else (row + 1) * cell_h

            x = random.randint(cell_left, cell_right - 1)
            y = random.randint(cell_top, cell_bottom - 1)

            rgb = img.getpixel((x, y))
            samples.append(rgb)

    avg_r = sum(c[0] for c in samples) // len(samples)
    avg_g = sum(c[1] for c in samples) // len(samples)
    avg_b = sum(c[2] for c in samples) // len(samples)

    return (avg_r, avg_g, avg_b)

def sample_rgb_random(img, img_width, img_height):
    total_r = 0
    total_g = 0
    total_b = 0

    for _ in range(RANDOM_NUM_SAMPLES):
        x = random.randint(0, img_width - 1)
        y = random.randint(0, img_height - 1)

        r, g, b = img.getpixel((x, y))
        total_r += r
        total_g += g
        total_b += b

    avg_r = total_r // RANDOM_NUM_SAMPLES
    avg_g = total_g // RANDOM_NUM_SAMPLES
    avg_b = total_b // RANDOM_NUM_SAMPLES

    return (avg_r, avg_g, avg_b)


