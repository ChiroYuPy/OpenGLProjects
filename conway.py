import pygame
import numpy as np
from BetterButton import Button

# Dimensions de la grille
GRID_SIZE = 64
CELL_SIZE = 10

# Dimensions de la fenêtre (viewport)
VIEWPORT_WIDTH, VIEWPORT_HEIGHT = 1280, 720

# Initialisation de Pygame
pygame.init()
WIDTH, HEIGHT = VIEWPORT_WIDTH, VIEWPORT_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Calculer la position initiale du viewport pour centrer la grille
viewport_x = (WIDTH - GRID_SIZE * CELL_SIZE) / 2
viewport_y = (HEIGHT - GRID_SIZE * CELL_SIZE) / 2

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (0, 192, 0)

# Variables pour le menu scrollable
menu_x = WIDTH - 150
menu_y = 0
menu_height = HEIGHT

# Liste des presets
presets = ["Preset 1", "Preset 2", "Preset 3", "Preset 4", "Preset 5", "Gosper Gun"]
selected_preset = None

font = pygame.font.Font(None, 36)

# Fonction pour dessiner le menu scrollable
def draw_menu():
    pygame.draw.rect(screen, GRAY, (menu_x, menu_y, 150, menu_height))
    for i, preset in enumerate(presets):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_x + 10 <= event.pos[0] <= menu_x + 140 and menu_y + i * 50 + 10 <= event.pos[1] <= menu_y + (
                    i + 1) * 50 + 10:
                select_preset(preset)


# Fonction pour sélectionner un preset
def select_preset(preset):
    global selected_preset
    selected_preset = preset
    load_preset(preset)


# Fonction pour initialiser la grille vide
def init_grid():
    return np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)


# Fonction pour mettre à jour la grille selon les règles de Conway
def update_grid(grid):
    new_grid = grid.copy()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Compter les voisins vivants
            neighbors = np.sum(grid[x - 1:x + 2, y - 1:y + 2]) - grid[x, y]
            if grid[x, y] == 1:  # La cellule est vivante
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = 0  # La cellule meurt
            elif grid[x, y] == 0:  # La cellule est morte
                if neighbors == 3:
                    new_grid[x, y] = 1  # Une nouvelle cellule naît
    return new_grid


grid = init_grid()
clock = pygame.time.Clock()

# Variable pour gérer le placement manuel des cellules
placing_cells = False

# Variables pour le zoom et le déplacement
zoom_factor = 1
min_zoom = 0.1
zoom_center_x, zoom_center_y = WIDTH / 2, HEIGHT / 2
panning = False
pan_start_x, pan_start_y = 0, 0

running = True
simulation_running = False


# Fonction pour réinitialiser la grille
def reset_grid():
    global grid
    grid = init_grid()


# Fonction pour démarrer/arrêter la simulation
def toggle_simulation():
    global simulation_running
    simulation_running = not simulation_running


# Fonction pour charger un preset de carte
def load_preset(preset):
    global grid
    if preset == "Preset 1":
        grid = init_grid()
        grid[25, 25] = 1
        grid[26, 26] = 1
        grid[27, 26] = 1
        grid[27, 25] = 1
        grid[27, 24] = 1
    elif preset == "Preset 2":
        grid = init_grid()
        grid[30, 30] = 1
        grid[31, 30] = 1
        grid[32, 30] = 1
    elif preset == "Preset 3":
        grid = init_grid()
        grid[20, 20] = 1
        grid[20, 21] = 1
        grid[20, 22] = 1
        grid[21, 22] = 1
        grid[22, 21] = 1
    elif preset == "Preset 4":
        grid = init_grid()
        grid[15, 15] = 1
        grid[15, 16] = 1
        grid[16, 15] = 1
        grid[16, 16] = 1
    elif preset == "Preset 5":
        grid = init_grid()
        grid[30, 30] = 1
        grid[31, 30] = 1
        grid[32, 30] = 1
        grid[34, 31] = 1
        grid[35, 32] = 1
    return grid


