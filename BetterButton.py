import pygame


class Button:
    def __init__(self, text, pos, width, height, elevation, command=None):

        gui_font = pygame.font.Font(None, 26)

        # Core attributes
        self.pressed = False
        self.command = command
        self.elevation = elevation
        self.dynamyc_elevation = elevation
        self.original_y_position = pos[1]

        # Calculate the position to center the button
        x = pos[0] - width / 2
        y = pos[1] - height / 2

        # Top rectangle
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect((x, y), (width, elevation))
        self.bottom_color = '#354B5E'

        # Text
        self.text_surf = gui_font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_position - self.dynamyc_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamyc_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamyc_elevation = 0
                if self.command:
                    self.command()
                self.pressed = True
            else:
                self.dynamyc_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
        else:
            self.dynamyc_elevation = self.elevation
            self.top_color = '#475F77'
