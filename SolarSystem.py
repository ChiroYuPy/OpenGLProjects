import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


class CelestialBody:
    def __init__(self, radius, color, distance, speed):
        self.radius = radius
        self.color = color
        self.distance = distance
        self.angle = random.uniform(0, 360)
        self.speed = speed

    def update(self):
        self.angle += self.speed
        self.angle %= 360

    def get_position(self):
        x = self.distance * math.cos(math.radians(self.angle))
        y = self.distance * math.sin(math.radians(self.angle))
        return (x, y, 0)


def draw_celestial_body(body):
    glPushMatrix()
    glTranslatef(*body.get_position())

    if body.color == (1, 1, 0):
        glMaterialfv(GL_FRONT, GL_EMISSION, (1, 1, 0, 1))
    else:
        glColor3fv(body.color)

    draw_sphere(body.radius, 16, 16)

    if body.color == (1, 1, 0):
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

    glPopMatrix()


def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    sun = CelestialBody(2, (1, 1, 0), 0, 0)
    planets = [
        CelestialBody(0.5, (0, 0, 1), 5, 1),
        CelestialBody(0.3, (0, 1, 0), 8, 0.5),
        CelestialBody(0.3, (0, 1, 0), 8, 0.5),
        CelestialBody(0.2, (0, 1, 0), 8, 0.5),
        CelestialBody(0.6, (0, 1, 0), 8, 0.5),
        CelestialBody(0.5, (0, 1, 0), 8, 0.5),
    ]

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [*sun.get_position(), 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        light_position = [*sun.get_position(), 0]  # Position de la source de lumière au même endroit que le soleil
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        light_position_emit = [*sun.get_position(),
                               1.0]  # Position de la source de lumière émise au même endroit que le soleil
        glLightfv(GL_LIGHT1, GL_POSITION, light_position_emit)

        ambient_color = [0.2, 0.2, 0.2, 1]
        diffuse_color = [1, 1, 1, 1]
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color)

        draw_celestial_body(sun)
        for planet in planets:
            draw_celestial_body(planet)
            planet.update()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
