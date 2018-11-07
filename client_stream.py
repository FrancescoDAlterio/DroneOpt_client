import socket
import random
import sys
import time

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8888


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
'''
except Exception as e:

    print("Unable to connect to server")
    print("Exception name:",type(e).__name__,",Error code:", e.args[0], ", Message: ", e.args[1])
    sys.exit(-1)
'''

while 1:

    try:
        data = client_socket.recv(1024)
        print("Received data from server: ",data.decode("UTF-8"))
        rand_num=(random.randint(0, 10))
        print( "generated number %d" %(rand_num))

        #se non riceve nulla ci pensiamo dopo


        client_socket.send(str(rand_num).encode()) #FORSE DA ERRORE
        #client_socket.send(b'diocan')
        time.sleep(1)

    except BrokenPipeError as e:
        print("Connection closed by the server, exit")
        print("Exception name:", type(e).__name__, " ", e.args)
        break



    '''
   if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:
        print "RECIEVED:" , data
        data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        if (data <> 'Q' and data <> 'q'):
            client_socket.send(data)
        else:
            client_socket.send(data)
            client_socket.close()
            break;
   
   
   '''