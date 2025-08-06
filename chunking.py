def get_nearby_tiles(player_pos, chunk_dict, chunk_size, radius_in_chunks=1):
		chunk_x = int(player_pos[0] // chunk_size)
		chunk_y = int(player_pos[1] // chunk_size)
		nearby_tiles = []
		for dx in range(-radius_in_chunks, radius_in_chunks +1):
			for dy in range(-radius_in_chunks, radius_in_chunks +1):
				key = (chunk_x + dx, chunk_y + dy)
				nearby_tiles.extend(chunk_dict.get(key, []))
		return nearby_tiles