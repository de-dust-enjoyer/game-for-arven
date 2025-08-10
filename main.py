import pygame
from game_state_manager import GameStateManager
from level import Level
from menu import Menu
from pause import Pause
from end import End
from nothing import Nothing
from debugInfo import DebugInfo

class Game:
	def __init__(self):
		# initialization:
		pygame.init()
		self.screensize:tuple = (1920, 1016)
		self.screen = pygame.display.set_mode(self.screensize, pygame.RESIZABLE)
		pygame.display.set_caption("Happy Birthday Arwen!")
		self.fps:int = 60
		self.clock = pygame.time.Clock()
		
		# game state manager and states
		self.transition_group = pygame.sprite.Group()
		self.game_state_manager = GameStateManager("nothing", self.transition_group)
		self.menu = Menu(self.screen, self.game_state_manager)
		self.level = Level(self.screen, self.game_state_manager)
		self.pause = Pause(self.screen, self.game_state_manager)
		self.end = End(self.screen, self.game_state_manager)
		self.nothing = Nothing(self.screen, self.game_state_manager)

		self.states = {"level": self.level, "menu": self.menu, "pause": self.pause, "end": self.end, "nothing": self.nothing}

		self.debug_info = DebugInfo(pygame.font.Font("assets/font/pixel_font.otf", 10))
						


	def run(self):
		self.game_state_manager.transition_state("menu")
		while True:
			self.clock.tick(self.fps)

			self.states[self.game_state_manager.get_state()].run()
			self.debug_info.add("fps: " ,self.clock.get_fps())

			self.transition_group.update()

			self.debug_info.render(self.screen)
			self.transition_group.draw(self.screen)
			

			pygame.display.flip()
					

if __name__ == "__main__":
	game = Game()
	game.run()