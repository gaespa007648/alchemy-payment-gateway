from web3 import Web3, HTTPProvider
from eth_account import Account
from app.abi import ERC20_ABI, EBC20_ABI_TRANSFER
import os
import app.config as config

### Pre-calcuate selector
TRANSFER_SELECTOR = Web3().keccak(
    text=f"{EBC20_ABI_TRANSFER['name']}({','.join([input['type'] for input in EBC20_ABI_TRANSFER['inputs']])})"
).hex()[:8]
TRANSFER_SELECTOR = Web3.to_hex(hexstr=TRANSFER_SELECTOR)

### Disable audit hdwallet
Account.enable_unaudited_hdwallet_features()
    
def getBalanceOf(account: str):
    RPC_URL = os.environ["RPC_URL"] # Alchemy or Infura RPC URL
    SC_ADDRESS = os.environ["SC_ADDRESS"] # Smart contract address
    SC_CHECKSUM_ADDR = Web3.to_checksum_address(SC_ADDRESS)
    
    ### Connect to blockchain provider and contract
    balance, error = 0, None
    try:
        web3 = Web3(HTTPProvider(RPC_URL))
        if web3.is_connected()==True:
            contract = web3.eth.contract(address=SC_CHECKSUM_ADDR, abi=ERC20_ABI)
            
            ### Get the balance of the account
            balance = contract.functions.balanceOf(account).call()
        else:
            raise Exception("Not connected to blockchain provider")
    except Exception as e:
        error = e
    return balance, error

def getBlockchainTxInfo(transaction_hash: str):
    '''
        We only process transfer transactions
    '''
    RPC_URL = os.environ["RPC_URL"] # Alchemy or Infura RPC URL
    transfer_info, error = {}, None   
    try:
        ### Connect to blockchain provider
        web3 = Web3(HTTPProvider(RPC_URL))
        if web3.is_connected() == True:
            transaction_info = web3.eth.get_transaction(transaction_hash)
            
            ### Parse block number, we need to get timestamp of the transaction
            block_number = transaction_info['blockNumber']
            block = web3.eth.get_block(block_number)
            timestamp = block.timestamp
            
            ### Parse information, we support EOA and LightAccount transfer transactions
            input = Web3.to_hex(hexstr=transaction_info['input'].hex())
            function_selector = TRANSFER_SELECTOR[2:] # remove 0x prefix
            if function_selector in input:
                # from address is wrapped in UserOperation, not in calldata
                # TODO: FROM_ADDRESS_LOC is currently hardcoded, you should aware the future changes in UserOperation format
                from_address = input[config.FROM_ADDRESS_LOC: config.FROM_ADDRESS_LOC+config.SIZEOF_ADDRESS]
                
                # get to address and amount in calldata
                start_idx = input.find(function_selector)
                calldata  = input[start_idx: start_idx + config.SIZEOF_FUNCTION_SELECTOR + config.SIZEOF_ADDRESS + config.SIZEOF_UINT256]
                to_address   = calldata[config.SIZEOF_FUNCTION_SELECTOR: config.SIZEOF_FUNCTION_SELECTOR + config.SIZEOF_ADDRESS]
                amount       = int(calldata[config.SIZEOF_FUNCTION_SELECTOR + config.SIZEOF_ADDRESS:], 16)
                transfer_info = {
                    "from_address": f"0x{from_address}",
                    "to_address": f'0x{to_address}', ### address is 20 bytes long, which is 40 hexstr,
                    "amount": amount,
                    "timestamp": timestamp,
                }
            else:
                raise Exception("Not a transfer transaction")
        else:
            raise Exception("Not connected to blockchain provider")
    except Exception as e:
        error = e
    return transfer_info, error
    
def sendTransferTx(to_address: str, amount: int):
    RPC_URL = os.environ["RPC_URL"] # Alchemy or Infura RPC URL
    SC_ADDRESS = os.environ["SC_ADDRESS"] # Smart contract address
    MNEMONIC = os.environ['MNEMONIC']
    from_account = Account.from_mnemonic(MNEMONIC)
    from_address = from_account.address
    tx_hash, error = None, None
    try:
        web3 = Web3(HTTPProvider(RPC_URL))
        if web3.is_connected()==True:
            ### reference the deployed contract
            MSP_CHECKSUM_ADDR = Web3.to_checksum_address(SC_ADDRESS)
            contract = web3.eth.contract(address=MSP_CHECKSUM_ADDR, abi=ERC20_ABI)
            
            ### get balance of admin
            balance = contract.functions.balanceOf(from_address).call()
            if balance<amount:
                raise Exception(f"Insufficient balance for admin account, the balance is {balance}")
            
            ### build and sign transaction
            unsent_transfer_tx = contract.functions.transfer(to_address, amount).build_transaction({
                "from": from_address,
                "nonce": web3.eth.get_transaction_count(from_address)
            })
            signed_tx = web3.eth.account.sign_transaction(unsent_transfer_tx, private_key=from_account.key)
            
            ### send and wait transaction
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)
        else:
            raise Exception("Not connected to blockchain provider")
    except Exception as e:
        error = str(e)
    return f'0x{tx_hash.hex()}' if tx_hash else '0x', error