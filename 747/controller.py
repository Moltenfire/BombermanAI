from bomberman import read_line, print_map, print_players, send_action, send_message
import random

class controller:

    def __init__(self, s):
        self.account = "747"
        self.password = "747"   
        # self.account = "火"
        # self.password = "fire"
        self.s = s
        self.map = []    
        self.players = {}   # {'name': [[row, col], alive], }
        self.bombs = []     # [[[row, col], time], ]
        self.explosions = [] # [[row, col], ]
        self.bomb_num = 0
        self.bombs_to_explode = []
        
        #AI variables
        self.current_state = "0" # 0 = Start, 
        self.current_target = [] # [row, col]
        self.current_path = [] # List of instuctions.
        
    def start(self):
        # register for current game
        if self.register():
            
            
            # Get Map
            self.get_map()
            
            print_map(self.map, self.players, self.bombs)
                        
            # Get Players
            self.get_players()
            
            print_players(self.players)
            
            self.main()
                   
    def register(self):
        str = ' '.join(['REGISTER', self.account, self.password])
        print str
        send_message(self.s, str)
        
        if read_line(self.s) == 'REGISTERED':
            print 'REGISTERED\n'
            return True
        else:
            return False

    def get_map(self):
        map_size = read_line(self.s).split()
        self.rows = int(map_size[1])
        self.cols = int(map_size[2])
        
        for i in range(self.rows):
            row = read_line(self.s).replace('0', '_').replace('1', '+').replace('2', '#').split()
            self.map.append(row)
            
    def get_players(self):
        player_numbers = read_line(self.s).split()
        num = int(player_numbers[1])
        
        for i in range(num):
            p = read_line(self.s).split()
            self.players[p[0]] = [[int(p[1]), int(p[2])], True]
                    
    def main(self):
    
        self.get_move()
        playing = True
    
        while playing:
            data = read_line(self.s).split()
            # print "Data:", data
            if data[0] == "END":
                playing = False
                break
            elif data[0] == "TICK":
                
                print "Tick:", data[1]
            elif data[0] == "ACTIONS":
                print "ACTIONS", data[1]
                
                for i in range(int(data[1])):
                    action = read_line(self.s).split()
                    self.perform_action(action)
                
                print_map(self.map, self.players, self.bombs, self.explosions)
                self.explosions = []
                print_players(self.players)
                
                self.tick_Bombs()
                
                self.get_move()
            elif data[0] == "DEAD":
                print "DEAD", data[1]
                
                for i in range(int(data[1])):
                    x = read_line(self.s).split()
                    print x
             
            elif data[0] == "LEFT" or data[0] == "RIGHT" or data[0] == "UP" or data[0] == "DOWN" or data[0] == "BOMB":
                print "Action accepted:", data[0]
                
            else:
                print "Error:", data
                print_map(self.map, self.players, self.bombs, self.explosions)    
                self.explosions = []
                
        print "\n--- Game End ---\n"

    def perform_action(self, action):
        name = action[0]
        type = action[1]
        row = self.players[name][0][0]
        col = self.players[name][0][1]
        
        print name, type
        
        if type == "BOMB":
            add = True
            for i in self.bombs:
                if i[0] == [row, col]:
                    add = False
            
            if add:
                self.bombs.append([[row, col], 5])
        elif type == "UP":
            if col != 0 and self.wall_check(row - 1, col):
                self.players[name][0][0] -= 1
        elif type == "DOWN":
            if col != 0 and self.wall_check(row + 1, col):
                self.players[name][0][0] += 1  
        elif type == "LEFT":
            if col != 0 and self.wall_check(row, col - 1):
                self.players[name][0][1] -= 1
        elif type == "RIGHT":
            if col != 0 and self.wall_check(row, col + 1):
                self.players[name][0][1] += 1
              
    def wall_check(self, row, col):
        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            print "At Wall"
            return False
        else:
            for i in self.bombs:
                if i[0] == [row, col]:
                    return False
                    
            if self.map[row][col] == "_":
                return True
            else:
                return False
                
    def tick_Bombs(self):
        for i in self.bombs:
            # print i[0]
            # print i[1] - 1, "\n"
            i[1] -= 1
            if i[1] == 0:
                # print "BOOM!"
                
                self.explode(i)
                
        if len(self.bombs_to_explode) != 0:
            self.explode(self.bombs_to_explode[0])
            
    def explode(self, bomb):
        row = bomb[0][0]
        col = bomb[0][1]
        e = [[row,col]]
        try:
            self.bombs.remove(bomb)            
        except:
            self.bombs_to_explode.remove(bomb)
            
        hit_bombs = []
        
        #Up
        for i in range(1,4):
            x = row - i
            if x < 0:
                break
            else:
                m = self.map[x][col]
                
            if m == "#":
                break
            elif m == "+":
                self.map[x][col] = "_"
                e.append([x,col])
                break
            else:
                e.append([x,col])        
                
        #Down
        for i in range(1,4):
            x = row + i
            if x >= self.rows:
                break
            else:
                m = self.map[x][col]
                
            if m == "#":
                break
            elif m == "+":
                self.map[x][col] = "_"
                e.append([x,col])
                break
            else:
                e.append([x,col])
                
        #Left
        for i in range(1,4):
            x = col - i
            if x < 0:
                break
            else:
                m = self.map[row][x]
                
            if m == "#":
                break
            elif m == "+":
                self.map[row][x] = "_"
                e.append([row,x])
                break
            else:
                e.append([row,x])
                
        #Down
        for i in range(1,4):
            x = col + i
            if x >= self.cols:
                break
            else:
                m = self.map[row][x]
                
            if m == "#":
                break
            elif m == "+":
                self.map[row][x] = "_"
                e.append([row,x])
                break
            else:
                e.append([row,x])
                
                
        print e
        
        for i in e:
            for j in self.bombs:
                if i[0] == j[0][0] and i[1] == j[0][1]:
                    hit_bombs.append(j)
                    self.bombs.remove(j)
        
        self.explosions.extend(e)
        self.bombs_to_explode.extend(hit_bombs)
        
    
    def get_move(self):
        actions = ["LEFT", "RIGHT", "UP", "DOWN"]
        send_action(self.s, random.choice(actions))
        
        
class point_map:

    def __init__(self, map, rows, cols):
        self.rows = rows
        self.cols = cols
        
        
        
class point:

    def __init__(self, row, col, block):
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.row = row
        self.col = col
        self.block = block
        self.bomb = None
        self.person = None
        
    def set_relations(self, N, S, E, W):
        self.north = N
        self.south = S
        self.east = E
        self.west = W
        
    def explode(self):
        if block == "+":
            block = "_"
            return 0
        elif block = "#":
            return 0
        else:
            return 1
        