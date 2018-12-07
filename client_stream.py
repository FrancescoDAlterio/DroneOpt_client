import socket
import random
import sys
import time
from socket import error as SocketError
import errno
import threading

SERVER_ADDRESS = '0.0.0.0'
SERVER_CNTR_PORT = 8888
SERVER_STRM_PORT = 9999


def rcv_udp_thread(udp_sock):

    finished = False

    while not finished:
        time.sleep(1)
        try:
            data, srvr = udp_sock.recvfrom(4096)
        except Exception as e:
            print "UDP: end of streaming",e
            udp_sock.close()
            break
        print "received %s from %s " %(data,srvr,)













#create UDP control socket
cl_stream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#cl_stream_sock.settimeout(1)

#send dummy UDP message to server
message = b'dummy'
cl_stream_sock.sendto(message,(SERVER_ADDRESS,SERVER_STRM_PORT))

client_udp_port= cl_stream_sock.getsockname()[1]

print "client udp port:",client_udp_port

#create TCP control socket
cl_control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cl_control_sock.connect((SERVER_ADDRESS, SERVER_CNTR_PORT))
except socket.error as sock_err_msg:
    print 'Control socket bind failed! Error code: ', sock_err_msg.args[0], "Message",sock_err_msg.args[1]
    print "Exiting..."
    sys.exit()
'''
#python3
except Exception as e:

    print("Unable to connect to server")
    print("Exception name:",type(e).__name__,",Error code:", e.args[0], ", Message: ", e.args[1])
    sys.exit(-1)
'''

#initialize the thread to receive the udp streaming before sending the UDP port

try:
    proc_thread = threading.Thread(target=rcv_udp_thread, args=(cl_stream_sock,))
    proc_thread.start()
    # signal.pause()
    # start_new_thread(clientthread, (conn,addr,))
except (KeyboardInterrupt, SystemExit):
    print
    '\n! Received keyboard interrupt, quitting threads.\n'



time.sleep(0.5)

try:
    cl_control_sock.send(str(client_udp_port).encode())

except SocketError as e:

    if e.errno != errno.EPIPE:
        print
        "ERROR: unexpected error while communicating with the server"
        print
        "Exception name:", type(e).__name__, " ", e.args
        raise  # Not error we are looking for
    print
    "ERROR:Connection closed by the server, exit"
    print
    "Exception name:", type(e).__name__, " ", e.args

    sys.exit()



while 1:


    try:
        data = cl_control_sock.recv(1024)
        print "Received data from server: ",data.decode("UTF-8")
        rand_num=(random.randint(0, 10))
        print "generated number %d" %(rand_num)

        cl_control_sock.send(str(rand_num).encode()) #FORSE DA ERRORE

        time.sleep(1)

    except SocketError as e:

        if e.errno != errno.EPIPE:
            print "ERROR: unexpected error while communicating with the server"
            print "Exception name:", type(e).__name__, " ", e.args
            raise  # Not error we are looking for
        print "ERROR:Connection closed by the server, exit"
        print "Exception name:", type(e).__name__, " ", e.args

        break

    """
    except BrokenPipeError as e:
        print("Connection closed by the server, exit")
        print("Exception name:", type(e).__name__, " ", e.args)
        break
    """


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