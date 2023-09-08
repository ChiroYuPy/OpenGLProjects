import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

fractal_shader_sources = [
    # Fractal 0: Mandelbrot
    {
        "fragment_shader": """
            #version 330
            uniform vec2 resolution;
            uniform vec2 center;
            uniform float scale;

            vec3 getColor(int iterations) {
                float t = float(iterations) / 100.0;
                vec3 color = vec3(t, t*t, t*t*t);  // Un exemple de dégradé, vous pouvez ajuster les valeurs
                return color;
            }

            void main()
            {
                vec2 uv = (gl_FragCoord.xy - 0.5 * resolution) / resolution;
                uv = center + uv * scale;

                vec2 c = uv;
                vec2 z = c;

                int iterations = 0;
                for (int i = 0; i < 100; i++) {
                    if (length(z) > 2.0) {
                        break;
                    }
                    z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
                    iterations = i;
                }

                vec3 color = getColor(iterations);
                gl_FragColor = vec4(color, 1.0);
            }

        """
    },
    # Fractal 1: Julia
    {
        "fragment_shader": """
        #version 330
        uniform vec2 resolution;
        uniform vec2 center;
        uniform float scale;

        vec3 getColor(int iterations) {
            float t = float(iterations) / 100.0;
            vec3 color = vec3(t*t, t, t*t*t);  // Same gradient as Mandelbrot
            return color;
        }

        void main()
        {
            vec2 uv = (gl_FragCoord.xy - 0.5 * resolution) / resolution;
            uv = center + uv * scale;

            vec2 c = vec2(-0.7, 0.27015);  // Julia fractal constant
            vec2 z = uv;

            int iterations = 0;
            for (int i = 0; i < 100; i++) {
                if (length(z) > 2.0) {
                    break;
                }
                z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
                iterations = i;
            }

            vec3 color = getColor(iterations);
            gl_FragColor = vec4(color, 1.0);
        }
        """
    },
    # Fractal 2: Burning Ship
    {
        "fragment_shader": """
            #version 330
            uniform vec2 resolution;
            uniform vec2 center;
            uniform float scale;

            vec3 getColor(int iterations) {
                float t = float(iterations) / 100.0;
                vec3 color = vec3(t*t, t, t*t*t);  // Another gradient example
                return color;
            }

            void main()
            {
                vec2 uv = (gl_FragCoord.xy - 0.5 * resolution) / resolution;
                uv = center + uv * scale;

                vec2 c = uv;
                vec2 z = c;

                int iterations = 0;
                for (int i = 0; i < 100; i++) {
                    if (length(z) > 2.0) {
                        break;
                    }
                    z = vec2(z.x * z.x - z.y * z.y, 2.0 * abs(z.x * z.y)) + c;
                    iterations = i;
                }

                vec3 color = getColor(iterations);
                gl_FragColor = vec4(color, 1.0);
            }
        """
    }
]

# Initialize Pygame
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Compile le vertex shader et le fragment shader
vertex_shader = """
#version 330
layout(location = 0) in vec4 position;
void main()
{
    gl_Position = position;
}
"""

# Fragment shader pour le rendu progressif
fragment_shader_progressive = """
    #version 330
    uniform vec2 resolution;
    uniform vec2 center;
    uniform float scale;
    uniform float progressive_detail;

    vec3 getColor(int iterations) {
        float t = float(iterations) / 100.0;
        vec3 color = vec3(t, t*t, t*t*t);  // Un exemple de dégradé, vous pouvez ajuster les valeurs
        return color;
    }

    void main()
    {
        vec2 uv = (gl_FragCoord.xy - 0.5 * resolution) / resolution;
        uv = center + uv * scale;

        vec2 c = uv;
        vec2 z = c;

        int iterations = 0;
        int max_iterations = int(progressive_detail);

        for (int i = 0; i < max_iterations; i++) {
            if (length(z) > 2.0) {
                break;
            }
            z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
            iterations = i;
        }

        vec3 color = getColor(iterations);
        gl_FragColor = vec4(color, 1.0);
    }
"""

fractal_type = 0

# Définition des paramètres de la vue
center = np.array([0.0, 0.0], dtype=np.float32)
scale = 1.0
dragging = False
prev_mouse_pos = None
divisor = (width+height)/2
drag_speed = 1/divisor

current_fractal_source = fractal_shader_sources[fractal_type]

# Initialize the shader variable with the initial fractal's shader
shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(current_fractal_source["fragment_shader"], GL_FRAGMENT_SHADER)
)
glUseProgram(shader)
min_progressive_zoom = 1000.0

running = True
while running:
    # Rendu progressif
    if scale > min_progressive_zoom:
        progressive_detail = (scale - min_progressive_zoom) * 1000.0  # Ajustez le facteur selon vos besoins
        glUniform1f(glGetUniformLocation(shader, "progressive_detail"), progressive_detail)
    else:
        glUniform1f(glGetUniformLocation(shader, "progressive_detail"), 100.0)  # Niveau de détail maximum

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle window resizing
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            glViewport(0, 0, width, height)
            aspect_ratio = width / height
            scale_y = scale
            scale_x = scale * aspect_ratio
            glUniform2f(glGetUniformLocation(shader, "resolution"), width, height)
            glUniform2f(glGetUniformLocation(shader, "center"), *center)
            glUniform1f(glGetUniformLocation(shader, "scale"), scale_x, scale_y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette vers le haut (zoom in)
                scale *= 0.9
            elif event.button == 5:  # Molette vers le bas (zoom out)
                scale *= 1.1
            elif event.button == 1:  # Bouton gauche enfoncé (commence le déplacement)
                dragging = True
                prev_mouse_pos = np.array(event.pos)
            elif event.button == 3:  # Bouton droit enfoncé (incrémente fractal_type)
                fractal_type = (fractal_type + 1) % len(fractal_shader_sources)
                current_fractal_source = fractal_shader_sources[fractal_type]
                glDeleteProgram(shader)
                shader = compileProgram(
                    compileShader(vertex_shader, GL_VERTEX_SHADER),
                    compileShader(current_fractal_source["fragment_shader"], GL_FRAGMENT_SHADER)
                )
                glUseProgram(shader)
                # Reset the view parameters when switching fractals
                center = np.array([0.0, 0.0], dtype=np.float32)
                scale = 1.0

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Bouton gauche relâché (arrête le déplacement)
                dragging = False

    if dragging:
        current_mouse_pos = np.array(pygame.mouse.get_pos())
        delta = (current_mouse_pos - prev_mouse_pos) * np.array([1, -1]) * drag_speed
        center -= delta * scale
        prev_mouse_pos = current_mouse_pos

    # Met à jour les uniformes du shader
    glUniform2f(glGetUniformLocation(shader, "resolution"), width, height)
    glUniform2f(glGetUniformLocation(shader, "center"), *center)
    glUniform1f(glGetUniformLocation(shader, "scale"), scale)

    # Efface l'écran
    glClear(GL_COLOR_BUFFER_BIT)

    # Dessine un rectangle avec le shader
    vertices = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype=np.float32)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, vertices)
    glEnableVertexAttribArray(0)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glDisableVertexAttribArray(0)

    pygame.display.flip()

pygame.quit()
