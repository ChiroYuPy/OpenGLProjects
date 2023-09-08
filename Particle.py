import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Initialisation de Pygame et OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)


# Fonction pour créer une particule
def create_particle():
    return {
        'position': [random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)],
        'velocity': [random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)]
    }


particles = [create_particle() for _ in range(3000)]

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Gestion du déplacement des particules par la souris
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_rel()
        for particle in particles:
            particle['position'][0] += x / 500
            particle['position'][1] -= y / 500

    glBegin(GL_POINTS)
    for particle in particles:
        glVertex3fv(particle['position'])
        for i in range(3):
            particle['position'][i] += particle['velocity'][i]
            if particle['position'][i] > 2 or particle['position'][i] < -2:
                particle['velocity'][i] *= -1
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
