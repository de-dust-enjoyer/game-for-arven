import pygame
from spritesheet import Spritesheet

class AnimationPlayer:
	def __init__(self, animations:dict = {}, animation_speed:int = 10, tilesize:tuple = (8,8), starting_animation:str="idle", repeat:bool=True, parent=None):
		self.animations:dict = {}
		for animation in animations:
			self.animations[animation] = Spritesheet(animations[animation], tilesize[0], tilesize[1]).get_imgs_as_list()
		self.repeat = repeat
		self.playing = False
		self.animation:str = starting_animation
		self.index:int = 0
		self.delta_time_target:float = 1 / animation_speed * 1000
		self.old_time:float = pygame.time.get_ticks()
		self.current_time:float = pygame.time.get_ticks()
		self.parent = parent
		self.locked = False
		self.perm_animation = "finnish"


	def update(self): # this runs framerate independent!!! (WOOOOW i love it!!!)
		if not self.locked:
			if self.playing:
				self.current_time = pygame.time.get_ticks()
				# if enough time has passed the next frame is called
				if self.current_time - self.old_time >= self.delta_time_target:
					self.index += 1 # increments the frame index
					self.old_time = pygame.time.get_ticks()
			
			if self.index >= len(self.animations[self.animation]): # if frame index higher than possible Frames then set to 0
				if self.repeat:
					self.index = 0
				elif not self.repeat and self.animation == "run":
					self.set_animation_perm("finnish")
					self.parent.dialog = [". . . . . . . ", "Es ist ein . . . . ", "Gutschein", ". . . . .", "Ein Kino Gutschein!"]
				else:
					self.playing = False
					self.index = len(self.animations[self.animation]) - 1

			return self.animations[self.animation][self.index] # returns the image for the animation
		else:
			return self.animations[self.perm_animation][0]



	def play(self, animation:str = None):
		if not self.playing:
			self.old_time = pygame.time.get_ticks()
			self.index = 0
			self.playing = True
		if animation and self.animation != animation:
			self.animation = animation


	def stop(self):
		self.playing = False
		self.index = 0


	def set_animation_perm(self, animation):
		self.old_time = pygame.time.get_ticks()
		self.index = 0
		self.playing = True
		self.animation = animation
		self.locked = True