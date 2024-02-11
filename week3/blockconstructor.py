import csv


class Mempool:
    def __init__(self, txid, fee, weight, parents = None):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = parents.split(',') if parents else []


def read_mempool_csv(file):
    """
    Read Data from a CSV File and create Mempool data with txid as the key.
    """
    mempool_data = {}
    with open(file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            txid, fee, weight, parents = map(str.strip, row[0].strip('"').split(','))
            mempool_data[txid] = Mempool(
                txid,
                fee,
                weight,
                parents)
    return mempool_data


def sort_mempool_transactions(mempool_data):
 
    """
    1.Just sorting a transactions by the highest fees is not enought to maximize block reward.
    2.Considering the weight of a transaction only, might result in most transactions being heavy but not high fees.
    Sort transactions based on fee rate.(maxmizing the fees by checking the fee against the size of that transaction)
    ,so if you set a high trasaction fee for a small transaction fee then your fee rate is high, but if you send a big transaction 
    with a low fee then your fee rate is low.)
    Refrence: https://bitcoin.stackexchange.com/questions/102377/on-a-practical-level-how-exactly-is-the-amount-of-a-bitcoin-transaction-fee-det
    """
    sorted_txs = sorted(
        mempool_data.values(), key=lambda tx: tx.fee / tx.weight, 
        reverse=True)
    return sorted_txs

def create_block(mempool_data):
    """
    Create a block using already sorted transactions.
    """
    #transaction may only appear in a block if all of its parents appear earlier in the block.
    #transaction may have zero, one, or many parents in the mempool. It may also have zero, one, or many children in the mempool.
    total_block_weight= 0
    total_fees = 0
    transactions = []
    priority_transactions = sort_mempool_transactions(mempool_data)
    for tx in priority_transactions:
        #The total weight of transactions in a block must not exceed 4,000,000 weight
        if total_block_weight + tx.weight <= 40000000:
            if all(parent in transactions for parent in tx.parents):
                transactions.append(tx.txid)
                total_block_weight += tx.weight
                total_fees += tx.fee
    #transaction must not appear more than once in the block(make sure there are no duplicates)
    block_transactions = list(set(transactions))
    print('\n'.join(block_transactions))
    print("weight",total_block_weight)
    print("fees",total_fees)

def main():
    mempool = read_mempool_csv('mempool.csv')
    create_block(mempool)

if __name__ == '__main__':
    main()