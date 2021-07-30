import sympy
import random
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import hashlib
import socket
import select
import sys
import random
from random import randint
import os
from _thread import *

clientIP = [None]*4
client_port_as_server = 50000
clinet_port_as_clinet = 50001
p = 23
g = 9

client_port_as_server = random.randrange(60000, 62000)
IP_address = str(sys.argv[1])

def clientthread(conn, addr):

    modemsg = conn.recv(1024)
    # print ("mode msg : ", str(modemsg))
    modemsg = modemsg.decode().strip().split();
    if(modemsg[0]=="group"):
    	conn.send("hello".encode())

    
    if(modemsg[0]=="p2p"):
        # key generation
        b = random.randint(10000, 50000)
        kb = pow(g, b)
        kb = kb % p
        # print("kb ",kb)

        # send key
        conn.send(str(kb).encode())

        # recieve key
        ka = conn.recv(1024)
        # print("ka ",ka)
        ka = ka.decode()
        # conn.send("hello".encode())
        # print("ka recievd ",ka)
        m_l=len(ka)
        mode=int(ka[m_l-1])
        ka=ka[:m_l-4]

        sharedkeyatB = (pow(int(ka), b)) % p
        sharedkeyatB = str(sharedkeyatB)+str(2020202009)
        theHash1 = hashlib.sha256(str(sharedkeyatB).encode("utf-8")).hexdigest()

        key1 = theHash1[0:16]
        cipher1 = DES3.new(key1, DES3.MODE_ECB)

        # print("connection from ", addr[1])

        # print("inside while mode ",mode)
        if(mode==1):
        	# print("inside while mode ",mode)
        	conn.send("hello".encode())
        	message = conn.recv(1024)
        	# print("after recieve",message)
        	conn.send("hello".encode())
        	# print("inside file mode messag erecieved ",message)
        	# message = message.decode()
        	message_list = message.decode().split()
        	# print("first message recievd in file ", message_list)
        	if(len(message_list)>3 and  message_list[0] == "send" and message_list[2] == "file"):
        		# print("inside file recieved")
        		dir_path = os.path.dirname(os.path.realpath(__file__))
        		filename = message_list[3]
        		new_file_path = dir_path+"/"+filename
        		file = open(new_file_path, 'wb')
        		while True:
        			data = conn.recv(1024)
        			data = cipher1.decrypt((data))
        			data = data
        			# print(data)
        			if not data:
        				break
        			file.write(data)

        		file.close()
        	else:
        		print("gibberish")
        	# data = cipher1.decrypt((message_list[2]))
        	# print("details of client", data)
        else:
        	conn.send("hello".encode())
        	message = conn.recv(1024)
        	# print("recievd encrypted message  is ",message)
        	data = cipher1.decrypt((message))
        	print(str(data.decode("utf-8")).strip())


    else:
        grpname = modemsg[2]
        # main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # main_server.connect((IP_address, serverPort))
        # print("sending main server grpname : ", grpname)
        msgToMainServer = "key " + grpname
        server.send(msgToMainServer.encode());

        grpKey = server.recv(1024)
        grpKey = grpKey.decode()
        # print ("grp key recv from main server : ", grpKey)

        cipher1 = DES3.new(grpKey, DES3.MODE_ECB)

        # print("connection from ", addr[1])

        # print("inside while mode ",modemsg)
        if(modemsg[1]=="file"):
            conn.send("hello".encode())
            message = conn.recv(1024)
            # print("after recieve",message)
            conn.send("hello".encode())
            # print("inside file mode messag erecieved ",message)
            # message = message.decode()
            message_list = message.decode().split()
            # print("first message recievd in file ", message_list)
            if(len(message_list)>3 and  message_list[0] == "send" and message_list[2] == "file"):
                # print("inside file recieved")
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = message_list[3]
                new_file_path = dir_path+"/"+filename
                file = open(new_file_path, 'wb')
                while True:
                	try:
                		data = conn.recv(1024)
                		data = cipher1.decrypt((data))
                		if not data:
                			break
                		file.write(data)
                	except Exception :
                		print ("all ok")

                file.close()
            else:
                print("invalid command")
            # data = cipher1.decrypt((message_list[2]))
            # print("details of client", data)
        else:
            message = conn.recv(1024)
            # print("recievd encrypted is ",message)
            data = cipher1.decrypt((message))
            print(str(data.decode("utf-8")).strip())


    sys.exit()
    # portdetails=message.split('-')
    # client_server_port=portdetails[1]
    # conn.send("Welcome to this chatroom!".encode())
    # print(type(addr))


def client_as_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP_address, client_port_as_server))
    server.listen(100)
    # print("started as server also")

    while True:
        conn, addr = server.accept()
        # list_of_clients.append(addr[1])
        # print(addr[0] + " connected")
        start_new_thread(clientthread, (conn, addr))

    # conn.close()
    server.close()


