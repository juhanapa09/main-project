import json
from web3 import Web3, HTTPProvider



# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = 'C:\\juhana one id\\juhana one id\\node_modules\\.bin\\build\\contracts\\oneid.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x2e30cFc8337ca4dEFA33cEBB054fC3e08426a583'
syspath=r"C:\juhana one id\juhana one id\static\\"