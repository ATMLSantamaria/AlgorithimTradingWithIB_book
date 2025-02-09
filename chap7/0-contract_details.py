import sys
from threading import Thread

# Necessary to include the ibapi module
sys.path.append('/home/alejandro/workspace/trading/IBJts/source/pythonclient/')

from ibapi.client import Contract
from ibapi.client import EClient, Contract
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper



# Class that inherit from EWrapper and EClient
class ContractReader(EWrapper, EClient):
    ''' Serves as the client and the wrapper '''

    def __init__(self, addr, port,client_id):
        EWrapper.__init__(self)
        EClient.__init__(self,self)

        # Connect to the TWS
        self.connect(addr,port,client_id)

        # Launch the client Thread
        thread = Thread(target=self.run)
        thread.start()

    # iswrapper is a decorator of the ibapi. Normally decorator provide extra functionalities to the methdo of the parent, But in this case
    # it just shows that the parent method is overriden 
    @iswrapper
    def symbolSamples(self, reqId, contractDescriptions):
        
        # Print the symbols in the returned results
        print('Number of descriptions: {}'.format(len(contractDescriptions)))
        for desc in contractDescriptions:
            print('Symbol: {}'.format(contractDescriptions.contract.symbol))

        # Choose the first symbol
        self.symbol = contractDescriptions[0].contract.symbol

    @iswrapper
    def contract

    


