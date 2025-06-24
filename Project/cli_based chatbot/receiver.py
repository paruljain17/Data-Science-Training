import socket 
try:
    #creating socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("socket created")
    ip_add ="192.168.97.56"
    port = 8888
    complete_add = (ip_add,port)
    s.bind(complete_add)
    while True:
        message , sender_address = s.recvfrom(1024)

        print("Raw Message",message)
        print("sender Address",sender_address)

        decoded_msg = message.decode("ascii")
        print("Message",decoded_msg)
except Exception as e:
    print("An error occured",e)