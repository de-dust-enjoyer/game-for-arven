class GameStateManager:
	def __init__(self, current_state):
		self.current_state = current_state

	def get_state(self):
		return self.current_state

	def set_state(self, new_state):
		self.current_state = new_state