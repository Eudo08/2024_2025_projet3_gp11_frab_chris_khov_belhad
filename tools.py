import pygame

NOIR = (0, 0, 0)

class Button: 
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw (self, surface):
        current_color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, NOIR, self.rect, 2)

        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, NOIR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def uptate (self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def che_clicked (self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked