import socket 
import select 
import sys 
import random
from _thread import *

client_user_name={}
clients_login={}
client_ports_as_server={}
clients_client_port_username = {}
groupnameList = []
group_members = {}
gruopname_key = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# if len(sys.argv) != 3: 
# 	print ("Correct usage: script, IP address, port number") 
# 	exit() 


IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
server.listen(100) 
list_of_clients = [] 


def clientthread(conn, addr): 

	print("connection from ",addr[1]) #clients port
	clients_port_as_client = addr[1]
	message = conn.recv(2048)
	message=message.decode()
	print("details of client",message)
	portdetails=message.split('-')
	client_server_port=portdetails[1]


	while True: 

		if clients_port_as_client in clients_client_port_username:
			clients_username = clients_client_port_username[clients_port_as_client]
		else:
			clients_username = ""

		message = conn.recv(2048).decode()
		# print ("message from client : ", message)
		processed_input=message.split()

		if(processed_input[0]=='signup'):
			username = processed_input[1]
			pwd = processed_input[2]
			if(username in client_user_name):
				msgtToClient = "user name already in use"
			else:
				client_user_name[username]=pwd
				clients_login[username]=0
				client_ports_as_server[username]=client_server_port
				clients_client_port_username[clients_port_as_client]=username
				msgtToClient = username + " added"
			
			conn.send(msgtToClient.encode())

		elif(processed_input[0]=="signin"):
			username = processed_input[1]
			pwd = processed_input[2]
            
			if(username not in client_user_name):
				msgtToClient = username + " not signed up"
			else:
				if clients_login[username] == 1:
					msgtToClient = username + " already signed in"
				elif client_user_name[username] != pwd:
					msgtToClient = " pwd does not match"
				else:
					clients_login[username] = 1
					msgtToClient = username + " logged in"
			conn.send(msgtToClient.encode())


		elif(processed_input[0]=='send' and processed_input[1]=="group"):
			print("SEND group COMMAND RECIEVED")
			groupname=processed_input[2]
			if clients_username=="":
				msgtToClient = "error first signup to start chatting"
			elif clients_login[clients_username] != 1:
					msgtToClient = "error first login to start chatting"
			elif groupname not in groupnameList:
				msgtToClient = "error group by the name : " + groupname + " does not exist"
			else:
				members = group_members[groupname]
				msgtToClient=gruopname_key[groupname]
				for member in members:
					if(member != clients_username):
							msgtToClient += " "+str(client_ports_as_server[member])

			print ("msg to client : ", msgtToClient)
			conn.send(msgtToClient.encode())


		elif(processed_input[0]=='send'):
			print("SEND COMMAND RECIEVED")
			if clients_username=="":
				msgtToClient = "error first signup to start chatting"
			elif clients_login[clients_username] != 1:
				msgtToClient = "error first login to start chatting"
			reciever_user_name=processed_input[1]
			if reciever_user_name not in client_user_name:
				msgtToClient = "error "+reciever_user_name + " does not exist"
			else:
				msgtToClient=client_ports_as_server[reciever_user_name]
			conn.send(msgtToClient.encode())


		elif(processed_input[0]=="list"):
			if clients_username=="":
				msgtToClient = "first signup to create group:"
			elif clients_login[clients_username] != 1:
				msgtToClient = "first login to create group:"
			else:
				msgtToClient = ""
				for groupname in groupnameList:
					msgtToClient += (groupname + "\n")

			conn.send(msgtToClient.encode())


		elif(processed_input[0]=="join"):
			groupname = processed_input[1]
			if clients_username=="":
				msgtToClient = "first signup to create group"
			elif clients_login[clients_username] != 1:
				msgtToClient = "first login to create group"
			elif groupname not in groupnameList:
				msgtToClient = "group by the name : " + groupname + " does not exist"
			else:
				members = group_members[groupname]

				if clients_username in members:
					msgtToClient = " you are already part of this group"
				else:
					group_members[groupname].append(clients_username)
					msgtToClient = "group joined"

			conn.send(msgtToClient.encode())

		elif(processed_input[0]=="create"):
			groupname = processed_input[1]
			groupkey = processed_input[2]
			print ("username : ", clients_client_port_username[clients_port_as_client])
			if clients_username=="":
				msgtToClient = "first signup to create group"
			elif clients_login[clients_username] != 1:
				msgtToClient = "first login to create group"
			elif groupname in groupnameList:
				msgtToClient = "group by the name : " + groupname + " already exist"
			else:
				groupnameList.append(groupname)
				group_members[groupname] = [clients_username]
				gruopname_key[groupname] = groupkey
				msgtToClient = "group created"

			conn.send(msgtToClient.encode())

		elif processed_input[0]=="key":

			grpname = processed_input[1]

			key = gruopname_key[grpname]
			print ("grp key required : ", key)
			conn.send(key.encode())


		
		# conn.send("Welcome to this chatroom!".encode()) 
		sys.stdout.flush() 
		

					# Calls broadcast function to send message to all 
				# message_to_send = "<" + addr[0] + "> " + message 
				# # broadcast(message_to_send, conn) 

				# # else: 
				# 	"""message may have no content if the connection 
				# 	is broken, in this case we remove the connection"""
				# 	# remove(conn) 

			# except: 
			# 	continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

while True: 
	conn, addr = server.accept() 
			
	list_of_clients.append(addr[1]) 
			
	print (addr[0] + " connected") 

	start_new_thread(clientthread,(conn,addr)) 

# conn.close() 
server.close() 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 
