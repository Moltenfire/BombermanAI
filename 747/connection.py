import socket, sys
import controller
from bomberman import read_line
        
# TCP_IP = 'uwcs.co.uk'
TCP_IP = '127.0.0.1'
TCP_PORT = 8037
BUFFER_SIZE = 1024	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:    
    s.connect((TCP_IP, TCP_PORT))
except:
    print "Failed: Could not connect"
    sys.exit(1) 
    
while 1:
    data = read_line(s)
    print "Server:", data
    if data == "INIT":
        print "\n--- New Game ---\n"
        c = controller.controller(s)
        c.start()
        # sys.exit()