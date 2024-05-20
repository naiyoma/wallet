# from bitcoinrpc.authproxy import AuthServiceProxy


# rpc_user = "123456"  
# rpc_password = "123456" 
# rpc_url = "http://127.0.0.1:8332"



# def user_address():
#     """
#     Get user address type.
#     """
#     while True:
#         address_type = input("Select address type (legacy, p2sh-segwit, bech32): ").lower()
#         if address_type in ["legacy", "p2sh-segwit", "bech32"]:
#             return address_type
#         else:
#             print("Invalid address type. Please choose from legacy, p2sh-segwit, or bech32.")
# wallet_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332", timeout=290)

# wallet_name = "testwallet80"
# disable_private_keys = False
# blank = False
# passphrase = ""
# avoid_reuse = True
# descriptors = True
# load_on_startup = True
# external_signer = False
# silent_payment = True

# new_wallet = wallet_connection.createwallet(
#     wallet_name,
#     disable_private_keys,
#     blank, passphrase,
#     avoid_reuse,
#     descriptors,
#     load_on_startup,external_signer,
#     silent_payment)
# import pdb; pdb.set_trace()

# wallet_address = wallet_connection.getnewaddress("GenerateAddress",user_address())
# print("-")
# print("Wallet Address: ", wallet_address)

# #Retrive wallet spendable balance
# wallet_balance = wallet_connection.getbalance()
# print("-------------------------------------------------------------------------------")
# print("Wallet Balance:",wallet_balance)
# print("-\n")

# #generate blocks
# blocks = wallet_connection.generatetoaddress(101, wallet_address)
# print("-------------------------------------------------------------------------------")
# print("Generating Blocks")
# print("-\n")

# #new balance 
# new_balance = wallet_connection.getbalance()
# print("-")
# print("New wallet Balance:",new_balance)
# print("-")

# wallet_connection.settxfee(0.00001)
# send_transaction = wallet_connection.sendtoaddress(wallet_address, 0.01, "test send")
# print("-")
# print("Transaction Id:",send_transaction)
# print("-\n")


import os
import hashlib
import ecdsa
from bech32 import bech32_encode, convertbits

# Constants
G = ecdsa.SECP256k1.generator
N = ecdsa.SECP256k1.order

def sha256(data):
    return hashlib.sha256(data).digest()

def hash_bip352_label(data):
    tag = sha256(b"BIP0352/Label")
    return sha256(tag + tag + data)

def generate_private_key():
    return os.urandom(32)

def generate_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return vk.to_string("compressed")

def tweak_public_key(public_key, tweak):
    point = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1).pubkey.point
    tweak_point = int.from_bytes(tweak, byteorder='big') * G
    new_point = point + tweak_point
    new_pubkey = ecdsa.VerifyingKey.from_public_point(new_point, curve=ecdsa.SECP256k1)
    return new_pubkey.to_string("compressed")

def generate_silent_payment_address(bscan, bscan_priv, bm, label=None):
    # Calculate Bm with optional label
    if label is not None:
        tweak = hash_bip352_label(bscan_priv.to_bytes(32, 'big') + label.to_bytes(4, 'big'))
        bm = tweak_public_key(bm, tweak)

    # Create Bech32m address
    hrp = "sp"
    version_byte = 0
    data = bytes([version_byte]) + bscan + bm
    converted = convertbits(data, 8, 5)
    return bech32_encode(hrp, converted)

def main():
    # Generate bscan (scan public key) and bscan_priv (scan private key)
    bscan_priv = int.from_bytes(generate_private_key(), byteorder='big')
    bscan = generate_public_key(bscan_priv.to_bytes(32, 'big'))

    # Generate bspend (spend public key)
    bspend_priv = int.from_bytes(generate_private_key(), byteorder='big')
    bspend = generate_public_key(bspend_priv.to_bytes(32, 'big'))

    # Generate silent payment address
    label = 1  # Optional label
    silent_payment_address = generate_silent_payment_address(bscan, bscan_priv, bspend, label)

    print("Silent Payment Address:", silent_payment_address)

if __name__ == "__main__":
    main()
