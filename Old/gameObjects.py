class Player:
	
	def __init__(self, name, r, c):
		
		self.name = name
		self.position = [r, c]
		self.alive = True
	
	def getData(self):
		print "Name: ", self.name
		print "Position: ", self.position
		print "Alive: ", self.alive
		
	def move(self, d):
		if d == "LEFT":
			self.position[1] -= 1
		elif d == "RIGHT":
			self.position[1] += 1
		elif d == "UP":
			self.position[0] -= 1
		elif d == "DOWN":
			self.position[0] += 1
			
	def kill(self):
		self.alive = False