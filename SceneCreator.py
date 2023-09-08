import pygame
import tkinter as tk
from tkinter import ttk
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pi

cubes = []
selected_cube_index = -1

spheres = []
selected_sphere_index = -1

class Cube:
    def __init__(self, x, y, z, w, h, d):
        self.x, self.y, self.z = x / 4, y / 4, z / 4
        self.w, self.h, self.d = w / 4, h / 4, d / 4
        self.rot_x, self.rot_y, self.rot_z = 0.0, 0.0, 0.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_z, 0, 0, 1)

        vertices = [
            (self.w, self.h, -self.d),
            (self.w, self.h, self.d),
            (-self.w, self.h, self.d),
            (-self.w, self.h, -self.d),
            (self.w, -self.h, -self.d),
            (self.w, -self.h, self.d),
            (-self.w, -self.h, self.d),
            (-self.w, -self.h, -self.d)
        ]

        edges = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()

    def set_rotation(self, x, y, z):
        self.rot_x = x
        self.rot_y = y
        self.rot_z = z

    def get_rotation(self):
        return self.rot_x, self.rot_y, self.rot_z


class Sphere:
    def __init__(self, x, y, z, radius):
        self.x, self.y, self.z = x / 4, y / 4, z / 4
        self.radius = radius / 4
        self.rot_x, self.rot_y, self.rot_z = 0.0, 0.0, 0.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_z, 0, 0, 1)

        glColor3f(1, 0, 0)  # Set sphere color to red
        gluSphere(gluNewQuadric(), self.radius, 32, 32)  # Render the sphere

        glPopMatrix()

    def set_rotation(self, x, y, z):
        self.rot_x = x
        self.rot_y = y
        self.rot_z = z

    def get_rotation(self):
        return self.rot_x, self.rot_y, self.rot_z


# Initialisation de Pygame
pygame.init()

# Configuration de Pygame
display = (960, 960)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST)
gluPerspective(45, (display[0] / display[1]), 0.1, 100)
glTranslatef(0.0, 0.0, -32)

def update_object_list():
    cube_list.delete(0, tk.END)
    for idx, cube in enumerate(cubes):
        cube_list.insert(tk.END, f"Cube {idx}: X={cube.x} Y={cube.y} Z={cube.z} W={cube.w} H={cube.h} D={cube.d}")

    sphere_list.delete(0, tk.END)
    for idx, sphere in enumerate(spheres):
        sphere_list.insert(tk.END, f"Sphere {idx}: X={sphere.x} Y={sphere.y} Z={sphere.z} Radius={sphere.radius}")


def update_cube_list():
    cube_list.delete(0, tk.END)
    for idx, cube in enumerate(cubes):
        cube_list.insert(tk.END, f"Cube {idx}: X={cube.x} Y={cube.y} Z={cube.z} W={cube.w} H={cube.h} D={cube.d}")

def add_cube():
    try:
        new_cube = Cube(float(x_slider.get()), float(y_slider.get()), float(z_slider.get()),
                        float(w_slider.get()), float(h_slider.get()), float(d_slider.get()))
        cubes.append(new_cube)
        update_object_list()  # Update the list after adding
    except ValueError:
        print("Veuillez entrer des valeurs numériques valides.")

def add_sphere():
    try:
        new_sphere = Sphere(float(x_slider.get()), float(y_slider.get()), float(z_slider.get()),
                            float(radius_slider.get()))
        spheres.append(new_sphere)
        update_object_list()  # Update the list after adding
    except ValueError:
        print("Veuillez entrer des valeurs numériques valides.")

def add_selected_object():
    selected_object_type = object_type_var.get()
    if selected_object_type == "Cube":
        add_cube()
    elif selected_object_type == "Sphere":
        add_sphere()
    update_object_list()


def update_sphere_list():
    sphere_list.delete(0, tk.END)
    for idx, sphere in enumerate(spheres):
        sphere_list.insert(tk.END, f"Sphere {idx}: X={sphere.x} Y={sphere.y} Z={sphere.z} Radius={sphere.radius}")

def load_selected_cube_params(event):
    global selected_cube_index
    selected_index = cube_list.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        selected_cube_index = selected_index
        selected_cube = cubes[selected_index]

        x_slider.set(selected_cube.x * 4)
        y_slider.set(selected_cube.y * 4)
        z_slider.set(selected_cube.z * 4)
        w_slider.set(selected_cube.w * 4)
        h_slider.set(selected_cube.h * 4)
        d_slider.set(selected_cube.d * 4)
        rot_x_slider.set(selected_cube.rot_x)
        rot_y_slider.set(selected_cube.rot_y)
        rot_z_slider.set(selected_cube.rot_z)

