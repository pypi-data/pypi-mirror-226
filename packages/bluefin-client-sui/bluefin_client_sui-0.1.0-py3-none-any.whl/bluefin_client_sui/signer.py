from web3 import Web3
import eth_account
import nacl
import hashlib
import json
class Signer:
    def __init__(self):
        pass
        

    def get_eip712_hash(self, domain_hash, struct_hash):
        """
            Returns the EIP712 hash.
            Inputs:
                - domain_hash: chain domain hash
                - struct_hash: struct hash of information to be signed
        """
        return Web3.solidityKeccak(
        [
            'bytes2',
            'bytes32',
            'bytes32'
        ],
        [
            '0x1901',
            domain_hash,
            struct_hash
        ]
    ).hex()


    def sign_hash(self, hash, private_key, append=''):
        """
            Signs the hash and returns the signature. 
        """
        result= nacl.signing.SigningKey(private_key).sign(hash)[:64]
        return result.hex()+'1' + append
    

    def encode_message(self,msg: dict):
        msg=json.dumps(msg,separators=(',', ':'))
        msg_bytearray=bytearray(msg.encode("utf-8"))
        intent=bytearray()
        intent.extend([3,0,0, len(msg_bytearray)])
        intent=intent+msg_bytearray
        hash=hashlib.blake2b(intent,digest_size=32)
        return hash.digest()
