import pygame
from timer import Timer
from os.path import join

class ArrowShooter(pygame.sprite.Sprite):
	def __init__(self, pos, id):
		super().__init__()

		self.id = id
		self.position = pos
		if self.id == "arrow_shooter_vertical":
			self.image = pygame.image.load(join("assets", "traps", "arrow_shooter_vertical.png")).convert_alpha()

		elif self.id == "arrow_shooter_horizontal":
			self.image = pygame.image.load(join("assets", "traps", "arrow_shooter_horizontal.png")).convert_alpha()
		self.firerate = 2
		self.shoot_timer = Timer(duration=self.firerate, repeat=True)

		self.shoot_timer.start()

	def update()