def load_selected_sphere_params(event):
    global selected_sphere_index
    selected_index = sphere_list.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        selected_sphere_index = selected_index
        selected_sphere = spheres[selected_index]

        x_slider.set(selected_sphere.x * 4)
        y_slider.set(selected_sphere.y * 4)
        z_slider.set(selected_sphere.z * 4)
        radius_slider.set(selected_sphere.radius * 4)
        rot_x_slider.set(selected_sphere.rot_x)
        rot_y_slider.set(selected_sphere.rot_y)
        rot_z_slider.set(selected_sphere.rot_z)

def update_selected_cube_params(event):
    global selected_cube_index
    if selected_cube_index >= 0 and selected_cube_index < len(cubes):
        selected_cube = cubes[selected_cube_index]
        selected_cube.x = x_slider.get() / 4
        selected_cube.y = y_slider.get() / 4
        selected_cube.z = z_slider.get() / 4
        selected_cube.w = w_slider.get() / 4
        selected_cube.h = h_slider.get() / 4
        selected_cube.d = d_slider.get() / 4
        selected_cube.rot_x = rot_x_slider.get()
        selected_cube.rot_y = rot_y_slider.get()
        selected_cube.rot_z = rot_z_slider.get()

def update_selected_sphere_params(event):
    global selected_sphere_index
    if selected_sphere_index >= 0 and selected_sphere_index < len(spheres):
        selected_sphere = spheres[selected_sphere_index]
        selected_sphere.x = x_slider.get() / 4
        selected_sphere.y = y_slider.get() / 4
        selected_sphere.z = z_slider.get() / 4
        selected_sphere.radius = radius_slider.get() / 4
        selected_sphere.rot_x = rot_x_slider.get()
        selected_sphere.rot_y = rot_y_slider.get()
        selected_sphere.rot_z = rot_z_slider.get()

# Fonction pour supprimer le cube sélectionné
def delete_selected_cube():
    global selected_cube_index
    if selected_cube_index >= 0 and selected_cube_index < len(cubes):
        cubes.pop(selected_cube_index)
        selected_cube_index = -1
        update_cube_list()
        load_selected_cube_params()

# Fonction pour activer/désactiver la rotation de la caméra
def toggle_camera_rotation():
    global camera_rotation
    camera_rotation = not camera_rotation

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Modifier des cubes en 3D")
root.geometry("480x640")

# Liste des cubes existants
cube_list = tk.Listbox(root)
cube_list.pack(fill=tk.BOTH, expand=True)

# Liste des shperes existants
sphere_list = tk.Listbox(root)
sphere_list.pack(fill=tk.BOTH, expand=True)

# Frame pour les sliders de cube
cube_frame = tk.Frame(root)
cube_frame.pack(side=tk.LEFT)

