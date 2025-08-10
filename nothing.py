import pygame, sys

class Nothing:
	def __init__(self, screen, game_state_manager):
		self.screen = screen
		self.game_state_manager = game_state_manager

	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


		self.screen.fill("black")
		pygame.display.flip()