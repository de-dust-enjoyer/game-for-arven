import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos:tuple,image:pygame.surface.Surface, id, gid):
		super().__init__()
		self.image = image

		self.rect = self.image.get_frect(topleft = pos)
		self.cache = {}
		self.id = id
		self.collision_rect = self.rect.copy()
		if gid == 78: # spike up
			self.collision_rect.size = (self.rect.width - 2, self.rect.height // 2)
			self.collision_rect.midbottom = self.rect.midbottom
		elif gid == 79: # spike left
			self.collision_rect.size = (self.rect.width // 2, self.rect.height - 2)
			self.collision_rect.midright = self.rect.midright
		elif gid == 80: # spike right
			self.collision_rect.size = (self.rect.width // 2, self.rect.height - 2)
			self.collision_rect.midleft = self.rect.midleft
		elif gid == 81: # spike down
			self.collision_rect.size = (self.rect.width - 2, self.rect.height // 2)
			self.collision_rect.midtop = self.rect.midtop


	def scale_by(self, scale:float):
		if not scale in self.cache:
			self.cache[scale] = pygame.transform.scale_by(self.image, scale)
		return self.cache[scale]