# Importing Standard Libraries
import ifcfg # pip install ifcfg
import time
from socket import *
import threading
import sys

# create network scanner class to store public/private functions and fields
class NetworkScanner:
    def __init__(self, inputPortRange):
        self.__hostName = gethostname()
        self.__ip = gethostbyname(self.__hostName)
        self.__portRange = inputPortRange
        self.__printZone = "-------------------------------------"

    def search_ports(self):
        startTime = time.time()

        sys.stdout.write("Starting port search \n")

        for i in range(self.__portRange[0], self.__portRange[1]):
            
            s = socket(AF_INET, SOCK_STREAM)
            
            conn = s.connect_ex((self.__ip, i))

            if(conn == 0):
                sys.stdout.write("Port {} is available \n".format(i))

            s.close()

        sys.stdout.write("Completed: {} \n".format(str(time.time()-startTime)))

    def search_network(self):

        sys.stdout.write("Starting Network Search \n")

        for outerKey in ifcfg.interfaces().keys():
            # print(key, values)
            # print("\n")
            sys.stdout.write(self.__printZone + "\n")
            sys.stdout.write(outerKey + "\n")
            for key, values in ifcfg.interfaces()[outerKey].items():
                sys.stdout.write(key + ": ")
                try:
                    for value in values:
                        sys.stdout.write(value)
                except TypeError: # key has no value
                    sys.stdout.write("None")
                sys.stdout.write("\n")
            sys.stdout.write(self.__printZone + "\n")


if __name__ == "__main__":
    netscan = NetworkScanner(inputPortRange=(0, 50))
    # in the background, scan all available ports on machine within range listed
    scanthread = threading.Thread(target=netscan.search_ports, daemon=True)
    scanthread.start()
    
    netscan.search_network()
    
    
    for line in sys.stdin:
        print(line, end="")

    scanthread.join()








