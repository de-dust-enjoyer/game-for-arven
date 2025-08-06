import pygame, sys
from button import Button


class Menu:
	def __init__(self, screen, game_state_manager):
		self.screen = screen
		self.game_state_manager = game_state_manager
		self.clicked = False

		self.button_group = pygame.sprite.Group()

		self.start_button = Button("PLAY", (self.screen.get_width()/2, self.screen.get_height()/2), 
				centered=True, method=self.game_state_manager.set_state, arg="level")
		self.button_group.add(self.start_button)

		self.quit_button = Button("QUIT", (self.start_button.rect.centerx, self.start_button.rect.bottom + 100),
				centered=True, method=self.terminate)
		self.button_group.add(self.quit_button)

	def run(self):
		mouse_button_up_event = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.terminate()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					pass
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					pass
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					pass
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					pass
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				mouse_button_up_event = event

		# game logic:
		self.button_group.update(mouse_button_up_event)


		# rendering:
		self.screen.fill("lightblue")
		self.button_group.draw(self.screen)

	def terminate(self):
		pygame.quit()
		sys.exit()
