import json
import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

from Block import Block


class Blockchain:
    # Basic blockchain init
    # Includes the chain as a list of blocks in order, pending transactions, and known accounts
    # Includes the current value of the hash target. It can be changed at any point to vary the difficulty
    # Also initiates a genesis block
    def __init__(self, hash_target):
        self._chain = []
        self._pending_transactions = []
        self._chain.append(self.__create_genesis_block())
        self._hash_target = hash_target
        self._accounts = {}
        self._invalid_transactions = []

    def __str__(self):
        return f"Chain:\n{self._chain}\n\nPending Transactions: {self._pending_transactions}\n"

    @property
    def hash_target(self):
        return self._hash_target

    @hash_target.setter
    def hash_target(self, hash_target):
        self._hash_target = hash_target

    # Creating the genesis block, taking arbitrary previous block hash since there is no previous block
    # Using the famous bitcoin genesis block string here :)
    def __create_genesis_block(self):
        genesis_block = Block(0, [], 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks',
                              None, 'Genesis block using same string as bitcoin!')
        return genesis_block

    def __validate_transaction(self, transaction):
        # Serialize transaction data with keys ordered, and then convert to bytes format
        hash_string = json.dumps(transaction['message'], sort_keys=True)
        encoded_hash_string = hash_string.encode('utf-8')

        # Take sha256 hash of the serialized message, and then convert to bytes format
        message_hash = hashlib.sha256(encoded_hash_string).hexdigest()
        encoded_message_hash = message_hash.encode('utf-8')

        # Signature - Encode to bytes and then Base64 Decode to get the original signature format back 
        signature = base64.b64decode(transaction['signature'].encode('utf-8'))

        try:
            # Load the public_key object and verify the signature against the calculated hash
            sender_public_pem = self._accounts.get(transaction['message']['sender']).public_key
            sender_public_key = serialization.load_pem_public_key(sender_public_pem)
            sender_public_key.verify(
                signature,
                encoded_message_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            return False

        return True

    def __process_transactions(self, transactions):
        # Appropriately transfer value from the sender to the receiver
        # For all transactions, first check that the sender has enough balance. 
        # Return False otherwise
        for transaction in transactions:
            sender_id = self._accounts.get(transaction['sender']).id
            if self._accounts.get(transaction['sender']).balance >= transaction['value']:
                self._accounts.get(transaction['sender']).decrease_balance(transaction['value'])
                self._accounts.get(transaction['receiver']).increase_balance(transaction['value'])
                pass
            else:
                # The invalid txns are added to another list of invalid and removed from _pending_transactions later
                # This invalid transactions list can be further used to incorporate any logic
                print(f'Sender {sender_id} has insufficient balance')
                self._invalid_transactions.append(transaction)
                # Note : Removing the invalid txn from _pending_transactions list here (as in comment below), causes
                # issue in this loop that is running on _pending_transactions list, hence they will be removed in the
                # parent method after this method is over
                # self._pending_transactions.remove(transaction)
                continue
        return True

    # Creates a new block and appends to the chain
    # Also clears the pending transactions as they are part of the new block now
    def create_new_block(self):
        if self.__process_transactions(self._pending_transactions):
            # Create new block with all valid pending transactions, invalid ones are removed in _process_transactions
            for x in self._invalid_transactions:
                try:
                    self._pending_transactions.remove(x)
                except ValueError:
                    pass
            new_block = Block(len(self._chain), self._pending_transactions, self._chain[-1].block_hash,
                              self._hash_target)
            self._chain.append(new_block)
            self._pending_transactions = []
            return new_block
        else:
            return False

    # Simple transaction with just one sender, one receiver, and one value
    # Created by the account and sent to the blockchain instance
    def add_transaction(self, transaction):
        if self.__validate_transaction(transaction):
            self._pending_transactions.append(transaction['message'])
            return True
        else:
            print(f'ERROR: Transaction: {transaction} failed signature validation')
            return False

    def __validate_chain_hash_integrity(self):
        # Run through the whole blockchain and ensure that previous hash is actually the hash of the previous block
        # Return False otherwise
        for block_index  in range (1, self._chain.__len__()):
            currblock = self._chain[block_index]
            prevblock = self._chain[block_index - 1]
            if currblock.previous_block_hash == prevblock.block_hash:
                pass
            else:
                print('__validate_chain_hash_integrity failed')
                return False
        return True

    def __validate_block_hash_target(self):
        # Run through the whole blockchain and ensure that block hash meets hash target criteria, and is the actual hash of the block
        # Return False otherwise
        for block_index in range(1, self._chain.__len__()):
            hash_string = '-'.join([
                str(self._chain[block_index]._index),
                str(self._chain[block_index]._timestamp),
                str(self._chain[block_index]._previous_block_hash),
                str(self._chain[block_index]._metadata),
                str(self._chain[block_index]._hash_target),
                str(self._chain[block_index]._nonce),
                json.dumps(self._chain[block_index]._transactions, sort_keys=True)
            ])
            encoded_hash_string = hash_string.encode('utf-8')
            block_hash = hashlib.sha256(encoded_hash_string).hexdigest()
            if self._chain[block_index].block_hash > self._chain[block_index].hash_target or self._chain[block_index].block_hash != block_hash:
                print('__validate_chain_hash_integrity failed')
                return False
            else:
                pass
        return True

    def __validate_complete_account_balances(self):
        # Run through the whole blockchain and ensure that balances never become negative from any transaction
        # Return False otherwise
        for block_index in range(1, self._chain.__len__()):
            for transaction in self._chain[block_index]._transactions:
                self._accounts.get(transaction['sender']).decrease_initial_balance(transaction['value'])
                self._accounts.get(transaction['receiver']).increase_initial_balance(transaction['value'])
                if self._accounts.get(transaction['sender'])._initial_balance < 0:
                    return False
        return True

    # Blockchain validation function
    # Runs through the whole blockchain and applies appropriate validations
    def validate_blockchain(self):
        # Call __validate_chain_hash_integrity and implement that method. Return False if check fails
        # Call __validate_block_hash_target and implement that method. Return False if check fails
        # Call __validate_complete_account_balances and implement that method. Return False if check fails
        self.__validate_chain_hash_integrity()
        self.__validate_block_hash_target()
        self.__validate_complete_account_balances()
        return True

    def add_account(self, account):
        self._accounts[account.id] = account

    def get_account_balances(self):
        return [{'id': account.id, 'balance': account.balance} for account in self._accounts.values()]

    def get_initial_account_balances(self):
        return [{'id': account.id, 'initial balance': account._initial_balance} for account in self._accounts.values()]


