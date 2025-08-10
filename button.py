import pygame
from os.path import join

class Button(pygame.sprite.Sprite):
	def __init__(self, text:str, pos:tuple, centered:bool = False, method = None, arg = None):
		super().__init__()
		scale = 28
		image_idle = pygame.transform.scale_by(pygame.image.load(join("assets", "ui", "button_idle.png")).convert_alpha(), scale)
		image_pressed = pygame.transform.scale_by(pygame.image.load(join("assets", "ui", "button_pressed.png")).convert_alpha(), scale)
		image_hover = pygame.transform.scale_by(pygame.image.load(join("assets", "ui", "button_hover.png")).convert_alpha(), scale)
		self.images = {"idle": image_idle, "pressed": image_pressed, "hover": image_hover}
		self.image = self.images["idle"]
		self.rect = self.image.get_rect()
		self.clicked = False
		self.method = method
		self.font = pygame.font.Font(join("assets", "font", "pixel_font.otf"), scale * 4)
		self.text = self.font.render(text, False, "white")


		self.arg = arg


		if centered:
			self.rect.center = pos
		else:
			self.rect.topleft = pos

		for key in self.images:
			image = self.images[key]
			image_center = image.get_rect().center
			text_offset_x = self.text.get_width() / 2
			text_offset_y = self.text.get_height() / 2
			image.blit(self.text, (image_center[0] - text_offset_x, image_center[1] - text_offset_y))


	def update(self, mouse_button_up_event):
		self.image = self.images["idle"]
		mouse_pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		if self.rect.collidepoint(mouse_pos):
			self.image = self.images["hover"]
			if click:
				self.clicked = True # clicked on the button
				self.image = self.images["pressed"]

				# needs rewriting doesnt work at all
		else:
			self.clicked = False

		if mouse_button_up_event and self.clicked:
			if self.method:
				if self.arg:
					self.method(self.arg)
				else:
					self.method()

			return True
