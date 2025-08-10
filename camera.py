import pygame
from timer import Timer
from chunking import get_nearby_tiles
from player import Player

class CameraGroup(pygame.sprite.Group):
	def __init__(self, groups:list, chunk_dict:dict, chunk_size:int):
		super().__init__()
		self.render_dist = 3 # chunks
		self.fullscreen = False
		self.display_surf = pygame.display.get_surface()
		self.camera_surf = pygame.surface.Surface(self.display_surf.get_size(), pygame.SRCALPHA).convert_alpha()
		self.camera_rect = self.camera_surf.get_rect()
		self.groups = groups
		self.zoom:int = 10
		
		self.zoom_center = pygame.math.Vector2(self.display_surf.get_size()) / 2
		self.offset:pygame.math.Vector2 = pygame.math.Vector2(100,250)

		self.velocity = pygame.Vector2(0, 0)
		self.camera_smoothing = 20
		self.dead_zone = 0.1

		self.target = None
		self.temp_target = None

		self.temp_target_timer = Timer(5)

		self.chunk_dict = chunk_dict
		self.chunk_size = chunk_size
	

	def custom_draw(self):
		zoom = self.zoom
		self.box_movement()
		# aduasts the rect to it fits the zoomed screen
		visible_w = self.display_surf.get_width() / zoom
		visible_h = self.display_surf.get_height() / zoom

		self.camera_rect.topleft = (self.offset.x , self.offset.y)
		self.camera_rect.size = (visible_w, visible_h)

		if self.offset.y < 300:
			self.display_surf.fill("lightblue")
		else:
			self.display_surf.fill((27,28,34))
		center_pos = self.camera_rect.center
		nearby_tiles = get_nearby_tiles(center_pos, self.chunk_dict, self.chunk_size, self.render_dist)

		for sprite in nearby_tiles:
			sprite_pos = pygame.Vector2(sprite.rect.topleft)
			adjusted_pos = ((sprite_pos - self.offset) * zoom)
			self.display_surf.blit(sprite.scale_by(zoom), adjusted_pos)


		for group in self.groups:
			for sprite in group:
				if not sprite.dead:
					sprite_pos = pygame.Vector2(sprite.rect.topleft)
					adjusted_pos = ((sprite_pos - self.offset) * zoom)
					self.display_surf.blit(sprite.scale_by(zoom), adjusted_pos)




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
