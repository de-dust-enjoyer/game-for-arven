import pygame

class Hair(pygame.sprite.Sprite):
	def __init__(self, target, image:pygame.Surface):
		super().__init__()
		self.target = target

		self.dead = self.target.dead
		if self.target.id == "player":
			self.target_pos = pygame.Vector2(target.rect.centerx - 0.1, target.rect.centery)
		else:
			self.target_pos = pygame.Vector2(target.rect.center)
		self.pos = pygame.Vector2(target.rect.center)
		self.velocity = pygame.Vector2(0,0)
		self.image = image
		self.rect = self.image.get_frect(center=self.pos)
		self.id = "hair"

	def scale_by(self, scale:float):
		scaled_img = pygame.transform.scale_by(self.image, scale)
		return scaled_img

	def update(self):
		self.dead = self.target.dead
		if self.target.id == "player":
			offset = -2 if self.target.flip_h else 2
			self.target_pos = pygame.Vector2(self.target.rect.centerx - offset, self.target.rect.centery)
		else:
			self.target_pos = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery + 0.3)
		self.velocity = self.target_pos - self.pos
		self.pos += self.velocity * 0.9
		self.rect.center = self.pos