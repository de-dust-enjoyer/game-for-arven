import pygame


class Trigger(pygame.sprite.Sprite):
	def __init__(self, rect:pygame.Rect, target, method=None, attribute:bool=None, set_true_if_inside:bool=False):
		super().__init__()
		self.rect = rect
		self.target = target
		self.method = method
		self.attribute = attribute
		self.set_true_if_inside = set_true_if_inside

	def update(self):
		if self.rect.colliderect(self.target.collision_rect):
			if self.method:
				self.method()
			if self.attribute:
				self.attribute = True if self.set_true_if_inside else False

		else:
			self.attribute = False if self.set_true_if_inside else True
