import pygame
from timer import Timer
from chunking import get_nearby_tiles

class CameraGroup(pygame.sprite.Group):
	def __init__(self, groups:list):
		super().__init__()
		self.display_surf = pygame.display.get_surface()
		self.camera_surf = pygame.surface.Surface(self.display_surf.get_size(), pygame.SRCALPHA).convert_alpha()
		self.camera_rect = self.camera_surf.get_rect()
		self.groups = groups
		self.zoom:int = 6
		self.zoom_center = pygame.math.Vector2(self.display_surf.get_size()) / 2
		self.offset:pygame.math.Vector2 = pygame.math.Vector2(0,200)

		self.velocity = pygame.Vector2(0, 0)
		self.camera_smoothing = 20
		self.dead_zone = 0.1

		self.target = None
		self.temp_target = None

		self.temp_target_timer = Timer(5)


		#optimizing
		self.sprites_drawn = 0
	

	def custom_draw(self):
		self.box_movement()
		# aduasts the rect to it fits the zoomed screen
		visible_w = self.camera_surf.get_width() / self.zoom
		visible_h = self.camera_surf.get_height() / self.zoom

		self.camera_rect.topleft = (self.offset.x , self.offset.y)
		self.camera_rect.size = (visible_w, visible_h)

		self.sprites_drawn = 0
		self.camera_surf.fill("lightblue")

		for group in self.groups:
			for sprite in group:
				if sprite.rect.colliderect(self.camera_rect) and sprite.id != "player" and sprite.id != "hair":
					sprite_pos = pygame.Vector2(sprite.rect.topleft)
					adjusted_pos = ((sprite_pos - self.offset) * self.zoom)

					self.camera_surf.blit(sprite.scale_by(self.zoom), adjusted_pos)
					self.sprites_drawn += 1
				elif sprite.id == "player" or sprite.id == "hair":
					if not sprite.dead:
						sprite_pos = pygame.Vector2(sprite.rect.topleft)
						adjusted_pos = ((sprite_pos - self.offset) * self.zoom)

						self.camera_surf.blit(sprite.scale_by(self.zoom), adjusted_pos)
						self.sprites_drawn += 1

		self.display_surf.blit(self.camera_surf, (0, 0))


	def box_movement(self):
		if self.temp_target_timer.update():
			self.temp_target = None
		self.velocity = pygame.Vector2(0, 0)
		if self.temp_target:
			self.velocity = (pygame.Vector2(self.temp_target.collision_rect.center) - pygame.Vector2(self.camera_rect.center)) / self.camera_smoothing
			if abs(self.velocity.length()) < self.dead_zone:
				self.velocity = pygame.Vector2(0,0)

		elif self.target:
			self.velocity = (pygame.Vector2(self.target.collision_rect.center) - pygame.Vector2(self.camera_rect.center)) / self.camera_smoothing
			if abs(self.velocity.length()) < self.dead_zone:
				self.velocity = pygame.Vector2(0,0)

		self.offset += self.velocity

	def set_target(self, target, player=False, duration=None):
		if player:
			self.target = target
		else:
			self.temp_target = target
			if duration:
				self.temp_target_timer.set_duration(duration)
				self.temp_target_timer.start()

	def remove_temp_target(self):
		self.temp_target = None
