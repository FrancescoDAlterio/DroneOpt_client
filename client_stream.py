import socket
import random
import sys
import time
from socket import error as SocketError
import errno
import threading
import os
import subprocess
import ClientUtilities

#global constants

SERVER_ADDRESS = '0.0.0.0'
SERVER_CNTR_PORT = 8888

CLIENT_IPERF_PORT = 5210 #actually it runs iperf server

#global variables

pipe_name = 'pipe_iperf'
keep_executing = True

transfer = -1
bandwidth=-1
jitter = -1
received_perc= -1

'''
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

'''

##### END DECLARATION PART #####


def UDPiperfthread(iperf_port):

    #in theory this thread should never terminate
    print "UDPiperfthread:  launching UDP test with iperf3 server"

    global keep_executing
    pipeout = os.open(pipe_name, os.O_WRONLY)
    process_to_open = 'stdbuf -oL iperf3 -s -V' #default port 5201


    p = subprocess.Popen(process_to_open, shell=True, stdout=pipeout)

    p.wait()
    #udp_stream_active = False

    while keep_executing:
        time.sleep(1)

    print "UDPiperfthread:  Exiting..."




def computemetricsthread():

    # in theory this thread should never terminate
    print "computemetricsthread: generating metrics..."
    pipein = open(pipe_name, 'r')
    global keep_executing

    global transfer
    global bandwidth
    global jitter
    global received_perc

    while keep_executing:


        line = pipein.readline()[:-1]

        if line == "iperf3: the client has terminated":
            print "ERROR: server not reachable anymore"
            keep_executing = False
            print "keep_executing:",keep_executing
            break


        tokenize = line.split()

        if len(tokenize)>2 and  tokenize [1] == "error":
            print line
            keep_executing = False
            print "keep_executing:", keep_executing
            break

        #real metrics
        if len(tokenize)>3 and tokenize[3] == 'sec':

            transfer = ClientUtilities.toKilo(tokenize[5],tokenize[4])
            bandwidth = ClientUtilities.toKilo(tokenize[7],tokenize[6])
            jitter = ClientUtilities.str_to_float(tokenize[8])[1]
            received_perc = 100-ClientUtilities.str_to_float(tokenize[11].translate(None, '()%'))[1]

            print "transfer:", transfer," bandwidth:", bandwidth," jitter:", jitter,"received_perc:", received_perc


    print "computemetricsthread: Finished computing metrics...Exiting"


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
#initialize the pipe between UDPiperfthread and computemetricsthread
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)



#initialize the thread to receive the udp streaming (start iperf server)
iperf_thread = threading.Thread(target = UDPiperfthread, args=(CLIENT_IPERF_PORT,))
iperf_thread.start()

metrics_thread = threading.Thread(target = computemetricsthread)
metrics_thread.start()

try:
    cl_control_sock.send('ready'.encode())

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

    keep_executing = False
    print "keep_executing:", keep_executing

    sys.exit()


while 1:


    try:
        data = cl_control_sock.recv(1024)
        print "Received data from server: ",data.decode("UTF-8")
        rand_num=(random.randint(0, 10))
        print "generated number %d" %(rand_num)

        cl_control_sock.send(str(rand_num).encode())

        time.sleep(1)

    except SocketError as e:

        if e.errno != errno.EPIPE:
            print "ERROR: unexpected error while communicating with the server"
            print "Exception name:", type(e).__name__, " ", e.args
            raise  # Not error we are looking for
        print "ERROR:Connection closed by the server, exit"
        print "Exception name:", type(e).__name__, " ", e.args

        keep_executing = False
        print "keep_executing:", keep_executing

        break

    except KeyboardInterrupt:

        print "EXECUTION STOPPED BY THE USER"
        keep_executing = False
        sys.exit()

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