def connect_to_peer(message, text,key, mode):

    if mode == "p2p":
        port = int(message)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((IP_address, port))
        
        msg_to_peer ="p2p chat"
        server.send(msg_to_peer.encode());

        # recv key
        kb = server.recv(1024)
        kb = kb.decode()

        #  send key
        key=str(key)+"---0"
        # print("key sendding ",key)
        server.send((key).encode())

        sharedkeyatA = (pow(int(kb), a)) % p
        sharedkeyatA = str(sharedkeyatA)+str(2020202009)
        sharedkeyatA = int(sharedkeyatA)

        # server.send(first_message.encode())
        # server.recv(1024)

        theHash = hashlib.sha256(str(sharedkeyatA).encode("utf-8")).hexdigest()
        thekey = theHash[0:16]
        cipher = DES3.new(thekey, DES3.MODE_ECB)
        server.recv(1024)
        while(len(text)%8!=0):
        	text+=" "
        text = cipher.encrypt((str.encode(text)))
        server.send(text)
        print("message send")

    else:
    	# print ("in group connect to peer : ")
    	port = int(message)
    	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server.connect((IP_address, port))
    	grpname = mode
    	msg_to_peer = "group chat " + grpname;
    	# print("send group caht" ,msg_to_peer)
    	server.send(msg_to_peer.encode());
    	cipher = DES3.new(key, DES3.MODE_ECB)
    	server.recv(1024)
    	while(len(text)%8!=0):
    		text+=" "
    	text = cipher.encrypt((str.encode(text)))
    	server.send(text)
    	print("message send")
    sys.exit()




def connect_to_peer_send_file(message, filename, key, mode):
    
    if mode=="p2p":
        port = int(message)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((IP_address, port))
        msg_to_peer ="p2p file"
        server.send(msg_to_peer.encode());
        # server.connect((ip, port))
        file_to_send = filename
        first_message = "send user file "+filename
        # print("first_message from sender ", first_message)

        # recv key
        kb = server.recv(1024)
        kb = kb.decode()

        #  send key
        key=str(key)+"---1"

        # print("key send ",key)


        server.send((key).encode())
        sharedkeyatA = (pow(int(kb), a)) % p
        sharedkeyatA = str(sharedkeyatA)+str(2020202009)
        sharedkeyatA = int(sharedkeyatA)
        server.recv(1024)
        server.send(first_message.encode())
        # print("after key send")
        server.recv(1024)

        theHash = hashlib.sha256(str(sharedkeyatA).encode("utf-8")).hexdigest()
        thekey = theHash[0:16]
        cipher = DES3.new(thekey, DES3.MODE_ECB)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_to_send = dir_path+"/"+file_to_send
        file_list=file_to_send.split('.')
        if(file_list[1]!="txt"):
        	send_file = open(file_to_send, 'rb')
        	# print("before while")
        	while True:
        		data = send_file.read(1024)
        		data_array=bytearray(data)
        		while(len(data_array)%8!=0):
        			data_array.append(0)

        		data = cipher.encrypt(((data_array)))
        		# print(data)
        		if not data:
        			break
        		server.send(data)



        else:
        	send_file = open(file_to_send, 'r')
        	# print("before while")
        	while True:
        		data = send_file.read(1024)
        		while(len(data)%8!=0):
        			data+=" "
        		data = cipher.encrypt((str.encode(data)))
        		# print(data)
        		if not data:
        			break
        		server.send(data)
            # server.recv(1024)

    else:
    	# print (" in connect_to_peer_send_file")
    	port = int(message)
    	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server.connect((IP_address, port))
    	grpname = mode
    	msg_to_peer = "group file " + grpname;
    	# print ("msg tp per : ", msg_to_peer)
    	server.send(msg_to_peer.encode());
    	# server.connect((ip, port))
    	file_to_send = filename
    	first_message = "send user file "+filename
    	# print("fi/rst_message from sender ", first_message)
    	server.recv(1024)
    	server.send(first_message.encode())
    	# print("after key send")
    	server.recv(1024)
    	cipher = DES3.new(key, DES3.MODE_ECB)
    	dir_path = os.path.dirname(os.path.realpath(__file__))
    	file_to_send = dir_path+"/"+file_to_send
    	file_list=file_to_send.split('.')
    	
    	if(file_list[1]!="txt"):
    		send_file = open(file_to_send, 'rb')
    		# print("before while")
    		while True:
    			data = send_file.read(1024)
    			data_array=bytearray(data)
    			while(len(data_array)%8!=0):
    				data_array.append(0)
    			data = cipher.encrypt(((data_array)))
    			# print(data)
    			if not data:
    				break
    			server.send(data)
    	else:
    		send_file = open(file_to_send, 'r')
    		# print("before while")
    		while True:
    			data = send_file.read(1024)
    			while(len(data)%8!=0):
    				data+=" "
    			data = cipher.encrypt((str.encode(data)))
    			# print(data)
    			if not data:
    				break
    			server.send(data)
     
    send_file.close()
    sys.exit()


# if len(sys.argv) != 3:
# 	print ("Correct usage: script, IP address, port number")
# 	exit()
IP_address = str(sys.argv[1])
serverPort = int(sys.argv[2])

