from pprint import pprint

class Transaction:
    def __init__(self, version, inputs, outputs, locktime):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = script_sig
        self.sequence = sequence

class TxOut:
    def __init__(self, value, script_pubkey):
        self.value = value
        self.script_pubkey = script_pubkey

def decode_transaction(hex_string):
    # Perform hex decoding
    raw_bytes = bytes.fromhex(hex_string)
    # Parse transaction fields
    version = raw_bytes[0:4]
    num_inputs = int.from_bytes(raw_bytes[6:7], byteorder='little')  # Corrected indexing and conversion to integer
    inputs = []

    # Parse inputs
    offset = 7
    for _ in range(num_inputs):
        prev_tx = raw_bytes[offset:offset+32]
        prev_index = raw_bytes[offset+32:offset+36]
        script_sig_length = raw_bytes[offset+36]
        script_sig = raw_bytes[offset+37:offset+37+script_sig_length]
        sequence = raw_bytes[offset+37+script_sig_length:offset+37+script_sig_length+4]
        inputs.append(TxIn(prev_tx, prev_index, script_sig, sequence))
        offset += 37 + script_sig_length + 4

    num_outputs = raw_bytes[offset]
    outputs = []
    offset += 1
    for _ in range(num_outputs):
        value = int.from_bytes(raw_bytes[offset:offset+8], byteorder='little')
        script_pubkey_length = raw_bytes[offset+8]
        script_pubkey = raw_bytes[offset+9:offset+9+script_pubkey_length]
        outputs.append(TxOut(value, script_pubkey))
        offset += 9 + script_pubkey_length
    # # import pdb; pdb.set_trace()
    # print("Output Count:\n")
    # print("Hex:", format(num_outputs, '02x'))
    # for i, (value, script_pubkey) in enumerate(outputs, start=1):
    #     print(f"\nOutput {i}:\n")
    #     print(f"Value: {value:016x} (In Satoshis, so {value} Satoshis)")
    #     print(f"Script Length: {format(script_pubkey_length, '02x')}")
    #     print("Script Pubkey:", script_pubkey.hex())

    
    transaction = Transaction(version, inputs, outputs,1)
    
    return transaction

def deserialize_transaction(transaction):
   
    deserialized_inputs = []
    deserialized_outputs = []

    for input in transaction.inputs:
        prev_tx_hex = input.prev_tx.hex()
        # Convert the hex string to bytes
        bytes_data = bytes.fromhex(prev_tx_hex)
        # Reverse the bytes
        reversed_bytes = bytes_data[::-1]
        # Convert the reversed bytes back to hex string
        reversed_hex = reversed_bytes.hex()
        vout_int = int.from_bytes(input.prev_index, byteorder='little')

        deserialized_input = {
            "prev_tx": reversed_hex,
            "vout": vout_int,
            "scriptSig": {
                "hex": input.script_sig.hex()
            },
            "sequence": int(input.sequence[::-1].hex(), 16)
        }
        deserialized_inputs.append(deserialized_input)
    # Deserialize outputs
    for output in transaction.outputs:
        # import pdb; pdb.set_trace()
        value = output.value 
        script_pubkey = output.script_pubkey.hex()  
        deserialized_output = {
            "value": value,
            "scriptPubKey": {
                "hex": script_pubkey
            }
        }
        deserialized_outputs.append(deserialized_output)
        
    deserialized_transaction = {
        "version": int.from_bytes(transaction.version, byteorder='little'),
        "inputs": deserialized_inputs,
        "outputs": deserialized_outputs
    }

    return deserialized_transaction

# Example usage
hex_transaction = "02000000000101c2b36b67a8e447765649e771bcb0450cfd06893025d80bac7a13ec3af7c4c77c0100000017160014fdde9936089bd0b1326fa954d0cdd8c831287cc4fdffffff020000000000000000066a04000102037fab402500000000225120f7ecd79ad135565bf182356a5aaa0b5fa814e9bfc32a931cb65825237f4eb87202473044022031db589b23dea0cf97287745f4cb697314de5a13cc6768dcfab7da4828dee52d022053571793abb91ba5d8c88a90d142854ce15eab5b6d980ed53f4884e62b86beef012102dfbd6e82b24409bb7bb94576bdfdf2ef22cc6f781efc337add8d2b05becca71b00000000"
transaction = decode_transaction(hex_transaction)
deserialized_transaction = deserialize_transaction(transaction)
pprint(deserialized_transaction)
