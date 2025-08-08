import pygame, sys
from timer import Timer
from tile import Tile

class TransitionScreen(pygame.sprite.Sprite):
	def __init__(self, method, arg, ui_group, transition_time=0.5):
		super().__init__(ui_group)
		self.screen_size = pygame.display.get_surface().get_size()
		self.id = "transition_screen"
		self.method = method
		self.arg = arg
		self.color = (0,0,0)
		self.speed = 20
		self.transition_time = transition_time
		self.alpha = 0
		self.increasing = True

		self.transition_timer = Timer(self.transition_time, repeat=False)

		self.rect = pygame.Rect(0, 0, self.screen_size[0], self.screen_size[1])
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)



	def update(self):
		if self.transition_timer.update():
			self.increasing = False

		if self.increasing:
			self.alpha += self.speed
		else:
			self.alpha -= self.speed

		self.alpha = max(0, min(self.alpha, 255))

		if self.alpha >= 255 and self.increasing:
			self.transition_timer.start()
			if self.method and self.arg:
				self.method(self.arg)
			elif self.method:
				self.method()
			


		elif self.alpha <= 0 and not self.increasing:
			self.kill()

		
		self.image.fill((self.color[0], self.color[1], self.color[2], self.alpha))