def load_gosper_glider_gun():
    global grid
    grid = init_grid()
    gun_pattern = [
        (24, 0), (22, 1), (24, 1),
        (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
        (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3),
        (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
        (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), (24, 5),
        (10, 6), (16, 6), (24, 6),
        (11, 7), (15, 7),
        (12, 8), (13, 8)
    ]
    for x, y in gun_pattern:
        grid[x, y] = 1

hollow_box_button = 70

preset1_button = Button("Preset 1", (WIDTH - 120, 20), 200, 50, 10, lambda: load_preset("Preset 1"))
preset2_button = Button("Preset 2", (WIDTH - 120, 20+hollow_box_button), 200, 50, 10, lambda: load_preset("Preset 2"))
preset3_button = Button("Preset 3", (WIDTH - 120, 20+hollow_box_button*2), 200, 50, 10, lambda: load_preset("Preset 3"))
preset4_button = Button("Preset 4", (WIDTH - 120, 20+hollow_box_button*3), 200, 50, 10, lambda: load_preset("Preset 4"))
preset5_button = Button("Preset 5", (WIDTH - 120, 20+hollow_box_button*4), 200, 50, 10, lambda: load_preset("Preset 5"))
gosper_glider_gun_button = Button("Gosper Gun", (WIDTH - 120, 20+hollow_box_button*5), 200, 50, 10, load_gosper_glider_gun)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Gestion du placement manuel des cellules avec le clic de la souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not simulation_running:
                    placing_cells = True
                    x, y = pygame.mouse.get_pos()
                    # Ajuster les coordonnées en fonction du zoom et du déplacement du viewport
                    x -= viewport_x
                    y -= viewport_y
                    x //= int(CELL_SIZE * zoom_factor)
                    y //= int(CELL_SIZE * zoom_factor)
                    x, y = int(x), int(y)
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if grid[x, y] == 1:
                            grid[x, y] = 0  # Supprimer la cellule si elle existe
                        else:
                            grid[x, y] = 1  # Placer la cellule si elle n'existe pas
                else:
                    panning = True
                    pan_start_x, pan_start_y = event.pos

            if event.button == 3:  # Clic droit
                panning = True
                pan_start_x, pan_start_y = event.pos

            if event.button == 4:  # Molette vers le haut pour zoomer
                zoom_factor *= 1.1
                # Ajuster la position du viewport pour centrer le zoom
                viewport_x = zoom_center_x - (zoom_center_x - viewport_x) * 1.1
                viewport_y = zoom_center_y - (zoom_center_y - viewport_y) * 1.1

            elif event.button == 5:  # Molette vers le bas pour dézoomer
                zoom_factor /= 1.1
                # Ajuster la position du viewport pour centrer le dézoom
                viewport_x = zoom_center_x - (zoom_center_x - viewport_x) / 1.1
                viewport_y = zoom_center_y - (zoom_center_y - viewport_y) / 1.1
                # Limiter le zoom minimal
                if zoom_factor < min_zoom:
                    zoom_factor = min_zoom

        elif event.type == pygame.MOUSEBUTTONUP:
            placing_cells = False

            # Arrêter le déplacement avec le clic de la souris droit relâché
            if event.button in [1, 3]:
                panning = False

        # Gérer les touches du clavier pour le zoom
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_simulation()

            # Réinitialiser la grille en appuyant sur la touche R
            if event.key == pygame.K_r:
                reset_grid()

            # Utiliser "+" pour zoomer
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                zoom_factor *= 1.1

            # Utiliser "-" pour dézoomer
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                zoom_factor /= 1.1
                # Limiter le zoom minimal
                if zoom_factor < min_zoom:
                    zoom_factor = min_zoom

    # Placement manuel des cellules lorsque le clic de la souris est enfoncé
    if placing_cells:
        x, y = pygame.mouse.get_pos()
        x -= viewport_x
        y -= viewport_y
        x //= int(CELL_SIZE * zoom_factor)
        y //= int(CELL_SIZE * zoom_factor)
        x, y = int(x), int(y)
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            grid[x, y] = 1

    # Gestion du déplacement avec le clic droit de la souris enfoncé
    if panning:
        x, y = pygame.mouse.get_pos()
        dx, dy = x - pan_start_x, y - pan_start_y
        viewport_x += dx
        viewport_y += dy
        pan_start_x, pan_start_y = x, y

    # Mise à jour de la grille si la simulation est en cours
    if simulation_running:
        grid = update_grid(grid)

    # Affichage de la grille
    screen.fill(BLACK)

    # Dessiner un rectangle autour de la grille
    grid_rect = pygame.Rect(viewport_x, viewport_y, GRID_SIZE * CELL_SIZE * zoom_factor,
                            GRID_SIZE * CELL_SIZE * zoom_factor)
    pygame.draw.rect(screen, WHITE, grid_rect, 1)

    # Affichage de la grille avec zoom et déplacement
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_x = x * int(CELL_SIZE * zoom_factor) + viewport_x
            cell_y = y * int(CELL_SIZE * zoom_factor) + viewport_y
            cell_radius = int(CELL_SIZE * zoom_factor) // 2
            if grid[x, y] == 1:
                pygame.draw.circle(screen, GREEN, (cell_x + cell_radius, cell_y + cell_radius), cell_radius)

    # Dessiner les boutons
    preset1_button.draw(screen)
    preset2_button.draw(screen)
    preset3_button.draw(screen)
    preset4_button.draw(screen)
    preset5_button.draw(screen)
    gosper_glider_gun_button.draw(screen)

    # Calculer les FPS
    fps = int(clock.get_fps())

    # Afficher les FPS en haut à gauche de l'écran
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()