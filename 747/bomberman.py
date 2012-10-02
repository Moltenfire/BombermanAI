from copy import deepcopy

def print_map(map, players=[], bombs=[]):

    playermap = deepcopy(map)
    bombmap = deepcopy(map)
    p = []
    b = []
    
    for i in players:
        row = players[i][0][0]
        col = players[i][0][1]
        playermap[row][col] = "X"
        
    for i in bombs:
        row = i[0][0]
        col = i[0][1]        
        bombmap[row][col] = "B"
    
    for i in playermap:
        # p.append(''.join(i))
        p.append(''.join(i).replace("_"," "))
    
    
    for i in bombmap:
        # b.append(''.join(i))
        b.append(''.join(i).replace("_"," "))
    
    for i in range(len(p)):
        print p[i], "   ", b[i]
    
    print ""
        
def print_players(players):

    for i in players:
        print "Player:  ", i
        print "Location: [%s, %s]" % (players[i][0][0], players[i][0][1])
        print "Status  : Alive\n" if players[i][1] else "Status  : Dead\n"

def read_line(s):
    str = ''
    
    while True:
        c = s.recv(1)
        
        if c == '\n' or c == '':
				break
        else:
            str = ''.join([str,c])
            
    return str
    
def send_action(s, action):
    if action != None:
        send_message(s, "ACTION %s" % action) 
    
def send_message(s, message):
    if message != None or message != '':
        s.send(message)