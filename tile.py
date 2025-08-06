import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos:tuple,image:pygame.surface.Surface, id):
		super().__init__()
		self.image = image
		self.rect = self.image.get_frect(topleft = pos)
		self.cache = {}
		self.id = id
		self.collision_rect = self.rect.copy()
		if self.id == "kill_tile":
			self.collision_rect.size = (self.rect.width - 2, self.rect.height // 2)
			self.collision_rect.midbottom = self.rect.midbottom

	def scale_by(self, scale:float):
		if not scale in self.cache:
			self.cache[scale] = pygame.transform.scale_by(self.image, scale)
		return self.cache[scale]