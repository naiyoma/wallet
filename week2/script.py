import os
import hashlib
import random
from pprint import pprint
from bitcoinlib.config.opcodes import op
from bitcoinlib.scripts import *
from bitcoinlib.keys import *
from bitcoinlib.transactions import *
from bitcoinlib.wallets import *
from bitcoinlib.services.bitcoind import BitcoindClient
from bitcoinrpc.authproxy import AuthServiceProxy




def create_redeem_script():
    # Get Pre-image as a byte string
    # Calculate SHA-256 hash of the pre-image
    # import pdb; pdb.set_trace()
    # Construct the redeem script
    # Print the redeem script
    pre_image = bytes.fromhex("427472757374204275696c64657273")
    lock_hex = hashlib.sha256(pre_image).hexdigest()
    redeem_script = Script([op.op_sha256, bytes.fromhex(lock_hex), op.op_equal])

    print("Redeem Script Hex:", redeem_script.serialize().hex())
    return redeem_script


def generate_new_address(redeem_script):
    # Using the redeem script above generate an adress
    addr = Address(redeem_script.serialize().hex(), script_type='p2sh')
    print("P2SH Address:", addr.address)
    return addr.address

def create_send_transaction(addr):
    #Create a transaction that sends an amount to the address above
    # Create a PrivateKey 
    #First Initate a Transaction Object
    #get a an unspend transaction id to be used as previous output and current input
    #create an input using the previous transaction id and the created private key
    #create an output for the transaction and include the value to be used by the adress created above
    #sign the transaction 
    #verify the transaction
    #check the raw hex
    #write unit tests to validate this transaction

 
    private_key_bytes = os.urandom(32)
    private_key = Key(private_key_bytes.hex())
    print("Private Key:", private_key.private_hex)
    t = Transaction()
    prev_tx = 'f2b3eb2deb76566e7324307cd47c35eeb88413f971d88519859b1834307ecfec'
    t.add_input(prev_txid=prev_tx, output_n=1, keys=private_key.public_hex, compressed=False)
    t.add_output(10, addr)
    t.sign(private_key.private_hex)
    print("----------Send Transaction Info-------------------------------------------------------------")
    pprint(t.as_dict())
    print("Raw:", t.raw_hex())
    print("-----------------------------------------------------------------------------------------")
    print("Verified %s " % t.verify())
    print(t.raw_hex())
    print("-----------------------------------------------------------------------")
    return t, private_key


 
def spend_transaction(t, private_key):
    #create a transaction that spends from the above transaction 
    #give that you have both locking and unlocking scripts 
    #while creating two outputs (main and change outputs), avoid address reuse
    # spend_tx = Transaction()
    # create a wallet and generate a new address to be used up as change
    # calculate the change address 
    #calculate the change output amount
    #create a new transaction to spend the previous outputs
    #sign this with the same private key

    for i, tx_input in enumerate(t.inputs):
        ulocking_script = tx_input.unlocking_script.hex()
        print(f"Input {i + 1} - Locking Script: {tx_input.unlocking_script.hex()}")

    utxo_info = t.outputs[0]
    utxo_value = utxo_info.value
    wallet_name = ''.join([random.choice(['w', 'a', 'l', 'l', 'e']) for i in range(5)])
    wallet = Wallet.create(wallet_name)
    change_address = wallet.new_key().address
    amount = 5 
    change_output_amount = utxo_value - amount

    new_tx = Transaction()
    new_tx.add_input(prev_txid=t.txid, output_n=0, unlocking_script=redeem_script.serialize())  
    new_tx.add_output(amount, addr)  
    new_tx.add_output(change_output_amount, change_address)

    new_tx.sign(private_key)
    print("-----------Spend Transaction----------------------------------------------------------------------------")
    pprint(new_tx.as_dict())
    print("Raw:", new_tx.raw_hex())
    print("----------------------------------------------------------------------------")
    print("Verified %s " % new_tx.verify())



redeem_script = create_redeem_script()
addr = generate_new_address(redeem_script)
t, private_key = create_send_transaction(addr)
spend_transaction(t, private_key)