x_slider = ttk.Scale(cube_frame, from_=-50, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
x_slider.grid(row=0, column=1, padx=10, pady=5)
x_value_label = ttk.Label(cube_frame, text="0")
x_value_label.grid(row=0, column=2, padx=10, pady=5)

y_slider = ttk.Scale(cube_frame, from_=-50, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
y_slider.grid(row=1, column=1, padx=10, pady=5)
y_value_label = ttk.Label(cube_frame, text="0")
y_value_label.grid(row=1, column=2, padx=10, pady=5)

z_slider = ttk.Scale(cube_frame, from_=-50, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
z_slider.grid(row=2, column=1, padx=10, pady=5)
z_value_label = ttk.Label(cube_frame, text="0")
z_value_label.grid(row=2, column=2, padx=10, pady=5)

w_slider = ttk.Scale(cube_frame, from_=0, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
w_slider.grid(row=3, column=1, padx=10, pady=5)
w_value_label = ttk.Label(cube_frame, text="0")
w_value_label.grid(row=3, column=2, padx=10, pady=5)

h_slider = ttk.Scale(cube_frame, from_=0, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
h_slider.grid(row=4, column=1, padx=10, pady=5)
h_value_label = ttk.Label(cube_frame, text="0")
h_value_label.grid(row=4, column=2, padx=10, pady=5)

d_slider = ttk.Scale(cube_frame, from_=0, to=50, orient=tk.HORIZONTAL, command=update_selected_cube_params)
d_slider.grid(row=5, column=1, padx=10, pady=5)
d_value_label = ttk.Label(cube_frame, text="0")
d_value_label.grid(row=5, column=2, padx=10, pady=5)

rot_x_slider = ttk.Scale(cube_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=update_selected_cube_params)
rot_x_slider.grid(row=6, column=1, padx=10, pady=5)
rot_x_value_label = ttk.Label(cube_frame, text="0")
rot_x_value_label.grid(row=6, column=2, padx=10, pady=5)

rot_y_slider = ttk.Scale(cube_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=update_selected_cube_params)
rot_y_slider.grid(row=7, column=1, padx=10, pady=5)
rot_y_value_label = ttk.Label(cube_frame, text="0")
rot_y_value_label.grid(row=7, column=2, padx=10, pady=5)

rot_z_slider = ttk.Scale(cube_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=update_selected_cube_params)
rot_z_slider.grid(row=8, column=1, padx=10, pady=5)
rot_z_value_label = ttk.Label(cube_frame, text="0")
rot_z_value_label.grid(row=8, column=2, padx=10, pady=5)

def update_value_labels():
    x_value_label.config(text="{:.3f}".format(x_slider.get()))
    y_value_label.config(text="{:.3f}".format(y_slider.get()))
    z_value_label.config(text="{:.3f}".format(z_slider.get()))
    w_value_label.config(text="{:.3f}".format(w_slider.get()))
    h_value_label.config(text="{:.3f}".format(h_slider.get()))
    d_value_label.config(text="{:.3f}".format(d_slider.get()))
    rot_x_value_label.config(text="{:.3f}".format(rot_x_slider.get()))
    rot_y_value_label.config(text="{:.3f}".format(rot_y_slider.get()))
    rot_z_value_label.config(text="{:.3f}".format(rot_z_slider.get()))



rot_labels = ["Rotation X", "Rotation Y", "Rotation Z"]

for i, label_text in enumerate(rot_labels):
    label = ttk.Label(cube_frame, text=label_text)
    label.grid(row=i + 6, column=0, padx=10, pady=5)

# Labels pour les sliders
labels = ["X", "Y", "Z", "Largeur", "Hauteur", "Profondeur"]

# Créer des labels pour chaque slider
for i, label_text in enumerate(labels):
    label = ttk.Label(cube_frame, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5)

radius_slider = ttk.Scale(cube_frame, from_=0, to=25, orient=tk.HORIZONTAL, command=update_selected_sphere_params)
radius_slider.grid(row=9, column=1, padx=10, pady=5)
radius_value_label = ttk.Label(cube_frame, text="0")
radius_value_label.grid(row=9, column=2, padx=10, pady=5)

radius_label = ttk.Label(cube_frame, text="Rayon")
radius_label.grid(row=9, column=0, padx=10, pady=5)

# Bouton pour supprimer un cube
delete_button = ttk.Button(root, text="Supprimer", command=delete_selected_cube)
delete_button.pack()

# Bouton pour activer/désactiver la rotation de la caméra
camera_rotation = False
toggle_rotation_button = ttk.Button(root, text="Activer/Désactiver Rotation Caméra", command=toggle_camera_rotation)
toggle_rotation_button.pack()

# Create the dropdown menu for object types
object_type_var = tk.StringVar()
object_type_options = ["Cube", "Sphere"]
object_type_menu = ttk.Combobox(cube_frame, textvariable=object_type_var, values=object_type_options)
object_type_menu.grid(row=10, column=0, columnspan=3, pady=10)

# Create the "Ajouter Objet" button
add_object_button = ttk.Button(cube_frame, text="Ajouter Objet", command=add_selected_object)
add_object_button.grid(row=11, column=0, columnspan=3, pady=10)

def add_selected_object():
    selected_object_type = object_type_var.get()
    if selected_object_type == "Cube":
        add_cube()
        show_cube_sliders()
        hide_sphere_sliders()
    elif selected_object_type == "Sphere":
        add_sphere()
        show_sphere_sliders()
        hide_cube_sliders()
    update_object_list()

def show_cube_sliders():
    for slider in cube_sliders:
        slider.grid()

def hide_cube_sliders():
    for slider in cube_sliders:
        slider.grid_remove()

def show_sphere_sliders():
    for slider in sphere_sliders:
        slider.grid()

def hide_sphere_sliders():
    for slider in sphere_sliders:
        slider.grid_remove()

# Créer les sliders pour les paramètres du cube
cube_sliders = [
    x_slider, y_slider, z_slider,
    w_slider, h_slider, d_slider,
    rot_x_slider, rot_y_slider, rot_z_slider
]

# Créer les sliders pour les paramètres de la sphère
sphere_sliders = [
    x_slider, y_slider, z_slider,
    radius_slider
]

# Fonction appelée lors de la sélection d'un élément dans la liste
def on_cube_list_select(event):
    load_selected_cube_params()

cube_list.bind('<<ListboxSelect>>', load_selected_cube_params)
sphere_list.bind('<<ListboxSelect>>', load_selected_sphere_params)

# Boucle principale pour la fenêtre Tkinter
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    update_value_labels()

    if camera_rotation:
        glRotatef(1, 0, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for cube in cubes:
        cube.draw()

    for sphere in spheres:
        sphere.draw()

    pygame.display.flip()
    pygame.time.wait(10)

    root.update()