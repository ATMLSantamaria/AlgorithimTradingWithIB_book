import sys
import threading
import time

from datetime import datetime



sys.path.append('/home/alejandro/workspace/trading/IBJts/source/pythonclient/')

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.utils import iswrapper

# print("hello")

class SimpleClient(EWrapper,EClient):

    def __init__(self,addr,port,client_id):
        EWrapper.__init__(self)
        EClient.__init__(self,self)
        
        # connect to the tws
        self.connect(addr,port,client_id)

        # Launch client thread
        clientThread = threading.Thread(target=self.run)
        clientThread.start()

    @iswrapper
    def currentTime(self, cur_time):
        t = datetime.fromtimestamp(cur_time)
        print('Current time: {}'.format(t))
        # return super().currentTime(time)

    @iswrapper
    def error(self, req_id, code, msg,advanced_order_reject_json=None):
        print('Error {}: {}'.format(code, msg))

def main():

    # Create the client and connect to TWS
    client = SimpleClient('127.0.0.1', 7497, 0)

    # Request the current time
    client.reqCurrentTime()

    # Sleep while the request is processed
    time.sleep(0.5)
    print("hello Alejan dro")
    # Disconnect from TWS
    client.disconnect()





# Esto es para que si este script se ejecutra directamente inovquemos a la funcion main
if __name__ == "__main__":
    main()
