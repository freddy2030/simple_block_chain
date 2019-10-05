from blockchain import blockchain
from time import time

# index = blockchain.index + 1
# gindex = blockchain.globalchainindex + 1
# timestamp = time()
# current_transactions = blockchain.get_transactions_pool()

# last_block = blockchain.last_block
# previous_hash = blockchain.hash( last_block )

# last_g_block = blockchain.last_gblock
# # previous_g_hash = blockchain.hash( last_g_block )
# previous_g_hash = "4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11"

# block_tmp = blockchain.new_candidate_block(index,
#                                             timestamp,
#                                             current_transactions,
#                                             previous_hash, gIndex = gindex, previous_g_hash = previous_g_hash)

block = {'id': '79d2421c82c88bc3b786a70a03209d939b9853e4cec0078bd4cd226fe4ad3a79', 'index': 1, 'gindex': 1, 'timestamp': 1570233978.7453845, 'transactions': '0093438dba9ea74069b9be63c40155d996c4655c87dc623cf0f41d92fe1a7467', 'proof': 258, 'previous_hash': '4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11', 'previous_g_hash': '4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11'}

blockchain.submit_block(block)