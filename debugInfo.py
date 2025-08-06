import pygame

class DebugInfo:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.debug_lines = []
        self.visible = True  # Toggle with a key if needed (like F3)

    def add(self, label: str, value):
        self.debug_lines.append(f"{label}: {value}")

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return

        for i, line in enumerate(self.debug_lines):
            text_surf = self.font.render(line, True, (0, 255, 0))
            text_rect = text_surf.get_rect(topleft=(10, 10 + i * 18))
            pygame.draw.rect(surface, (0,0,0), text_rect)
            surface.blit(text_surf, (text_rect))
            

        self.debug_lines.clear()  # Reset each frame
