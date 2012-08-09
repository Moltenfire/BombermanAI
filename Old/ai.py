import copy, random, sys

class AI:

	def __init__(self, account, grid, players, bombs, rows, cols):
		self.account = account
		self.grid = copy.deepcopy(grid)
		self.players = players
		self.bombs = bombs
		self.rows = rows
		self.cols = cols
		# Set current goal
		# self.printMap()
		
	
	def update(self, grid, players, bombs):
		self.grid = copy.deepcopy(grid)
		self.players = players
		self.bombs = bombs
		self.toExplode = set()
		self.exploded = set()
		
		#Work out danger squares, moves to avoid this turn or have to take
		
		for i in self.bombs:			
			if i[2] == 1 and i[3] not in self.toExplode:
				self.toExplode.add(i[3])
				
		print self.bombs, self.toExplode
		
		while len(self.toExplode.difference(self.exploded)) != 0:
			for i in self.toExplode.difference(self.exploded):
				for j in self.bombs:
					if i == j[3]:
						print "Exploding: ", j
						self.explodeBomb(j)
						
		self.printMap()
										
	def explodeBomb(self, x):
		self.exploded.add(x[3])
		
		r = x[0]
		c = x[1]
	
		self.explode(r, c)
		
		print "Before: ", self.grid[r][c]
		self.grid[r][c] = "1"
		print "After: ", self.grid[r][c]
		
		#Left
		for i in range(1,4):
			if self.explode(r, c-i):
				break
			else:
				self.grid[r][c-i] = "1"
		#Right
		for i in range(1,4):
			if self.explode(r, c+i):
				break
			else:
				self.grid[r][c+i] = "1"
		#Up
		for i in range(1,4):
			if self.explode(r-i, c):
				break
			else:
				self.grid[r-i][c] = "1"
		#Down
		for i in range(1,4):
			if self.explode(r+i, c):
				break
			else:
				self.grid[r+i][c] = "1"
				
	def explode(self, r, c):
		
		if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
			return 1
			
 		if self.grid[r][c] == " ":
			for i in self.bombs:
				if i[0] == r and i[1] == c:
					self.toExplode.add(i[3])
			return 0
		elif self.grid[r][c] == "+":
			self.grid[r][c] = " "
			return 1
		elif self.grid[r][c] == "#":
			return 1

	
	def getMove(self):
		i = random.randint(0,5)
		
		# if i == 0:
			# self.plantBomb()
		# else:
		return self.randomMove()
		
	def randomMove(self):

		moves = self.legalMoves()
		
		if moves != []:
			return random.choice(moves)
		else:
			return None
		
	def nearestSafeSquare(self, r, c):
		pass
		# Returns the distance to the nearest safe square
				
	def legalMoves(self):
		directions = ["LEFT", "UP", "RIGHT", "DOWN"]
		moves = ["BOMB"]
		r = self.players[self.account].position[0]
		c =	self.players[self.account].position[1]
		
		if r == 0:
			directions.remove("UP")
		elif r == (self.rows - 1):
			directions.remove("DOWN")
			
		if c == 0:
			directions.remove("LEFT")
		elif c == (self.cols - 1):
			directions.remove("RIGHT")
			
		print directions
			
		for i in directions:
			if self.isLegal(i, r, c):
				moves.append(i)
		
		print moves
		return moves
				
	def isLegal(self, d, r, c):

		if d == "LEFT":
			if self.grid[r][c-1] == " ":
				return 1
		elif d == "RIGHT":
			if self.grid[r][c+1] == " ":
				return 1
		elif d == "UP":
			if self.grid[r-1][c] == " ":
				return 1
		elif d == "DOWN":
			if self.grid[r+1][c] == " ":
				return 1				
			
		return 0

		
	def printMap(self):
		if self.grid != []:
			g = copy.deepcopy(self.grid)
			
			for i in self.players:
				if self.players[i].alive:
					g[self.players[i].position[0]][self.players[i].position[1]] = "X"
					
			for i in self.bombs:
				g[i[0]][i[1]] = "B"
						
			# for i in self.explosions:
				# g[i[0]][i[1]] = "*"
				
			print "-" * ((self.cols * 2) - 1)
			for j in g:
				s = " ".join(j)
				print s
			print "-" * ((self.cols * 2) - 1)