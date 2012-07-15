import copy, random

class AI:

	def __init__(self, account, grid, players, bombs, rows, cols):
		self.account = account
		self.grid = copy.deepcopy(grid)
		self.players = players
		self.bombs = bombs
		self.rows = rows
		self.cols = cols
		# Set current goal
		
	
	def update(self, grid, players, bombs):
		self.grid = copy.deepcopy(grid)
		self.players = players
		self.bombs = bombs
		
		#Work out danger squares, moves to avoid this turn or have to take
		
		for i in self.bombs:
			self.exploded = set()
			if i[2] == 1 and i[3] not in self.exploded:
				self.exploded.add(i[3])
				
	# def explodeBomb(self, x):
		# self.explode(x[0], x[1])
		
		# #Left
		# for i in range(1,4):
			# if self.explode(x[0], x[1]-i):
				# break			
		# #Right
		# for i in range(1,4):
			# if self.explode(x[0], x[1]+i):
				# break
		# #Up
		# for i in range(1,4):
			# if self.explode(x[0]-i, x[1]):
				# break			
		# #Down
		# for i in range(1,4):
			# if self.explode(x[0]+i, x[1]):
				# break
				
	# def explode(self, r, c):
		
		# if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
			# return 1
			
		# for i in self.playerInfo:
			# if self.playerInfo[i].position[0] == r and self.playerInfo[i].position[1] == c:
				# self.playerInfo[i].kill()
				# if self.playerInfo[i].name == self.account:
					# self.inGame = False

		# if self.grid[r][c] == " ":
			# self.explosions.add((r,c))
			# for i in self.bombs:
				# if i[0] == r and i[1] == c:
					# self.explodeBomb(i)
					# break								
			# return 0
		# elif self.grid[r][c] == "+":
			# self.explosions.add((r,c))
			# self.grid[r][c] = " "
			# return 1
		# elif self.grid[r][c] == "#":
			# return 1

	
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