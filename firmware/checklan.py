import socket
import os
import uuid 
# printing the value of unique MAC
# address using uuid and getnode() function 

target = "192.168.40.251"
timeout = 10
hexMAX =  hex(uuid.getnode())
print(hexMAX)
print(uuid.getnode())

#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def checkLAN(trgt: str, tout: int):
    try:
        s = socket.create_connection((trgt, 80), tout)
        ipaddr = s.getsockname()[0]
        global ipADDRESS
        ipADDRESS = ipaddr
        print(s)
        host = socket.gethostname()
        print ("MyIP:", ipaddr, " TargetIP:", trgt, " MyHost:", host)
    except OSError as e:
        print (e.strerror)
        print ("Connection failed: %s\n" % e.errno)
        return False
    finally:        
        s.close()
        return True

lancheck = checkLAN(target, timeout)
print("LAN IS OK: " + str(lancheck))
print(ipADDRESS)