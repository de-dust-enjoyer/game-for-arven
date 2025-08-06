import pygame, random
from os.path import join
from animation_player import AnimationPlayer
from timer import Timer
from dialog_box import DialogBox



class Player(pygame.sprite.Sprite):
	def __init__(self, starting_pos:pygame.math.Vector2, chunk_dict:dict, chunk_size:int, ui_group, checkpoints:dict):
		super().__init__()
		self.checkpoints = checkpoints
		self.spawn_pos = starting_pos
		self.ui_group = ui_group
		self.id = "player"
		animations:dict = {
			"idle" : pygame.image.load(join("assets", "player", "idle.png")).convert_alpha(),
			"run" : pygame.image.load(join("assets", "player", "run.png")).convert_alpha(),
			"jump" : pygame.image.load(join("assets", "player", "jump.png")).convert_alpha(),
			"look_up" : pygame.image.load(join("assets", "player", "look_up.png")).convert_alpha(),
			"look_down" : pygame.image.load(join("assets", "player", "look_down.png")).convert_alpha()
		}
		self.animation_player:AnimationPlayer = AnimationPlayer(animations, 10)
		self.image = self.animation_player.update()
		self.rect = self.image.get_frect(center = self.spawn_pos)
		self.collision_rect = self.rect.copy()
		self.collision_rect.size = (self.rect.width - 4, self.rect.height - 2)
		self.collision_rect.midbottom = self.rect.midbottom
		self.old_rect = self.collision_rect.copy() # for collision direction
		self.position = pygame.math.Vector2(self.rect.topleft)

		self.chunk_dict = chunk_dict
		self.chunk_size = chunk_size

		#movement vars:
		self.speed:float = 1.5
		self.max_velocity_y = 8
		self.accelaration:float = 0.15
		self.velocity:pygame.Vector2 = pygame.Vector2(0,0)
		self.gravity:float = 0.008
		self.jump_vel:float = 1.8
		self.jump = False
		self.has_jump = True
		self.is_on_floor = False
		self.is_on_left_wall = False
		self.is_on_right_wall = False
		self.flip_h = False
		self.allowed_to_move = True
		wall_jump_time = 0.3
		self.wall_jump_strength:float = 0.6
		self.wall_jump_left_timer = Timer(wall_jump_time, return_true_when_stopped = True)
		self.wall_jump_right_timer = Timer(wall_jump_time, return_true_when_stopped = True)
		self.jump_delay_timer = Timer(0.15, return_true_when_stopped = True)
		self.death_timer = Timer(3, return_true_when_stopped = False)

		self.dead = False

		self.downforce:float = 0

		self.animation_player.play("run")

	def update(self):
		if self.death_timer.update():
			self.collision_rect.center = self.spawn_pos
			self.position = pygame.Vector2(self.collision_rect.topleft)
			self.dead = False
		self.image = self.animation_player.update()
		self.move()
		self.handle_checkpoints()


	def move(self):
		if not self.dead:
			# update the timers
			has_wall_jumped_left = self.wall_jump_left_timer.update()
			has_wall_jumped_right = self.wall_jump_right_timer.update()
			can_climb = self.jump_delay_timer.update()
			if self.allowed_to_move:

				self.old_rect = self.collision_rect.copy()

				keys = pygame.key.get_pressed()
				# if no action is pressed > play "idle"
				self.animation_player.play("idle")
				# animation for looking up and down
				if keys[pygame.K_w]:
					self.animation_player.play("look_up")
				elif keys[pygame.K_s]:
					self.animation_player.play("look_down")


				# horizontal movement:
				nothing_pressed = True
				if keys[pygame.K_a] and has_wall_jumped_left:
					self.velocity.x = -1
					self.flip_h = True
					nothing_pressed = False
					if not self.is_on_left_wall:
						self.animation_player.play("run")
					else:
						self.animation_player.play("idle")


				elif keys[pygame.K_d] and has_wall_jumped_right:
					self.velocity.x = 1
					self.flip_h = False
					nothing_pressed = False
					if not self.is_on_right_wall:
						self.animation_player.play("run")
					else:
						self.animation_player.play("idle")
				elif has_wall_jumped_left and has_wall_jumped_right or self.is_on_floor:
					self.velocity.x = 0

				self.position.x += self.velocity.x * self.speed
				self.collision_rect.left = self.position.x
				self.handle_collisions("horizontal")


				

			# gravity:
			if not self.is_on_left_wall and not self.is_on_right_wall:
				self.downforce += self.gravity
			elif can_climb:
				self.velocity.y = self.velocity.y * 0.7
				self.downforce += self.gravity * 0.1
				self.downforce = self.downforce * 0.9
			else:
				self.downforce += self.gravity
			self.velocity.y += self.downforce
			self.velocity.y = min(self.max_velocity_y, self.velocity.y)
			self.position.y += self.velocity.y
			self.collision_rect.top = self.position.y
			self.handle_collisions("vertical")

			if self.allowed_to_move:
			# vertical movement
				if self.jump:
					self.jump = False
					self.animation_player.play("jump")
					if self.is_on_floor:
						self.velocity.y = -self.jump_vel
						self.downforce = 0
						self.jump_delay_timer.start()
						
					elif self.is_on_left_wall and can_climb:

						self.velocity = pygame.Vector2(self.wall_jump_strength, -self.jump_vel * 0.7)
						self.downforce = 0
						self.wall_jump_left_timer.start()
						
					elif self.is_on_right_wall and can_climb:
						self.velocity = pygame.Vector2(-self.wall_jump_strength, -self.jump_vel * 0.7)
						self.downforce = 0
						self.wall_jump_right_timer.start()
						

					

		
	def handle_collisions(self, direction:str):
		# update the collision rect posidion
		self.is_on_floor = False if direction == "vertical" else True # reset the is_on_floor var
		# reset the wall vars:
		if direction == "horizontal":
			self.is_on_left_wall = False
			self.is_on_right_wall = False

		nearby_tiles = self.get_nearby_tiles(self.collision_rect.center, self.chunk_dict, self.chunk_size)
		for sprite in nearby_tiles:
			if self.collision_rect.colliderect(sprite.rect) and sprite.id == "collision_tile":
				if direction == "vertical":
					if self.collision_rect.bottom > sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
						# player is on floor
						self.collision_rect.bottom = sprite.rect.top
						self.is_on_floor = True
						self.velocity.y = 0
						self.downforce = 0
						self.has_jump = True

					elif self.collision_rect.top < sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
						# player is on ceiling
						self.collision_rect.top = sprite.rect.bottom
						self.velocity.y = 0

				elif direction == "horizontal":
					if self.collision_rect.left < sprite.rect.right and self.old_rect.left >= sprite.rect.right:
						# player has a wall to his left
						self.collision_rect.left = sprite.rect.right
						self.velocity.x = 0
						self.is_on_left_wall = True
					elif self.collision_rect.right > sprite.rect.left and self.old_rect.right <= sprite.rect.left:
						# player has a wall to his right
						self.collision_rect.right = sprite.rect.left
						self.velocity.x = 0
						self.is_on_right_wall = True
		# kill player if hit spikes
			elif self.collision_rect.colliderect(sprite.rect) and sprite.id == "kill_tile":
				
				self.die()


		# update the position variable
		self.rect.midbottom = self.collision_rect.midbottom
		self.position = pygame.math.Vector2(self.collision_rect.topleft)

	def get_nearby_tiles(self, player_pos, chunk_dict, chunk_size, radius_in_chunks=1):
		print(player_pos)
		chunk_x = int(player_pos[0] // chunk_size)
		chunk_y = int(player_pos[1] // chunk_size)
		nearby_tiles = []
		for dx in range(-radius_in_chunks, radius_in_chunks +1):
			for dy in range(-radius_in_chunks, radius_in_chunks +1):
				key = (chunk_x + dx, chunk_y + dy)
				nearby_tiles.extend(chunk_dict.get(key, []))
		return nearby_tiles




	def scale_by(self, scale:float):
		scaled_img = pygame.transform.scale_by(self.image, scale)
		return pygame.transform.flip(scaled_img, self.flip_h, False)


	def stop(self):
		self.allowed_to_move = False
		self.animation_player.play("idle")

	def start(self):
		self.allowed_to_move = True

	def handle_checkpoints(self):
		updated_spawn_pos = None
		for checkpoint in self.checkpoints:
			if self.collision_rect.colliderect(self.checkpoints[checkpoint]):
				self.spawn_pos = pygame.Vector2(self.checkpoints[checkpoint].center)
				updated_spawn_pos = checkpoint


		if updated_spawn_pos:
			self.checkpoints.pop(updated_spawn_pos)
			if updated_spawn_pos != "checkpoint_1":
				dialog = DialogBox([random.choice(["Cool! ein Checkpoint.", "Checkpoint!", "Endlich am Checkpoint!"])], "Arwen", self)
			else:
				dialog = DialogBox(["Wie lebe ich noch?", "das waren locker hundert Meter!"], "Arwen", self)
			self.ui_group.add(dialog)
			dialog.start()

				

	def die(self):
		self.dead = True
		self.movement_var_reset()
		self.death_timer.start()


	def movement_var_reset(self):
		self.velocity = pygame.Vector2(0,0)
		self.downforce = 0

		
