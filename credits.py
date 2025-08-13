import pygame
import sys
from os.path import join

class Credits:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager
        self.font = pygame.font.Font(join("assets", "font", "pixel_font.otf"), 50)  # Bigger font
        self.scroll_speed = 0.7 # Pixels per frame
        self.offset = self.screen.get_height() + 100  # Start below screen
        self.done = True

        # Long Lorem Ipsum text
        lorem = (
            "Hi hier ist Simon. "
            "Ich hoffe das kleine Game hat dir gefallen und du hast nicht zu schlimm geraged. "
            "Es tut mit leid das du es erst Verspätet erhällst. "
            "Als ich die Idee dazu hatte wollte ich eigentlich nur ein kleines Minigame für dich erstellen. "
            "Das ist dann etwas aus dem Ruder gelaufen und ich habe dann doch sehr lange daran gearbeitet. "
            "Der Kino Gutschein ist generell nicht ein physischer Gutschein sondern ein Versprechen das ich dich "
            "wenn du Lust hast ins Kino einlade (mit allem was dazugehört). "
            "Da es ja anscheinend Jahre dauert bis in diesen komischen cadilac-kino "
            "mal ein cooler Film läuft habe ich mir gedacht dass das doch eine gute Idee ist. "
            "Ich wünsche dir nochmal alles Gute nachträglich zum Geburtstag. Bleib so wie du bist "
            "Ich hoffe wir sehen uns bald wieder!. ich liebe dich <3 . . . . . . . . "

            "[Beliebige Taste drücken]"
        )

        # Split into lines for rendering
        self.credits_lines = self.wrap_text(lorem, self.font, self.screen.get_width() - 600)

        self.running = True

    def wrap_text(self, text, font, max_width):
        """Split text into lines that fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.done:
                self.running = False
                self.game_state_manager.transition_state("menu")

        self.screen.fill((27,28,40))

        # Render scrolling text
        for i, line in enumerate(self.credits_lines):
            y = self.offset + i * 60  # 60 pixels between lines
            text_surface = self.font.render(line, False, "white")
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y))

            self.done = True if text_rect.bottom < self.screen.get_height() else False
            self.screen.blit(text_surface, text_rect)


        self.offset -= self.scroll_speed

        pygame.display.flip()
