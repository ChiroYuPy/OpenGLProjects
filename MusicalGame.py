import pygame
import math

blanc = (255, 255, 255)
noir = (0, 0, 0)

# Angles en radians
tiles = [0, math.radians(90), math.radians(45), math.radians(135), math.radians(-90), math.radians(-45), math.radians(90)]

pygame.init()
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de Musique")


class Tile(pygame.sprite.Sprite):
    def __init__(self, previous_tile_x, previous_tile_y, direction):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(blanc)
        self.rect = self.image.get_rect()
        self.rect.x = previous_tile_x + 10 * math.cos(direction)  # Calcul des nouvelles coordonnées X
        self.rect.y = previous_tile_y + 10 * math.sin(direction)  # Calcul des nouvelles coordonnées Y
        self.direction = direction

# Création d'un groupe de sprites pour les tuiles
all_sprites = pygame.sprite.Group()

# Position initiale
x, y = 100, 300

# Création des tuiles à partir de la liste 'tiles'
for direction in tiles:
    tile = Tile(x, y, direction)
    all_sprites.add(tile)

    # La tuile suivante sera positionnée en fonction de la tuile précédente
    x, y = tile.rect.x, tile.rect.y

    # Avancer de 60 pixels horizontalement pour la prochaine tuile
    x += 60

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacement de l'écran
    fenetre.fill(noir)

    # Mise à jour et dessin des tuiles
    all_sprites.draw(fenetre)

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(60)

pygame.quit()
