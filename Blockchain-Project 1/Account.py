import hashlib
import json
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Account:
    # Default balance is 100 if not sent during account creation
    # nonce is incremented once every transaction to ensure tx can't be replayed and can be ordered (similar to Ethereum)
    # private and public pem strings should be set inside __generate_key_pair
    def __init__(self, sender_id, balance=100):
        self._id = sender_id
        self._balance = balance
        self._nonce = 0
        self._private_pem = None
        self._public_pem = None
        self._private_key = None
        self._public_key = None
        self.__generate_key_pair()
        self._initial_balance = 100

    @property
    def id(self):
        return self._id

    @property
    def public_key(self):
        return self._public_pem

    @property
    def balance(self):
        return self._balance

    @property
    def initial_balance(self):
        return self._initial_balance

    def increase_balance(self, value):
        self._balance += value

    def decrease_balance(self, value):
        self._balance -= value

    def increase_initial_balance(self, value):
        self._initial_balance += value

    def decrease_initial_balance(self, value):
        self._initial_balance -= value

    def __generate_key_pair(self):
        # Implement key pair generation logic
        # Convert them to pem format strings and store in the class attributes already defined
        # pass
        # Generating the private/public key pair
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        # Assigning the public key from the pair
        self._public_key = self._private_key.public_key()

        # Serializing the private key data to show what the file pem data looks like
        self._private_pem = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        print(f'Private key data for {self._id} is \n{self._private_pem}\n')

        # Serializing the public key data to show what the file pem data looks like
        self._public_pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(f'Public key data for {self._id} is \n{self._public_pem}\n\n')

    def create_transaction(self, receiver_id, value, tx_metadata=''):
        nonce = self._nonce + 1
        transaction_message = {'sender': self._id, 'receiver': receiver_id, 'value': value, 'tx_metadata': tx_metadata, 'nonce': nonce}

        # Serialize transaction data with keys ordered, and then convert to bytes format
        hash_string = json.dumps(transaction_message, sort_keys=True)
        encoded_hash_string = hash_string.encode('utf-8')

        # Take sha256 hash of the serialized message, and then convert to bytes format
        message_hash = hashlib.sha256(encoded_hash_string).hexdigest()
        encoded_message_hash = message_hash.encode('utf-8')

        signature = ''

        # Implement digital signature of the hash of the message

        # Encrypting the original message using the public key
        signature = self._private_key.sign(
            encoded_message_hash,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signature = base64.b64encode(signature).decode('ascii')

        self._nonce = nonce
        return {'message': transaction_message, 'signature': signature}
        

