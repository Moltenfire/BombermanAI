import copy, random, socket, sys
import ai, gameObjects

class Bomberman:

	def __init__(self, account, password):
	
		self.TCP_IP = 'uwcs.co.uk'
		self.TCP_PORT = 8037
		self.BUFFER_SIZE = 1024	
		self.account = account
		self.password = password
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect()
		self.setVariables()
		
		#receive sever data
		self.getMessages() 
		
	def setVariables(self):
		self.grid = []
		self.playerInfo = {}
		self.bombs = []
		self.explosions = set()
		self.inGame = False
		self.sentAction = False
		self.rows = 0
		self.cols = 0
		self.bombNum = 1
		self.numberPlayers = 0
					
	def connect(self):
		try:			
			self.s.connect((self.TCP_IP, self.TCP_PORT))
		except:
			print "Failed: Could not connect"
			sys.exit()
			
	def sendMessage(self, message):
		print "Sent: ", message, "\n"
		self.s.send(message)
			def getMessages(self):
		while 1:	
			data = self.read_line()
			self.parseline(data)
			
	def sendAction(self, action):
		#Add in a check so only valid actions are sent.
		if not self.sentAction and self.inGame:
			if action != None:
				self.sendMessage(" ".join(["ACTION", action]))
			self.sentAction = True
			
	def printMap(self):
		if self.grid != [] and False:
			g = copy.deepcopy(self.grid)
			
			for i in self.bombs:
				g[i[0]][i[1]] = "B"
			
			for i in self.playerInfo:
				if self.playerInfo[i].alive:
					g[self.playerInfo[i].position[0]][self.playerInfo[i].position[1]] = "X"
						
			for i in self.explosions:
				g[i[0]][i[1]] = "*"
				
			print "-" * ((self.cols * 2) - 1)
			for j in g:
				s = " ".join(j)
				print s
			print "-" * ((self.cols * 2) - 1)
			
	def read_line(self):
		ret = ''

		while True:
			c = self.s.recv(1)

			if c == '\n' or c == '':
				break
			else:
				ret = ''.join([ret,c])
		
		# Prints all data sent from server
		print "Server: ", ret
		
		return ret
			
	def parseline(self, l):
		phrases = { "DEAD": self.dead, "INIT": self.register, "MAP": self.createMap, "PLAYERS": self.players, "REGISTERED": self.registered, "STOP": self.stop, "END": self.stop, "TICK": self.tick, "ACTIONS": self.actions, "LEFT": self.confirmation, "RIGHT": self.confirmation, "DOWN": self.confirmation, "UP": self.confirmation, "BOMB": self.confirmation } 
		
		# { "DEAD": dead, "END": end, "SCORES": scores }
		
		x = l.split()
		phrases[x[0]](x)			
		
	def register(self, x):
		m = "REGISTER " + self.account + " " + self.password
		self.sendMessage(m)
		
	def registered(self, x):
		self.inGame = True
		self.ai = ai.AI(self.account, self.grid, self.playerInfo, self.bombs, self.rows, self.cols)
	
	def stop(self, x):
		#reset everything and wait for next round
		self.setVariables()
		
	def confirmation(self, x):
		pass
		
	def actions(self, x):
		# Update with last turns actions
		if x[1] != "0":
			for i in range(int(x[1])):
				y = self.read_line().split()
				if y[1] == "BOMB":
					self.dropBomb(self.playerInfo[y[0]].position)
				elif self.isLegal(self.playerInfo[y[0]].position,y[1]):
					self.playerInfo[y[0]].move(y[1])
				
		# Simulate Bombs
		self.updateBombs()
		
		# Perform a move
		if self.inGame:
			self.ai.update(self.grid, self.playerInfo, self.bombs)
			self.printMap()
			self.sendAction(self.ai.getMove())
			
	def isLegal(self, position, move):
		r = position[0]
		c = position[1]
		
		if move == "LEFT" and c != 0:
			if self.grid[r][c-1] == "0":
				return 1
		elif move == "RIGHT" and c != (self.cols - 1):
			if self.grid[r][c+1] == "0":
				return 1
		elif move == "UP" and r != 0:
			if self.grid[r-1][c] == "0":
				return 1
		elif move == "DOWN" and r != (self.rows - 1):
			if self.grid[r+1][c] == "0":
				return 1
		
	def dropBomb(self, x):
		self.bombs.append([x[0],x[1],4,self.bombNum])
		self.bombNum += 1
		
	def updateBombs(self):
		for i in self.bombs:
			i[2] -= 1
			if i[2] == 0:				
				self.explodeBomb(i)
				
	def explodeBomb(self, x):
		self.bombs.remove(x)
		self.explode(x[0], x[1])
		
		#Left
		for i in range(1,4):
			if self.explode(x[0], x[1]-i):
				break			
		#Right
		for i in range(1,4):
			if self.explode(x[0], x[1]+i):
				break
		#Up
		for i in range(1,4):
			if self.explode(x[0]-i, x[1]):
				break			
		#Down
		for i in range(1,4):
			if self.explode(x[0]+i, x[1]):
				break
				
	def explode(self, r, c):
		
		if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
			return 1
			
		for i in self.playerInfo:
			if self.playerInfo[i].position[0] == r and self.playerInfo[i].position[1] == c:
				self.playerInfo[i].kill()
				if self.playerInfo[i].name == self.account:
					self.inGame = False

		if self.grid[r][c] == " ":
			self.explosions.add((r,c))
			for i in self.bombs:
				if i[0] == r and i[1] == c:
					self.explodeBomb(i)
					break								
			return 0
		elif self.grid[r][c] == "+":
			self.explosions.add((r,c))
			self.grid[r][c] = " "
			return 1
		elif self.grid[r][c] == "#":
			return 1
	
	def dead(self, x):
		for i in range(int(x[1])):
			y = self.read_line().split()
			self.playerInfo[y[0]].kill()
			if y[0] == self.account:
				self.inGame = False
					
	def createMap(self, x):
		self.rows = int(x[1])
		self.cols = int(x[2])
		for i in range(self.rows):
			y = self.read_line().replace(" ", "|").replace("0", " ").replace("1", "+").replace("2", "#").split("|")
			self.grid.append(y)
			
	def players(self, x):
		self.numberPlayers = int(x[1])
		for i in range(self.numberPlayers):
			y = self.read_line().split()
			self.playerInfo[y[0]] = gameObjects.Player(y[0],int(y[1]),int(y[2]))		
	def tick(self, x):
		if self.inGame:
			num = int(x[1])
			self.sentAction = False
			
			
	
