from bomberman import read_line, print_map

class controller:

    def __init__(self, s):
        self.account = "747"
        self.password = "747"
        self.s = s
        self.map = []
        
        
    def start(self):
        # register for current game
        if self.register():
    
            # Get Map
            self.get_map()
        
    def register(self):
        str = ' '.join(['REGISTER', self.account, self.password])
        print str
        self.send_message(str)
        
        if read_line(self.s) == 'REGISTERED':
            print 'REGISTERED'
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

    def send_message(self, message):
        if message != None or message != '':
            self.s.send(message)
             