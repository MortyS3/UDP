import socket
import sys
import select
import time
what = input('Which type of data do you want receive (txt, message or file)?: ')
if what == 'message':
    timeout = 60
    host = '10.0.1.2'
    port = 7777
    addr = (host, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(addr)

    while True:
        print('Waiting for data ({0} seconds)...'.format(timeout))
        server.settimeout(timeout)
        try:
            d = server.recvfrom(1024)
        except socket.timeout:
            print('Time is out. {0} seconds have passed'.format(timeout))
            break
        received = d[0]
        addr = d[1]
        print('From: ', addr )
        print('Received data: ', received.decode('utf-8'))
    
        msg = input('Enter message to send: ')
        server.sendto(msg.encode('utf-8'), addr)
    server.close()
elif what == 'txt' :
    UDP_IP = '10.0.1.2'
    IN_PORT = 7777
    timeout = 3


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))

    while True:
        data,addr = sock.recvfrom(1024)
        if data:
            print('File name: ', data.decode('utf-8'))
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [],timeout)
            if ready[0]:
                data, addr = sock.recvfrom(1024)
                f.write(data)
            else:
                print('%s Finish!' % file_name.decode('utf-8'))
                f.close()
                break
elif what == 'file':    
    def checkArg():
   
        if len(sys.argv) != 2:
            print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 1 argument!")
            sys.exit()
        else:
            print("1 Argument exists. We can proceed further")


    def checkPort():
        if int(sys.argv[1]) <= 5000:
            print(
            "Port number invalid. Port number should be greater than 5000. Next time enter valid port.")
            sys.exit()
        else:
            print("Port number accepted!")





    def ServerGet(g):
        print("Sending Acknowledgment of command.")
        msg = "Valid Get command. Let's go ahead "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent to Client.")

        print("In Server, Get function")

        if os.path.isfile(g):
            msg = "File exists. Let's go ahead "
            msgEn = msg.encode('utf-8')
            s.sendto(msgEn, clientAddr)
            print("Message about file existence sent.")

            c = 0
            sizeS = os.stat(g)
            sizeSS = sizeS.st_size  # number of packets
            print("File size in bytes:" + str(sizeSS))
            NumS = int(sizeSS / 1024)
            NumS = NumS + 1
            tillSS = str(NumS)
            tillSSS = tillSS.encode('utf8')
            s.sendto(tillSSS, clientAddr)

            check = int(NumS)
            GetRunS = open(g, "rb")
            while check != 0:
                RunS = GetRunS.read(1024)
                s.sendto(RunS, clientAddr)
                c += 1
                check -= 1
                print("Packet number:" + str(c))
                print("Data sending in process:")
            GetRunS.close()
            print("Sent from Server - Get function")

        else:
            msg = "Error: File does not exist in Server directory."
            msgEn = msg.encode('utf-8')
            s.sendto(msgEn, clientAddr)
            print("Message Sent.")


    def ServerPut():
        print("Sending Acknowledgment of command.")
        msg = "Valid Put command. Let's go ahead "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent to Client.")

        print("In Server, Put function")
        if t2[0] == "put":

            BigSAgain = open(t2[1], "wb")
            d = 0
            print("Receiving packets will start now if file exists.")
       
            try:
                Count, countaddress = s.recvfrom(1024)  
            except ConnectionResetError:
                print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                sys.exit()
            except:
                print("Timeout or some other error")
                sys.exit()

            tillI = Count.decode('utf8')
            tillI = int(tillI)


            while tillI != 0:
                ServerData, serverAddr = s.recvfrom(1024)

                dataS = BigSAgain.write(ServerData)

                d += 1
                tillI = tillI - 1
                print("Received packet number:" + str(d))


            BigSAgain.close()
            print("New file closed. Check contents in your directory.")



    def ServerElse():
        msg = "Error: You asked for: " + \
            t2[0] + " which is not understood by the server."
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent.")


    host = ""
    checkArg()
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Error. Exiting. Please enter a valid port number.")
        sys.exit()
    except IndexError:
        print("Error. Exiting. Please enter a valid port number next time.")
        sys.exit()
    checkPort()

    #port = 7777
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Server socket initialized")
        s.bind((host, port))
        print("Successful binding. Waiting for Client now.")
        # s.setblocking(0)
        # s.settimeout(15)
    except socket.error:
        print("Failed to create socket")
        sys.exit()

    # time.sleep(1)
    while True:
        try:
            data, clientAddr = s.recvfrom(1024)
        except ConnectionResetError:
            print(
            "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        text = data.decode('utf8')
        t2 = text.split()
        #print("data print: " + t2[0] + t2[1] + t2[2])
        if t2[0] == "get":
            print("Go to get func")
            ServerGet(t2[1])
        elif t2[0] == "put":
            print("Go to put func")
            ServerPut()
        else:
            
            ServerElse()

    print("Program will end now. ")
    quit()

else:
    print('Incorrect input')
