
# coding: utf-8

# In[1]:


import socket
import sys
from _thread import *


# In[2]:


host =''
port = 8006
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # To reuse the port immediately and notwait for the time out


# In[3]:


try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))


# In[4]:


s.listen(5)
print('Waiting for a connection.')


# In[5]:


no_of_clients=0
agreements =0


# In[6]:


def threaded_client(conn):
    global no_of_clients
    global agreements
    # This is the scope of the current connection !
    # Put the information dictionary containing the name, port and address here
    client_info={}
    conn.send(str.encode(("You are clinet #{}\n").format(str(no_of_clients+1))))
    
    no_of_clients+=1
    if (no_of_clients>2):
        msg="**************Two players are already quizzing*********************\n"
        conn.sendall(str.encode(msg))
        no_of_clients-=1
        conn.close()
    else :
        client_info["port"] = conn.getpeername()[1]
        
        conn.send(str.encode('Type your name !\n'))
        client_info["name"]=str(conn.recv(2048).decode('utf-8'))
        conn.send(str.encode(("Hey {} Welcome to 1 on 1 quizzing").format(client_info["name"])))
        # Now the quiziing will start when both the clients will be ready !
        # A global variable needed to maintain yeses , if two then go ahead
        conn.send(str.encode("Are you up for the quiz ? [y/n]\n"))

        if((conn.recv(2048))) == b'y\n':
            # Lets start quizzing !
            agreements+=1
            if (agreements == 1):
                conn.send(str.encode(("Please wait for the other player")))
                while True:
                    if (agreements == 2):
                        break

            print(agreements)
            conn.send(str.encode(("It starts now")))
            # Quizzing actually starts
            # Lets code it out
            while True:
                data = conn.recv(2048)
                reply='Server Output : '+data.decode('utf-8')
                print(str(data.decode('utf-8')) == "exit\r\n")
                if str(data.decode('utf-8')) == "exit\r\n":
                    print("Bye Bye {}".format(str(client_info["port"])))
                    break
                conn.sendall(str.encode(reply))
        else :
            conn.send(str.encode("Anyways , thanks for your time !\n"))
        no_of_clients -= 1
        print("Number of existing clients : ",no_of_clients)
        conn.close()


while True:
    try:
        conn, addr = s.accept()
        print('connected to : '+addr[0]+':'+str(addr[1]))
        print("Hey\n")
        start_new_thread(threaded_client,(conn,))
    except KeyboardInterrupt as e:
        conn.close()
        sys.exit()