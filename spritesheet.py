import pygame

class Spritesheet():
	def __init__(self, img, tilesize_x:int = 8, tilesize_y:int = 8):
		self.img = img
		self.tilesize = (tilesize_x, tilesize_y)
		

	def get_img(self, index):
		img = pygame.Surface(self.tilesize, pygame.SRCALPHA).convert_alpha()
		img.blit(self.img, (0,0), (self.tilesize[0] * index, 0, self.tilesize[0], self.tilesize[1]))
		
		return img

	def get_imgs_as_list(self):
		img_list:list = []
		for index in range(int(self.img.get_width() / self.tilesize[0])):
			img_list.append(self.get_img(index))

		return img_list
