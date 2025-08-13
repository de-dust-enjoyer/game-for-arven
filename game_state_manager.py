from transition_screen import TransitionScreen

class GameStateManager:
	def __init__(self, current_state, ui_group):
		self.current_state = current_state
		
		self.ui_group = ui_group

	def transition_state(self, new_state):
		if new_state != self.current_state:
			transition_screen = TransitionScreen(self.set_state, new_state, self.ui_group)

	def get_state(self):
		return self.current_state

	def set_state(self, new_state):
		self.current_state = new_state