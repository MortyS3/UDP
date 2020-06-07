import socket
import sys
import time

what = input('Enter wich data you want to send (txt, message or file: ')
if what == 'message':
    host = '192.168.0.2'
    port = 7777
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = input('Enter message to send: ')
    client.sendto(msg.encode('utf-8'), ('10.0.1.2', 7777))
    d = client.recvfrom(1024)
    reply = d[0]
    addr = d[1]
    print ('Server reply: ' + reply.decode('utf-8'))
    client.close()
elif what == 'txt':
    UDP_IP = '192.168.0.2'
    UDP_PORT = 7777
    buf = 1024
    file_name = str(input(" Name of the documend: "))


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(file_name.encode(), ('10.0.1.2', 7777))
    print('Sending %s' % file_name)

    f = open(file_name, 'r')
    data = f.read(buf)
    while(data):
        if(sock.sendto(data.encode(), ('10.0.1.2', 7777))):
            data = f.read(buf)
            time.sleep(0.02)
    sock.close()
    f.close()
elif what == 'file':
    def checkArg():

        if len(sys.argv) != 3:
            print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 2 arguments!")
            sys.exit()
        else:
            print("2 Arguments exist. We can proceed further")


    def checkPort():
        if int(sys.argv[2]) <= 5000:
            print(
            "Port number invalid. Port number should be greater than 5000 else it will not match with Server port. Next time enter valid port.")
            sys.exit()
        else:
            print("Port number accepted!")

    checkArg()
    try:
        socket.gethostbyname(sys.argv[1])
    except socket.error:
        print("Invalid host name. Exiting. Next time enter in proper format.")
        sys.exit()

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error. Exiting. Please enter a valid port number.")
        sys.exit()
    except IndexError:
        print("Error. Exiting. Please enter a valid port number next time.")
        sys.exit()

    checkPort()


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Client socket initialized")
        s.setblocking(0)
        s.settimeout(15)
    except socket.error:
        print("Failed to create socket")
        sys.exit()



    while True:
        command = input(
            "Please enter a command: \n1. get [file_name]\n2. put [file_name] ")


        CommClient = command.encode('utf-8')

        try:
            s.sendto(CommClient, (host, port))
        except ConnectionResetError:
            print(
            "Error. Port numbers are not matching. Exiting. Next time please enter same port numbers.")
            sys.exit()

        CL = command.split()
        print(
        "We shall proceed, but you may want to check Server command prompt for messages, if any.")
   
        if CL[0] == "get":
            print("Checking for acknowledgement")
            try:
                ClientData, clientAddr = s.recvfrom(51200)
            except ConnectionResetError:
                print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                sys.exit()
            except:
                print("Timeout or some other error")
                sys.exit()
            text = ClientData.decode('utf8')
            print(text)
            print("Inside Client Get")

            try:
                ClientData2, clientAddr2 = s.recvfrom(51200)
            except ConnectionResetError:
                print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                sys.exit()
            except:
                print("Timeout or some other error")
                sys.exit()

            text2 = ClientData2.decode('utf8')
            print(text2)

            if len(text2) < 30:
                if CL[0] == "get":
                    BigC = open("Received-" + CL[1], "wb")
                    d = 0
                    try:
                        # number of paclets
                        CountC, countaddress = s.recvfrom(1024)
                    except ConnectionResetError:
                        print(
                        "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                        sys.exit()
                    except:
                        print("Timeout or some other error")
                        sys.exit()

                    tillC = CountC.decode('utf8')
                    tillCC = int(tillC)
                    print("Receiving packets will start now if file exists.")
               
                    while tillCC != 0:
                        ClientBData, clientbAddr = s.recvfrom(1024)
                        dataS = BigC.write(ClientBData)
                        d += 1
                        print("Received packet number:" + str(d))
                        tillCC = tillCC - 1

                    BigC.close()
                    print(
                    "New Received file closed. Check contents in your directory.")

        elif CL[0] == "put":
            print("Checking for acknowledgement")
            try:
                ClientData, clientAddr = s.recvfrom(1024)
            except ConnectionResetError:
                print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                sys.exit()
            except:
                print("Timeout or some other error")
                sys.exit()

            text = ClientData.decode('utf8')
            print(text)
            print("We shall start sending data.")

            if text == "Valid Put command. Let's go ahead ":
                if os.path.isfile(CL[1]):

                    c = 0
                   

                    size = os.stat(CL[1])
                    sizeS = size.st_size 
                   
                    print("File size in bytes: " + str(sizeS))
                    Num = int(sizeS / 1024)
                    Num = Num + 1
                    print("Number of packets to be sent: " + str(Num))
                    till = str(Num)
                    tillC = till.encode('utf8')
                    s.sendto(tillC, clientAddr)
                    tillIC = int(Num)
                    GetRun = open(CL[1], "rb")

                    while tillIC != 0:

                        time.sleep(0.07)
                        Run = GetRun.read(1024)
                        
                        
                        s.sendto(Run, clientAddr)
                        c += 1
                        tillIC -= 1
                        
                        print("Packet number:" + str(c))
                        print("Data sending in process:")

                        

                    GetRun.close()

                    print("Sent from Client - Put function")
                else:
                    print("File does not exist.")
            else:
                print("Invalid.")


        else:
            try:
                ClientData, clientAddr = s.recvfrom(51200)
            except ConnectionResetError:
                print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                sys.exit()
            except:
                print("Timeout or some other error")
                sys.exit()
            text = ClientData.decode('utf8')
            print(text)

    print("Program will end now. ") 
    quit()

else:

    print('Inncorect input')

