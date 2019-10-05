# from blockchain import blockchain
import util

def addTransaction(transaction):
    pass

def resetBalance(blockchain):
    index = blockchain.index
    print(index)
    i = 1
    alltran = []
    while( i <= index ):
        blockInfo = blockchain.get_block_info_from_index(str(i))
        blockWithTran = blockchain.get_block_with_transcation_from_hash(blockInfo["curBlock"])
        transactionList = blockWithTran["transactions"]
        for transaction in transactionList:
            alltran.append(transaction)
            util.clearAccount(transaction)
            util.addAccountList(transaction)
        i+=1
    for transaction in alltran:
        print(transaction)
        util.changeBalance(transaction)

# resetBalance()