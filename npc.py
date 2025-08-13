import pygame
from animation_player import AnimationPlayer
from player import Player
from os.path import join
from dialog_box import DialogBox
from timer import Timer


class NPC(Player):
	def __init__(self, starting_pos, chunk_dict:dict, chunk_size:int, id:str, player:Player, camera_group:pygame.sprite.Group, ui_group: pygame.sprite.Group):
		super().__init__(starting_pos, chunk_dict, chunk_size, ui_group, {})
		self.id = id

		animations:dict = {
			"idle" : pygame.image.load(join("assets", "npc", self.id, "idle.png")).convert_alpha(),
			"run" : pygame.image.load(join("assets", "npc", self.id, "run.png")).convert_alpha(),
			"finnish" : pygame.image.load(join("assets", "npc", self.id, "finnish.png")).convert_alpha()
		}

		tilesizes = {
			"simon": (8,8),
			"luis": (8,12),
			"present": (9, 12)
		}
		starting_animation = "idle"
		
		self.animation_player = AnimationPlayer(animations, 5, tilesizes[self.id], starting_animation, repeat=not self.id == "present", parent=self) # sets repeat to false if present
		dialog = {
			"simon": 
			["Oh", "Hi", "Was machst du denn hier?", "Arwen hör zu ich hab Mist gebaut", "Du hattest ja Geburtstag", "und ich habe dir ein schönes Geschenk besorgt . . . . .",
			"Dann habe ich hier im Draussen einen Einheimischen getroffen", "Er meinte er würde mich im 1v1 besiegen", "Das konnte ich nicht auf mir sitzen lassen!",
			"Ausserdem sah er aus als hätte er noch nie Counter Strike gespielt", "Er meinte aber er spielt nur mit Einsatz . . . .", "Und ich hatte nichts dabei", "Ausser deinem Geschenk . . . .",
			". . . .", "Er hat mir einen ferrari peak gedrückt", "ich hatte keine Zeit zu reagieren und habe verloren", "Aber es besteht noch Hoffnung!", "Sie bewahren dein Geschenk in der Schatzkammer auf . . .",
			"Der Weg ist nicht weit aber . . . ", "Zwischen dir und der Kammer liegen unzählige tödliche Fallen!", "Geh nun. Hol dir dein Geschenk wieder!", "Ich glaube an dich!"],
			
			"luis": 
			["Oha!", "Ich hab nicht erwartet dich hier zu treffen.", "Wir haben ein kleines Problem!!!", "Aber erstmal,", 
			"ALLES GUTE ZUM GEBURTSTAG", "und jetzt die schlechte Nachricht!!", "Simon wurde von den Einheimischen in den Tempel gelockt!",
			"Sie meinten zu ihm er habe keine Chance gegen sie in Counter Strike", "Er ist ihnen schneller gefolgt als ich gucken konnte",
			"ich habe ihn auf dem Weg verloren!!!", "gehe in den Tempel und finde ihn!!!"],
			"present": 
			["Da ist es ja endlich"]
		}
		self.dialog = dialog[self.id]
		self.animation = "idle"
		self.animation_player.play(self.animation)
		self.ui_group = ui_group

		self.player = player
		self.camera_group = camera_group

		
		self.image = self.animation_player.update()
		self.rect = self.image.get_frect()
		self.collision_rect = self.rect.copy()
		self.collision_rect.size = (self.rect.width - 4, self.rect.height - 2)
		self.collision_rect.midbottom = self.rect.midbottom
		self.old_rect = self.collision_rect.copy() # for collision direction

		self.interaction_box = pygame.Rect((self.rect.topleft), (50, 50))
		self.interaction_box.center = self.collision_rect.center

		self.target:pygame.Vector2 = None
		self.look_target = None
		self.speed = 0.5
		self.allowed_to_move = True

		self.play_credits = False
		self.done = False




	def update(self):

		self.image = self.animation_player.update()
		self.move()
		
		self.handle_interaction()

	def move(self):

		# general movement

		self.collision_rect.topleft = self.position
		self.rect.midbottom = self.collision_rect.midbottom


		# animation
		if not self.look_target:
			self.flip_h = True if self.velocity.x <= 0 else False
		else:
			if self.collision_rect.centerx < self.look_target.collision_rect.centerx:
				self.flip_h = False
			else:
				self.flip_h = True


	def look_at(self, target):
		self.look_target = target

	def stop_look_at(self):
		self.look_target = None

	def play_dialog(self):
		if len(self.ui_group) == 0:
			if self.id != "present":
				dialog_box = DialogBox(self.dialog, self.id, self)
			else:
				dialog_box = DialogBox(self.dialog, "Arwen", self)
			self.ui_group.add(dialog_box)
			dialog_box.start()


	def handle_interaction(self):
		self.interaction_box.center = self.collision_rect.center
		if self.player.collision_rect.colliderect(self.interaction_box) and len(self.dialog):
			self.player.stop()
			self.stop()
			self.camera_group.set_target(self)

			self.play_dialog()
			if not self.id == "present":
				self.look_at(self.player)
			

		elif len(self.dialog) == 0:
			if not self.end_game:
				self.player.start()
			
			self.camera_group.remove_temp_target()



	def last_scene(self):
		self.end_game = True
		self.position = pygame.Vector2(1824, 286)
		
		self.dialog = ["Na, dann wollen wir mal!"]
		for group in self.groups():
			for sprite in group:
				if sprite.id == "luis":
					sprite.end_game = True
					sprite.position = pygame.Vector2(1808, 286)
					sprite.look_at(self)
					sprite.dialog = ["Joooo! Du hast es Geschafft"]

				elif sprite.id == "simon":
					sprite.end_game = True
					sprite.position = pygame.Vector2(1816, 290)
					sprite.look_at(self)
					sprite.dialog = ["Zum Glück bist du heil zurückgekommen", "Ich dachte schon dein Geschenk wäre für immer verloren", 
					"...", "es tut mir leid :( ...", "es war dumm es zu verwetten", "Aber ich war mir so sicher dass ich gewinne", "Aber Hey", 
					"Wenigstens hast du es jetzt wieder", "komm schon öffne es du hast es dir jetzt aber wirklich verdient!"]
				elif sprite.id == "player":
					sprite.end_game = True
					sprite.collision_rect.center = (1835, 290)
					sprite.position = pygame.Vector2(sprite.collision_rect.center)
					sprite.downforce = 0
					sprite.velocity.y = 0








