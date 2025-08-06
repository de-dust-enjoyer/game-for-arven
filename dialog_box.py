import pygame
from os.path import join
from timer import Timer

class DialogBox(pygame.sprite.Sprite):
	def __init__(self, dialog:list, name:str, control_parent):
		super().__init__()
		self.id = "dialog_box"
		self.name = name
		self.parent = control_parent
		self.dialog = dialog
		self.dialog_index = 0
		self.letter_index = 0
		self.typing_complete = False
		self.waiting_for_input = False
		
		scale = 8
		self.image = pygame.transform.scale_by(
			pygame.image.load(join("assets", "ui", "dialog_box.png")).convert_alpha(), scale)
		self.original_image = self.image.copy()
		self.rect = self.image.get_rect()
		self.rect.midtop = (pygame.display.get_surface().get_width() // 2, 80)
		self.text_lines = []
		
		self.font = pygame.font.Font(join("assets", "font", "pixel_font.otf"), 14)
		self.name_font = pygame.font.Font(join("assets", "font", "pixel_font.otf"), 14)
		self.name_text = self.name_font.render(self.name, False, (20,130,20))
		self.name_rect = self.name_text.get_rect(center = (self.rect.width // 2, 20))
		self.letter_timer = Timer(duration=0.02, repeat=True)
		# load and scale ui img

	def start(self):
		if self.dialog:
			self.letter_index = 0
			self.typing_complete = False
			self.waiting_for_input = False
			self.text_lines = []
			self.letter_timer.start()

	def update(self):
		if self.typing_complete:
			return
		if self.letter_timer.update():
			current_text = self.dialog[self.dialog_index]
			if self.letter_index < len(current_text):
				self.text_lines.append(current_text[self.letter_index])
				self.render_text()
				self.letter_index += 1
			else:
				self.typing_complete = True

	def render_text(self):
		self.image = self.original_image.copy()
		full_text = "".join(self.text_lines)
		max_width = self.rect.width - 30 # padding

		words = full_text.split(" ") # returns list with string split at " "
		lines = []
		current_line = ""

		for word in words:
			test_line = current_line + word + " "
			test_surface = self.font.render(test_line, False, "white")
			if test_surface.get_width() <= max_width:
				current_line = test_line
			else:
				lines.append(current_line)
				current_line = word + " "
		lines.append(current_line)

		# rendering
		y_offset = 30
		self.image.blit(self.name_text, self.name_rect)
		for line in lines:
			text_surface = self.font.render(line, False, "white")
			self.image.blit(text_surface, (15, y_offset))
			y_offset += self.font.get_height()



	def next_line(self):
		if not self.typing_complete:
			return

		self.dialog_index += 1
		if self.dialog_index >= len(self.dialog):
			self.kill() #suii
			self.parent.dialog = []
			

		else:
			self.start()

	def skip(self):
		self.text_lines = list(self.dialog[self.dialog_index])
		self.typing_complete = True
		self.render_text()