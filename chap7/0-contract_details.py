import sys
from threading import Thread
import time
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
            print('Symbol: {}'.format(desc.contract.symbol))

        # Choose the first symbol
        self.symbol = contractDescriptions[0].contract.symbol

    @iswrapper
    def contractDetails(self,reqIq,details):
        print('Long name: {}'.format(details.longName))
        print('Category: {}'.format(details.category))
        print('Subcategory: {}'.format(details.subcategory))
        print('Contract ID: {}'.format(details.contract.conId))
    
    @iswrapper
    def contractDetailsEnd(self,reqIq):
        print('Then End')
    
    def error(self,reqIq,code,msg,advancedOrderRejectJson=None):
        print('Error {}: {}'.format(format,msg))

    
def main():
    # Create the client and connect to TWS
    client = ContractReader('127.0.0.1', 7497, 0)
    time.sleep(0.5)

    # Request descriptions of contracts related to cheesecake
    client.reqMatchingSymbols(0, 'NVDA')
    time.sleep(3)

    # Request details for the stock
    contract = Contract()
    contract.symbol = "NVDA" #client.symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    client.reqContractDetails(1, contract)

    time.sleep(3)
    client.disconnect()

# Esto es para que si este script se ejecutra directamente inovquemos a la funcion main
if __name__ == "__main__":
    main()


    


