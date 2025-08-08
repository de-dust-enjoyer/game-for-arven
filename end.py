import pygame, sys
from os.path import join

class End:
	def __init__(self, screen, game_state_manager):
		self.screen = screen
		self.game_state_manager = game_state_manager

		self.img = pygame.image.load(join("assets", "ui", "end.png")).convert()

	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
		self.screen.blit(self.img, (0,0))