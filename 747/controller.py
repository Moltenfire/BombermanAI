from bomberman import read_line, print_map, print_players, send_action, send_message

class controller:

    def __init__(self, s):
        self.account = "747"
        self.password = "747"
        self.s = s
        self.map = []    
        self.players = {}   # {'name': [[row, col], alive], }
        self.bombs = []     # [[[row, col], time], ]
        self.bomb_num = 0
        
    def start(self):
        # register for current game
        if self.register():
            
            
            # Get Map
            self.get_map()
                        
            # Get Players
            self.get_players()

            print_map(self.map, self.players)
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
        while True:
            data = read_line(self.s).split()
            if data[0] == "END":
                break
            elif data[0] == "TICK":
                
                print "Tick:", data[1]
            elif data[0] == "ACTIONS":
                print "ACTIONS", data[1]
                
                for i in range(int(data[1])):
                    action = read_line(self.s).split()
                    self.perform_action(action)
                
                print_map(self.map, self.players)
                print_players(self.players)
                
                self.get_move()


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
                
    def get_move(self):
        send_action(s, "BOMB")
            
        
        
    
             