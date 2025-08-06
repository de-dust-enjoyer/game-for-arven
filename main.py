import pygame

from game_state_manager import GameStateManager
from level import Level
from menu import Menu
from debugInfo import DebugInfo

class Game:
	def __init__(self):
		# initialization:
		pygame.init()
		self.screensize:tuple = (960, 540)
		self.screen = pygame.display.set_mode(self.screensize)
		pygame.display.set_caption("Happy Birthday Arwen!")
		self.fps:int = 60
		self.clock = pygame.time.Clock()
		
		# game state manager and states
		self.game_state_manager = GameStateManager("menu")
		self.menu = Menu(self.screen, self.game_state_manager)
		self.level = Level(self.screen, self.game_state_manager)

		self.states = {"level": self.level, "menu": self.menu}

		self.debug_info = DebugInfo(pygame.font.Font("assets/font/pixel_font.otf", 10))
						


	def run(self):
		while True:
			self.clock.tick(self.fps)

			self.states[self.game_state_manager.get_state()].run()
			self.debug_info.add("fps: " ,self.clock.get_fps())

			self.debug_info.render(self.screen)
			pygame.display.flip()
					



# if the name of the main file is "main" create the game and run it!
if __name__ == "__main__":
	game = Game()
	game.run()