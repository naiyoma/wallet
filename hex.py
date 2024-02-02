
from bitcoinlib.transactions import Transaction

def parse_transactions(hex):
    # import pdb; pdb.set_trace() 
    transaction_object = Transaction.parse_hex(hex)
    txid = transaction_object.txid
    confirmations = transaction_object.confirmations
    inputs = transaction_object.inputs
    outputs = transaction_object.outputs
    version = transaction_object.version
    locktime = transaction_object.locktime


