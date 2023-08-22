from web3 import Web3
from .utilities import bn_to_bytes8, hash_string, address_to_bytes32,numberToHex, hexToByteArray
from .constants import *
from .signer import Signer
from .interfaces import Order
import hashlib
import json

class OrderSigner(Signer):
    def __init__(self, network_id, orders_contract_address="", domain="IsolatedTrader", version="1.0"):
        super().__init__()
        self.network_id = network_id
        self.contract_address = orders_contract_address 
        self.domain = domain
        self.version = version 

    def get_order_flags(self, order):
        
        ''' 0th bit = ioc
            1st bit = postOnly
            2nd bit = reduceOnly
            3rd bit  = isBuy
            4th bit = orderbookOnly
            e.g. 00000000 // all flags false
            e.g. 00000001 // ioc order, sell side, can be executed by taker
            e.e. 00010001 // same as above but can only be executed by settlement operator
        '''
        flag = 0 
        if order['ioc']:
            flag+=1
        if order['postOnly']:
            flag+=2
        if order['reduceOnly']:
            flag+=4
        if order['isBuy']:
            flag+=8
        if order['orderbookOnly']:
            flag+=16
        return flag
    
    def get_domain_hash(self):
        """
            Returns domain hash
        """
        return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
            'bytes32'
        ],
        [
            hash_string(EIP712_DOMAIN_STRING),
            hash_string(self.domain),
            hash_string(self.version),
            self.network_id,
            address_to_bytes32(self.contract_address)
        ]
    ).hex()

    def get_order_hash(self, order:Order):
        """
            Returns order hash.
            Inputs:
                - order: the order to be signed
            Returns:
                - str: order hash
        """
        flags = self.get_order_flags(order)
        flags = hexToByteArray(numberToHex(flags,2))
        
        buffer=bytearray()
        orderPriceHex=hexToByteArray(numberToHex(int(order["price"])))
        orderQuantityHex=hexToByteArray(numberToHex(int(order['quantity'])))
        orderLeverageHex=hexToByteArray (numberToHex(int(order['leverage'])))
        orderSalt=hexToByteArray(numberToHex(int(order['salt'])))
        orderExpiration=hexToByteArray(numberToHex(int(order['expiration']),16))
        orderMaker=hexToByteArray(numberToHex(int(order['maker'],16),64))
        orderMarket=hexToByteArray(numberToHex(int(order['market'],16),64))
        bluefin=bytearray("Bluefin", encoding="utf-8")

        buffer=orderPriceHex+orderQuantityHex+orderLeverageHex+orderSalt+orderExpiration+orderMaker+orderMarket+flags+bluefin
        order_hash=hashlib.sha256(buffer).digest()
        return order_hash        
    def sign_order(self, order:Order, private_key):
        """
            Used to create an order signature. The method will use the provided key 
            in params(if any) to sign the order.

            Args:
                order (Order): an order containing order fields (look at Order interface)
                private_key (str): private key of the account to be used for signing
    
            Returns:
                str: generated signature
        """
        order_hash = self.get_order_hash(order)
        return self.sign_hash(order_hash, private_key, "")

    def sign_cancellation_hash(self,order_hash:list):
        """
            Used to create a cancel order signature. The method will use the provided key 
            in params(if any) to sign the cancel order.

            Args:
                order_hash(list): a list containing all orders to be cancelled
                private_key (str): private key of the account to be used for signing
            Returns:
                str: generated signature
        """
        sigDict={}
        sigDict['orderHashes']=order_hash
        encodedMessage=self.encode_message(sigDict)
        return encodedMessage        



    