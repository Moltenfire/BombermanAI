def read_line(s):
    str = ''
    
    while True:
        c = s.recv(1)
        
        if c == '\n' or c == '':
				break
        else:
            str = ''.join([str,c])
            
    return str
    
def print_map(map, players=[], bombs=[]):
    
    for i in map:
        print ' '.join(i)