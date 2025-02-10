#We have a Contract and an Order

# We just need the method placeOrder from the client

from threading import Thread
import sys
import time

sys.path.append('/home/alejandro/workspace/trading/IBJts/source/pythonclient/')


from ibapi.client import EClient, Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper

#  Creamos la clase submitOrder para encapsular este comportamiento
class SubmitOrder(EWrapper,EClient):
    ''' Serves as the client and the wrapper '''
    def __init__(self,addr,port,clientId):
        EWrapper.__init__(self)
        EClient.__init__(self,self)
        self.orderId=None

        # Connect to TWS
        self.connect(addr,port,clientId)

        # Launch the client thread
        thread=Thread(target=self.run)
        thread.start()

    @iswrapper
    def nextValidId(self,order_id):
        ''' Provides the next order ID '''
        self.order_id=order_id
        print('Order ID: '.format(order_id))

    @iswrapper
    def orderStatus(self,order_id, status, filled, remaining,
        avgFillPrice, permId, parentId, lastFillPrice, clientId,
        whyHeld, mktCapPrice):
        ''' Check the status of the submitted order '''
        print('Number of filled positions: {}'.format(filled))
        print('Average fill price: {}'.format(avgFillPrice))

    @iswrapper
    def position(self,account, contract, pos, avgCost):
        ''' Read information about open positions '''
        print('Position in {}: {}'.format(contract.symbol, pos))

    @iswrapper
    def accountSummary(self, req_id, account, tag, value,currency):
        ''' Read information about the account '''
        print('Account {}: {} = {}'.format(account, tag, value))

    def error(self, req_id, code, msg,advancedOrderRejectJson=None):
        print('Error {}: {}'.format(code, msg))


def main():
    # Create client and connect it to TWS
    client=SubmitOrder('127.0.0.1',7497,0)

    # Define a contract for Nvidia Stock
    contract=Contract()
    contract.symbol='NVDA'
    contract.secType='STK'
    contract.exchange='SMART'
    contract.currency='USD'

    # Define de Order
    order=Order()
    order.action='BUY'
    order.totalQuantity=200
    order.orderType='LMT'
    order.lmtPrice=134
    order.transmit=False

    # Obtain a valid ID for the order
    # client.req_ids(1)
    client.reqIds(1)
    time.sleep(2)
    
    # Place the order
    if client.order_id:
        client.placeOrder(client.order_id, contract, order)
        time.sleep(3)
    else:
        print('Order ID not received. Ending application.')
        sys.exit()

    # Obtain information about open positions
    client.reqPositions()
    
    time.sleep(2)

        # Obtain information about account
    client.reqAccountSummary(0, 'All','AccountType,AvailableFunds')
    time.sleep(2)

    # Disconnect from TWS
    client.disconnect()

if __name__ == '__main__':
    main()



            
    