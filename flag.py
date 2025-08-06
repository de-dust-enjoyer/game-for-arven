import pygame
from os.path import join
from animation_player import AnimationPlayer

class Flag(pygame.sprite.Sprite):
	def __init__(self, checkpoints:dict, name:str, pos):
		super().__init__()
		self.id = name
		self.dead = False # all objects need this
		self.checkpoints = checkpoints
		image_dict = {
			"down": pygame.image.load(join("assets", "objects", "flag_down.png")).convert_alpha(),
			"up"  : pygame.image.load(join("assets", "objects", "flag_up.png")).convert_alpha()
		}
		self.animation_player = AnimationPlayer(image_dict, 1, (8,16))


		self.animation_player.play("down")
		self.image = self.animation_player.update()

		self.rect = self.image.get_rect(topleft= pos)

	def update(self):
		if not self.id in self.checkpoints and not self.animation_player.animation == "up":
			self.animation_player.play("up")
			self.image = self.animation_player.update()


	def scale_by(self, scale:float):
		scaled_img = pygame.transform.scale_by(self.image, scale)
		return scaled_img
