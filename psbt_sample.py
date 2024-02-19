from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = "123456"  
rpc_password = "123456" 
rpc_url = "http://127.0.0.1:8332"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332", timeout=290)


wallet_name = "t1"
new_wallet = rpc_connection.createwallet(wallet_name)

wallet_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/wallet/{wallet_name}", timeout=170)



wallet_address = wallet_connection.getnewaddress("GenerateAddress")
wallet_address_2 = wallet_connection.getnewaddress("test2")

print("Wallet Address:", wallet_address)
print("wallaet2: wallet:", wallet_address_2)
address_1 = wallet_connection.getaddressinfo(wallet_address)
address_2 = wallet_connection.getaddressinfo(wallet_address_2)
pubkey_1 = address_1['pubkey']
pubkey_2 = address_2['pubkey']
multisig = wallet_connection.createmultisig(2, [pubkey_1, pubkey_2])
multisig_address = multisig['address']

print("________Multisig__________________________")
print(multisig)
print("------------------------------------------------")
print("")
blocks = wallet_connection.generatetoaddress(131, wallet_address)
blocks_2 = wallet_connection.generatetoaddress(131, wallet_address_2)
new_balance = wallet_connection.getbalance()

print("------------------------------------------------------------------------------")
print("New wallet Balance:",new_balance)
print("------------------------------------------------------------------------------")

#get the block count blocks in your node
new_block_count = wallet_connection.getblockcount()
print("-----------------------------------------------------------------------")
print("New Block Count:", new_block_count)
print("-----------------------------------------------------------------------")

wallet_connection.settxfee(0.00001)
send_transaction = wallet_connection.sendtoaddress(multisig_address, 0.00001, "donation" "sean's outpost")
print("-----------------------------------------------------------------------------")
print("Transaction Id:",send_transaction)
print("------------------------------------------------------------------------------")
blocks_3 = wallet_connection.generatetoaddress(131, multisig_address)

raw_transaction_details = wallet_connection.getrawtransaction(send_transaction, True)
print("--------------------------------------------------------------------")
# parse_transactions(raw_transaction_details)
pprint(raw_transaction_details)
print("----------------------------------------------------------------------")
import pdb; pdb.set_trace()
psbt = wallet_connection.walletcreatefundedpsbt([
    {
        # "txid":raw_transaction_details['txid'],
        "txid":raw_transaction_details['vin'][0]["txid"],
        "vout": raw_transaction_details['vin'][0]['vout'],
        # "vout": 0
    }
], [
     {
        "data": "00010203"  
    }
])


print(psbt)
decode = wallet_connection.decodepsbt(psbt["psbt"])
print("-----------------------DecodedPSBT-----------------------")
print(decode)
print("------------------------------------------------------")

alice_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/wallet/{wallet_name}", timeout=170)
bob_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/wallet/{wallet_name}", timeout=170)

alice_signed_psbt = alice_connection.walletprocesspsbt(psbt["psbt"])
print("Alice's Signed PSBT:", alice_signed_psbt)

# Bob signs the PSBT
bob_signed_psbt = bob_connection.walletprocesspsbt(psbt["psbt"])
print("Bob's Signed PSBT:", bob_signed_psbt)

combined_psbt = wallet_connection.combinepsbt([alice_signed_psbt["psbt"], bob_signed_psbt["psbt"]])
print("Combined PSBT:", combined_psbt)

print(wallet_connection.decodepsbt(combined_psbt))