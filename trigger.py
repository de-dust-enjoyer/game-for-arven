import pygame

class Trigger(pygame.sprite.Sprite):
	def __init__(self, id: str, rect: pygame.Rect, target, method=None, attribute: str = None, set_true_if_inside: bool = False):
		super().__init__()
		self.id = id
		self.dead = False # objects need this
		self.rect = rect
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.image.fill((0,0,200, 40))
		self.target = target
		self.method = method
		self.attribute = attribute  # Should be string (attribute name)
		self.set_true_if_inside = set_true_if_inside

	def update(self):
		is_colliding = self.rect.colliderect(self.target.collision_rect)

		if self.attribute:
			if not hasattr(self.target, "trigger_states"):
				self.target.trigger_states = {}
			if self.attribute not in self.target.trigger_states:
				self.target.trigger_states[self.attribute] = set()


		if is_colliding:
            # Call method if provided
			if self.method:
				self.method()


			if self.attribute:
				self.target.trigger_states[self.attribute].add(self.id)
				value = bool(self.target.trigger_states[self.attribute]) if self.set_true_if_inside else False
				setattr(self.target, self.attribute, value)
			
		else:
			# Only modify attribute if we're managing it
			if self.attribute and hasattr(self.target, "trigger_states"):

				self.target.trigger_states[self.attribute].discard(self.id)

				has_active = bool(self.target.trigger_states[self.attribute])
				value = has_active if self.set_true_if_inside else not has_active
				setattr(self.target, self.attribute, value)

	def scale_by(self, scale:float):
		scaled_img = pygame.transform.scale_by(self.image, scale)
		return scaled_img