import time
# needs a duration and optionally if the timer should repeat. if timer is finnished it will return True
class Timer:
	def __init__(self, duration:float, repeat:bool = False, return_true_when_stopped = False):
		self.time_target = duration
		self.repeat = repeat
		self.running = False
		self.return_true_when_stopped = return_true_when_stopped
		self.old_time = time.time()

	def set_duration(self, duration):
		if self.time_target != duration:
			self.time_target = duration
	
	def start(self, refresh:bool=False):
		if not refresh:
			if not self.running:
				self.old_time = time.time()
				self.running = True
		else:
			self.old_time = time.time()
			self.running = True


	def stop(self):
		self.running = False

	def toggle(self):
		self.running = not self.running

	def is_running(self):
		return self.running

	def time_left(self):
		if not self.running:
			return 0
		else:
			return self.time_target - (time.time() - self.old_time)

	def update(self):
		if self.running:
			if time.time() - self.old_time >= self.time_target:
				if not self.repeat:
					self.stop()
					return True
				else:
					self.stop()
					self.start()
					return True
			else:
				return False
		elif self.return_true_when_stopped:
			return True

