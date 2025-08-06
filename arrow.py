import pygame
from os.path import join
from timer import Timer

class Arrow(pygame.sprite.Sprite):
	def __init__(self, orientation, pos_center):
		super().__init__()

		self.image = pygame.load.image(join("assets", "traps", "arrows.png")).convert_alpha()
		if orientation == "horizontal":
			self.image == pygame.transform.rotate(self.image, -90)

		self.speed = 2
		self.direction = pygame.Vector2(0,1) if orientation == "vertical" else pygame.Vector2(1,0)
		self.position = pygame.Vector2(pos_center)

		self.rect = self.image.get_frect()

		self.kill_timer = Timer(duration=5)
		self.kill_timer.start()

	def update(self):
		self.postition += self.direction * self.speed
		self.rect.center = self.position
		if self.kill_timer.update():
			self.kill()
