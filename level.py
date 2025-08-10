import pygame, sys, pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from os.path import join
from tile import Tile
from camera import CameraGroup
from hair import Hair
from npc import NPC
from flag import Flag
from trigger import Trigger
from transition_screen import TransitionScreen

class Level:
	def __init__(self, screen, game_state_manager):
		self.screen = screen
		self.game_state_manager = game_state_manager
		

		# game vars
		self.game_won:bool = False

		self.tilesize:tuple = (8,8)

		# chunking
		self.chunk_size = 32
		self.chunked_tiles = {} # {(chunk_x, chunk_y): [Tile, Tile, Tile ...]}

		# groups:
		self.objects = pygame.sprite.Group()
		self.all_tiles = pygame.sprite.Group()
		self.collision_tiles = pygame.sprite.Group()
		self.kill_tiles = pygame.sprite.Group()
		self.trigger_group = pygame.sprite.Group()
		self.camera_group = CameraGroup([self.objects], self.chunked_tiles, self.chunk_size)
		self.ui_group = pygame.sprite.Group()


		self.checkpoints = {}


		self.build_level()

	

	def build_level(self, level_path:str = join("assets", "levels", "level-01.tmx")):
		tmx_data = load_pygame(level_path)
		for layer in tmx_data.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer): # if layer is a tilelayer (not an object layer)
				for x, y, gid, in layer:
					tile_img = tmx_data.get_tile_image_by_gid(gid)
					if not tile_img:
						continue

					pos = (x * self.tilesize[0], y * self.tilesize[1])
					tile = Tile(pos, tile_img, layer.name, None)

					self.all_tiles.add(tile)
					if layer.name == "collision_tile":
						self.collision_tiles.add(tile)
					elif layer.name == "kill_tile":
						self.kill_tiles.add(tile)


					# chunking

					chunk_x = pos[0] // self.chunk_size
					chunk_y = pos[1] // self.chunk_size
					chunk_key = (chunk_x, chunk_y)
					self.chunked_tiles.setdefault(chunk_key, []).append(tile)


			elif isinstance(layer, pytmx.TiledObjectGroup):
				for obj in layer:
					if layer.name == "player":
						player = Player((obj.x, obj.y), self.chunked_tiles, self.chunk_size, self.ui_group, self.checkpoints)
						self.player = player
						self.camera_group.set_target(self.player, player=True)
						hair_big = Hair(player, pygame.image.load(join("assets", "player", "hair_big.png")).convert_alpha())
						hair_mid = Hair(hair_big, pygame.image.load(join("assets", "player", "hair_mid.png")).convert_alpha())
						hair_mid2 = Hair(hair_mid, pygame.image.load(join("assets", "player", "hair_mid.png")).convert_alpha())
						hair_small = Hair(hair_mid, pygame.image.load(join("assets", "player", "hair_small.png")).convert_alpha())
						hair_small2 = Hair(hair_small, pygame.image.load(join("assets", "player", "hair_small.png")).convert_alpha())
						self.objects.add(hair_big, hair_mid, hair_mid2, hair_small, hair_small2, player)


					elif layer.name == "npc":
						
						npc = NPC((obj.x, obj.y), self.chunked_tiles, self.chunk_size, obj.name, player, self.camera_group, self.ui_group)
						if obj.name == "luis":
							pass
							#self.camera_group.set_target(npc, player=True)
							#npc.goto(pygame.Vector2(player.collision_rect.center))
						elif obj.name == "present":
							npc.look_at(npc)
						self.objects.add(npc)
							

					elif layer.name == "checkpoints":
						if obj.type == "checkpoint":
							self.checkpoints[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
						elif obj.type == "flag":
							flag = Flag(self.checkpoints, obj.name, (obj.x, obj.y))
							self.objects.add(flag)

					elif layer.name == "triggers":
						trigger = Trigger(obj.name, pygame.Rect(obj.x, obj.y, obj.width, obj.height),self.player, attribute="in_no_move_zone", set_true_if_inside=True)	
						self.trigger_group.add(trigger)

	def run(self):
		# input loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.game_state_manager.set_state("pause")
				if event.key == pygame.K_SPACE:
					self.player.jump = True
					for obj in self.ui_group:
						if obj.id == "dialog_box":
							obj.next_line()


		# game logic:
		self.objects.update()
		self.trigger_group.update()
		self.ui_group.update()

		for obj in self.objects:
			if obj.id == "present":
				if obj.game_won_timer.update():
					transition_screen = TransitionScreen(self.game_state_manager.set_state, "end", self.ui_group, 2)

		# rendering:
		self.screen.fill("black")
		self.camera_group.custom_draw()
		self.ui_group.draw(self.screen)


		
