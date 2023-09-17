import pygame
from pygame.locals import *
import pymunk
import random
import math

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
width, height = 1280, 720
display = (width, height)
screen = pygame.display.set_mode(display, DOUBLEBUF)

# Configuration de l'espace Pymunk
space = pymunk.Space()
space.gravity = (0, -100)  # Gravité vers le bas (ajustez selon vos préférences)


# Création d'une forme physique pour les particules
def create_particle(x, y):
    mass = 1
    radius = 10
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8  # Élasticité (collision rebondissante)
    space.add(body, shape)
    return shape


# Création d'une contrainte pour empêcher les particules d'aller en dessous du bas de l'écran
bottom = pymunk.Segment(space.static_body, (0, 10), (width, 10), 10)
space.add(bottom)

# Création de particules
num_particles = 100
particles = []

for _ in range(num_particles):
    x = random.uniform(20, width - 20)
    y = random.uniform(20, height - 20)
    particle = create_particle(x, y)
    # Réduction de la vitesse initiale
    particle.body.velocity = (0, random.uniform(-50, 50))
    particles.append(particle)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour la physique
    dt = 1.0 / 60.0
    for _ in range(10):
        space.step(dt)

    screen.fill((0, 0, 0))  # Effacer l'écran

    # Dessiner les particules avec des couleurs basées sur la proximité
    for particle in particles:
        pos_x, pos_y = particle.body.position
        angle = math.degrees(particle.body.angle)

        # Comptez le nombre de particules à moins de 20 pixels
        count_nearby = sum(1 for p in particles if p != particle and
                           math.sqrt((p.body.position.x - pos_x) ** 2 + (p.body.position.y - pos_y) ** 2) < 20)

        # Déterminez la couleur en fonction du nombre de particules voisines
        color = (count_nearby * 10, 0, 255 - count_nearby * 10)

        pygame.draw.circle(screen, color, (int(pos_x), int(height - pos_y)), 10)

    pygame.display.flip()
    clock.tick(60)  # Limiter la vitesse de rafraîchissement à 60 images par seconde

pygame.quit()
