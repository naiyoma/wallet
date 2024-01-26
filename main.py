
import logging
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def user_address():
    """
    Get user address type.
    """
    while True:
        address_type = input("Select address type (legacy, p2sh-segwit, bech32): ").lower()
        if address_type in ["legacy", "p2sh-segwit", "bech32"]:
            return address_type
        else:
            print("Invalid address type. Please choose from legacy, p2sh-segwit, or bech32.")

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = "123456"  
rpc_password = "123456" 


rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332", timeout=290)
#retrieve the blockcount of your node
block_count = rpc_connection.getblockcount()
print("-------------------------------------------------------------------------")
print("Block Count: ", block_count)
print("-------------------------------------------------------------------------")


# Create a wallet named "testwallet15"
wallet_name = "testwallet80"
new_wallet = rpc_connection.createwallet(wallet_name)

# Specify the wallet file in the URI path for subsequent RPC calls
wallet_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/wallet/{wallet_name}", timeout=170)

# Retrieve a new address from the newly created wallet
wallet_address = wallet_connection.getnewaddress("GenerateAddress", user_address())
wallet_info = wallet_connection.getwalletinfo()
print("-------------------------------------------------------------------------")
print("Wallet Address: ", wallet_address)
print("-------------------------------------------------------------------------")
print("---------------------------------------------------------------")
print("Wallet Info:")
print("-----------")
pprint(wallet_info)
print("---------------------------------------------------------------\n")

#Retrive wallet spendable balance
wallet_balance = wallet_connection.getbalance()

print("-------------------------------------------------------------------------------")
print("Wallet Balance:",wallet_balance)
print("-------------------------------------------------------------------------------")

#generate blocks

blocks = wallet_connection.generatetoaddress(101, wallet_address)
print("-------------------------------------------------------------------------------")
print("Blocks:",blocks)
print("-------------------------------------------------------------------------------")

#new balance 
new_balance = wallet_connection.getbalance()

print("-------------------------------------------------------------------------------")
print("New wallet Balance:",new_balance)
print("-------------------------------------------------------------------------------")

#get the block count blocks in your node
new_block_count = wallet_connection.getblockcount()
print("---------------------------------------------------------------")
print("New Block Count:", new_block_count)
print("---------------------------------------------------------------\n")

#Lets a create raw transaction


# raw_transaction=wallet_connection.createrawtransaction()
# import pdb; pdb.set_trace()
# transaction_id = wallet_connection.sendtoaddress(wallet_address, 0.00000001)
# transaction_id = wallet_connection.sendtoaddress(wallet_address, 0.1, "", "", True, True, 0.00001)

# print("---------------------------------------------------------------")
# print("Transaction_ID:", transaction_id)
# print("---------------------------------------------------------------\n")


# # private_key_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/dumpprivkey/{wallet_address}")
# #Retrieve Pubkey for a wallet
# # private_key = wallet_connection.dumpprivkey(wallet_address)
# # print(f"Wallet Privatekey: {private_key}")

# # Retrieve the best block hash
# best_block_hash = wallet_connection.getbestblockhash()
# print(f"Best Block Hash: {best_block_hash}")
