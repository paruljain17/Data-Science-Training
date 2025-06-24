import socket 
try:
    #creating socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("socket created")
    ip_add ="192.168.97.56"
    port = 8888
    target_add = (ip_add,port)
    message = input("Enter the message : 😂")
    encoded_msg = message.encode("ascii")
    s.sendto(encoded_msg,target_add)
    print("message sent successfully")
    s.close()
except Exception as e:
    print("An error occured",e)
