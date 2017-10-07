'''
    udp socket client
    Silver Moon
'''
 
import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket


def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()


if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print ('Usage : python telnet.py hostname port')
        sys.exit()


    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()


    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
    print ('Connected to remote host. Start sending messages')
    
    while(1) :
        msg = raw_input('Enter message to send : ')
         
        try :
            #Set the whole string
            s.sendto(msg, (host, port))
             
            # receive data from client (data, addr)
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
             
            print ('Server reply : ' + reply)
         
        except socket.error, msg:
            print ('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()