import pygame, sys, pytmx
from pytmx.util_pygame import load_pygame
from player import Player
from os.path import join
from tile import Tile
from camera import CameraGroup
from hair import Hair
from npc import NPC

class Level:
	def __init__(self, screen, game_state_manager):
		self.screen = screen
		self.game_state_manager = game_state_manager
		

		# game vars
		self.game_won:bool = False

		self.tilesize:tuple = (8,8)


		# groups:
		self.objects = pygame.sprite.Group()
		self.all_tiles = pygame.sprite.Group()
		self.collision_tiles = pygame.sprite.Group()
		self.kill_tiles = pygame.sprite.Group()
		self.camera_group = CameraGroup([self.all_tiles, self.objects])
		self.ui_group = pygame.sprite.Group()
		

		self.checkpoints = {}


		self.build_level()

	

	def build_level(self, level_path:str = join("assets", "levels", "level-01.tmx")):
		tmx_data = load_pygame(level_path)
		for layer in tmx_data.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer): # if layer is a tilelayer (not an object layer)
				for x, y, gid in layer:
					if layer.name == "collision_floor":
						tile_img = tmx_data.get_tile_image_by_gid(gid)
						if tile_img:
							tile = Tile((x * self.tilesize[0],y * self.tilesize[1]), tile_img, "collision_tile")
							self.collision_tiles.add(tile)
							self.all_tiles.add(tile)
					elif layer.name == "kill_tiles":
						tile_img = tmx_data.get_tile_image_by_gid(gid)
						if tile_img:
							tile = Tile((x * self.tilesize[0],y * self.tilesize[1]), tile_img, "kill_tile")
							self.kill_tiles.add(tile)
							self.all_tiles.add(tile)
					elif layer.name == "non_collision_floor":
						tile_img = tmx_data.get_tile_image_by_gid(gid)
						if tile_img:
							tile = Tile((x * self.tilesize[0],y * self.tilesize[1]), tile_img, "non_collision_tile")
							self.all_tiles.add(tile)
			elif isinstance(layer, pytmx.TiledObjectGroup):
				for obj in layer:
					if layer.name == "player":
						player = Player((obj.x, obj.y), self.collision_tiles, self.ui_group, self.kill_tiles, self.checkpoints)
						self.player = player
						self.camera_group.set_target(self.player, player=True)
						hair_big = Hair(player, pygame.image.load(join("assets", "player", "hair_big.png")).convert_alpha())
						hair_mid = Hair(hair_big, pygame.image.load(join("assets", "player", "hair_mid.png")).convert_alpha())
						hair_mid2 = Hair(hair_mid, pygame.image.load(join("assets", "player", "hair_mid.png")).convert_alpha())
						hair_small = Hair(hair_mid, pygame.image.load(join("assets", "player", "hair_small.png")).convert_alpha())
						hair_small2 = Hair(hair_small, pygame.image.load(join("assets", "player", "hair_small.png")).convert_alpha())
						self.objects.add(hair_big, hair_mid, hair_mid2, hair_small, hair_small2, player)


					elif layer.name == "npc":
						npc = NPC((obj.x, obj.y), self.collision_tiles, obj.name, player, self.camera_group, self.ui_group)
						self.objects.add(npc)

					elif layer.name == "checkpoints":
						self.checkpoints[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)


	def run(self):
		# input loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.terminate() # crashes the game lol
				if event.key == pygame.K_SPACE:
					self.player.jump = True
					for obj in self.ui_group:
						if obj.id == "dialog_box":
							obj.next_line()


		# game logic:
		self.objects.update()
		self.ui_group.update()
		# rendering:
		self.screen.fill("black")
		self.camera_group.custom_draw()
		self.ui_group.draw(self.screen)
		
