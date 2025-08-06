import pygame
from animation_player import AnimationPlayer
from player import Player
from os.path import join
from dialog_box import DialogBox

class NPC(Player):
	def __init__(self, starting_pos, chunk_dict:dict, chunk_size:int, id:str, player:Player, camera_group:pygame.sprite.Group, ui_group: pygame.sprite.Group):
		super().__init__(starting_pos, chunk_dict, chunk_size, ui_group, {})
		self.id = id
		animations:dict = {
			"idle" : pygame.image.load(join("assets", "npc", self.id, "idle.png")).convert_alpha(),
			"run" : pygame.image.load(join("assets", "npc", self.id, "run.png")).convert_alpha()
		}
		tilesizes = {
			"simon": (8,8),
			"luis": (8,12)
		}
		self.animation_player = AnimationPlayer(animations, 5, tilesizes[self.id])
		dialog = {
			"simon": ["lol"],
			"luis": ["Oha!", "Ich hab nicht erwartet dich hier zu treffen.", "Wir haben ein kleines Problem!!!", "Aber erstmal,", 
			"ALLES GUTE ZUM GEBURTSTAG", "und jetzt die schlechte Nachricht!!", "Simon wurde von den Einheimischen in den Tempel gelockt!",
			"Sie meinten zu ihm er habe keine Chance gegen sie in Counter Strike", "Er ist ihnen schneller gefolgt als ich gucken konnte",
			"ich habe ihn auf dem Weg verloren!!!", "gehe in den Tempel und finde ihn!!!"]
		}
		self.dialog = dialog[self.id]

		self.ui_group = ui_group

		self.player = player
		self.camera_group = camera_group

		self.animation = "idle"
		self.image = self.animation_player.update()
		self.rect = self.image.get_frect()
		self.collision_rect = self.rect.copy()
		self.collision_rect.size = (self.rect.width - 4, self.rect.height - 2)
		self.collision_rect.midbottom = self.rect.midbottom
		self.old_rect = self.collision_rect.copy() # for collision direction

		self.interaction_box = pygame.Rect((self.rect.topleft), (60, 60))
		self.interaction_box.center = self.collision_rect.center

		self.target:pygame.Vector2 = pygame.Vector2(self.player.collision_rect.center)
		self.speed = 0.5
		self.allowed_to_move = True


	def update(self):
		self.image = self.animation_player.update()
		self.move()
		self.handle_interaction()

	def move(self):
		# set the target:

		# general movement
		if self.target and self.allowed_to_move:
			self.velocity.x = self.target.x - pygame.Vector2(self.collision_rect.center).x
			if self.velocity.length() > 1:
				self.velocity = self.velocity.normalize()
			self.position += self.velocity * self.speed
			self.collision_rect.topleft = self.position
		else:
			self.velocity.x = 0
			self.collision_rect.topleft = self.position

		self.handle_collisions("horizontal")


		# gravity
		self.downforce += self.gravity
		self.velocity.y += self.downforce
		self.velocity.y = min(self.max_velocity_y, self.velocity.y)
		self.position.y += self.velocity.y
		self.collision_rect.top = self.position.y
		self.handle_collisions("vertical")

		# animation
		self.flip_h = True if self.velocity.x <= 0 else False
		if self.velocity.x:
			self.animation_player.play("run")
		else:
			self.animation_player.play("idle") 

	def goto(self, pos:pygame.Vector2):
		self.target = pos

	def play_dialog(self):
		if len(self.ui_group) == 0:
			dialog_box = DialogBox(self.dialog, self.id, self)
			self.ui_group.add(dialog_box)
			dialog_box.start()


	def handle_interaction(self):
		self.interaction_box.center = self.collision_rect.center
		if self.player.collision_rect.colliderect(self.interaction_box) and len(self.dialog):
			self.player.stop()
			self.stop()
			self.camera_group.set_target(self)
			self.play_dialog()
		elif len(self.dialog) == 0:

			self.player.start()
			
			self.camera_group.remove_temp_target()





