import socket
import sys
from _thread import *
from sys import getsizeof
import pickle


host =''
port = 8006
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # To reuse the port immediately and notwait for the time out

# a list of question and options and correct answer, question is str type option is a again a a list of 4 strings
questions =["Whats 1+1","Whats 1+2","Whats 1+3","Whats 1+4","Whats 1+5","Whats 1+6","Whats 1+7","Whats 8+1","Whats 9+1","Whats 10+1"]
answers=['2','3','4','5','6','7','8','9','10','11']
try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))


s.listen(5)
print('Waiting for a connection.')


no_of_clients=0
agreements =0
total_questions = 0
players=[]
turn=0


def threaded_client(conn):
    global no_of_clients
    global agreements
    global total_questions
    ques_to_me=0
    my_score=0
    global players
    global turn
    # This is the scope of the current connection !
    # Put the information dictionary containing the name, port and address here
    client_info={}
    conn.send(str.encode(("You are clinet #{}\n").format(str(no_of_clients+1))))
    
    no_of_clients+=1
    if (no_of_clients>2):
        msg="**************Two players are already quizzing******************\n"
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
            my_pos=len(players)
            players.append(conn)
            if (agreements == 1):
                conn.send(str.encode(("Please wait for the other player")))
                while True:
                    if (agreements == 2):
                        break

            print(agreements)
            conn.send(str.encode(("It starts now")))
            # Quizzing actually starts
            # First , just append this connection object in the players list !
            
            conn.send(str.encode(("Your position is {}\n").format(my_pos)))
            
            if (my_pos == 0):
            	other_pos =1
            else:
            	other_pos =0

            while True:
            	if(turn==my_pos):
            		ques_to_me+=1
            		conn.send(str.encode(questions[total_questions]))
            		
            		data = conn.recv(2048)
            		answer = data.decode('utf-8').rstrip()
            		#if (answer==answers[total_questions]):
            		curr_ans=answers[total_questions]
            		if((answer)) == curr_ans:
            			conn.send(str.encode("That was correct!\n"))
            			my_score+=10
            		else:
            			conn.send(str.encode(("Sorry that wasn't correct!\n , correct answer is {}").format(curr_ans)))
            		total_questions+=1
            		#change_turn()
            		if (my_pos == 0):
            			turn =1
            		else:
            			turn =0
            	if (ques_to_me==4):
            		break
            conn.send(str.encode(("\nThanks for playing . Your final score is {}!\n").format(my_score)))
        else :
            conn.send(str.encode("\nAnyways , thanks for your time !\n"))
        players.remove(conn)
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