# client as server
start_new_thread(client_as_server, ())

# client as client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP_address, serverPort))


message = IP_address+str('-')+str(client_port_as_server)
server.send(message.encode())
print("sending server clients details : ", message)
username = ""
while True:

    message = sys.stdin.readline()
    
    """
    convert msg to lowercase an then compare
    """

    #  key generation
    a = random.randint(10000, 50000)
    # print(a)
    ka = pow(g, a)
    ka = ka % p

    processed_input = message.split()
   
    if processed_input[0] == "signup":
        if len(processed_input) != 3:
            print ("invalid command ")
            continue
        server.send(message.encode())

        username = processed_input[1]
        # print("username ",username)
        messageFromServer = server.recv(1024)
        print(messageFromServer.decode())


    elif processed_input[0] == "signin":
        if len(processed_input) != 3:
            print ("invalid command ")
            continue
        server.send(message.encode())
        messageFromServer = server.recv(1024)
        print(messageFromServer.decode())
		

    elif(len(processed_input)>2 and processed_input[0] == "send" and processed_input[2] == "file"):
    	recvUsername = processed_input[1]
    	messageToServer = "send " +  recvUsername
    	server.send(messageToServer.encode())
    	messageFromServer = server.recv(1024)
    	message_split=messageFromServer.split()
    	if(message_split[0]=="error"):
    		print(messageFromServer)
    		continue
    	# print("recv port : ", messageFromServer.decode())
    	message = messageFromServer.decode()
    	# print("inside file transfer other client details ", message)
    	start_new_thread(connect_to_peer_send_file,
                         (message, processed_input[3], ka,"p2p"))
        # while True:
        # 	data=send_file.read(1024)
        # 	if not data:
        # 		break

    elif(processed_input[0] == "send" and processed_input[1]=="group"):
        grpName = processed_input[2]
        messageToServer = "send group " +  grpName
        server.send(messageToServer.encode())
        messageFromServer = server.recv(1024).decode()
        # print("key and recv port : ", messageFromServer.decode())
        message_split=messageFromServer.split()
        if(message_split[0]=="error"):
        	print(messageFromServer)
        	sys.stdout.flush()
        	continue
        list_of_ports = []
        messageFromServer = messageFromServer.split()
        groupkey = messageFromServer[0]
        for i in range(1,len(messageFromServer)):
            list_of_ports.append(int(messageFromServer[i]))

        # print ("list of ports : ", list_of_ports)
        # print("username in send group  ",username)
        text = "<" + username +"> "
        for i in range(3, len(processed_input)):
            text += " " + processed_input[i]


        # print ("msg to send : ", text)
        if processed_input[3]=="file":
        	# print ("in group send file ")
        	filename = processed_input[4]
        	for port in list_of_ports:
        		start_new_thread(connect_to_peer_send_file, (port, filename, groupkey, grpName))
        else:
        	for port in list_of_ports:
        		start_new_thread(connect_to_peer, (port, text, groupkey, grpName))
            # start_new_thread(connect_to_peer, (port, text, groupkey, grpName))


    elif(processed_input[0] == "send" and processed_input[1]!="group"):
        recvUsername = processed_input[1]
        messageToServer = "send " +  recvUsername
        server.send(messageToServer.encode())
        messageFromServer = server.recv(1024).decode()
        # print("recv port : ", messageFromServer.decode())
        message_split=messageFromServer.split()
        if(message_split[0]=="error"):
        	print(messageFromServer)
        	continue
        # print("username in p2p ",username)
        text = "<" + username +"> "

        for i in range(2, len(processed_input)):
            text += " "+processed_input[i]

        # print ("msg to send : ", text)


        start_new_thread(connect_to_peer, (messageFromServer, text,ka, "p2p"))

    elif processed_input[0]=="create":
        if len(processed_input) != 2:
            print ("invalid command ")
            continue
        
        random_num = ""
        for i in range(16):
            random_num += str(randint(0,9))

        theHash = hashlib.sha256(random_num.encode("utf-8")).hexdigest()
        thekey = theHash[0:16]
        # cipher = DES3.new(thekey, DES3.MODE_ECB)
        message += " " + thekey
        server.send(message.encode())
        messageFromServer = server.recv(1024)   
        print(messageFromServer.decode())

    elif processed_input[0]=="list":
        if len(processed_input) != 1:
            print ("invalid command ")
            continue
        server.send(message.encode())
        messageFromServer = server.recv(1024).decode()
        
        if messageFromServer[-1]==':':
            print(messageFromServer)
        else:
            messageFromServer = messageFromServer[:-1]
            groupnamesList = messageFromServer.split('\n')
            if len(groupnamesList)==0:
                print ("no groups listed")
            else:
                for name in groupnamesList:
                    print (name)

    elif processed_input[0]=="join":
        if len(processed_input) != 2:
            print ("invalid command ")
            continue
        server.send(message.encode())
        messageFromServer = server.recv(1024)
        print(messageFromServer.decode())
    else:
    	print("invalid command")

    # server.recv(1024)
    sys.stdout.flush()
server.close()
