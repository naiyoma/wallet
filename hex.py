
from bitcoinlib.transactions import Transaction
from pprint import pprint



def parse_transactions(hex):
    """
    Parse a transactions.
    """
    transaction = Transaction.parse_hex(hex)
    inputs = [
        {
            "txid": input.prev_txid.hex(),
            "vout": input.output_n_int,
            "signatures": [signature.hex() for signature in input.signatures],
            "witness_type": input.witness_type,
            "witness": [witness.hex() for witness in input.witnesses]
        }
        for input in  transaction.inputs
    ]
    outputs = [
        {
            "address": output.address,
            "value":output.value,
            "output_n":output.output_n,
            "hex":output.script.serialize().hex()
        }
        for output in transaction.outputs
    ]
    pprint(
        {
        "txid": transaction.txid,
        "confirmations": transaction.confirmations,
        "version": transaction.version.hex(),
        "input": inputs,
        "outputs": outputs,
        "locktime": transaction.locktime
        }
    )
    
parse_transactions("020000000001010ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e3f4a901e314e1b827c3332d7e1865ffe1d7ff5f5d7576a9000f354487a09de44cd00000000")
