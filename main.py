from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBearer
from fastapi.responses import JSONResponse
from app.chain import getBalanceOf, getBlockchainTxInfo, sendTransferTx
from app.body import Transfer

### App related variables
app = FastAPI()
origins = ["*"]
methods = ["*"]
headers = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers
)

basic_scheme = HTTPBasic(auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

### API Design
@app.get('/')
async def health_checking():
  '''
  Health checking API.
  '''
  return {"message": "Health check for mesh-payment-chain"}

@app.get('/balance/{address}')
async def get_balance(address: str):
  '''
    Get balance of an address
  '''
  balance, error = getBalanceOf(address)
  if error:
    return JSONResponse(
      status_code = status.HTTP_404_NOT_FOUND,
      content = {"message": str(error)}
    )
  return JSONResponse(
    status_code = status.HTTP_200_OK,
    content = { "balance": balance }
  )

@app.get('/transaction/{transaction_hash}')
async def get_transaction(transaction_hash: str):
  '''
    Get ERC-20 transfer transaction information
  '''
  transaction_info, error = getBlockchainTxInfo(transaction_hash)
  if error:
    return JSONResponse(
      status_code = status.HTTP_404_NOT_FOUND,
      content = {"message": str(error)}
    )
  return JSONResponse(
    status_code = status.HTTP_200_OK,
    content = { "transaction": transaction_info }
  )
  
@app.post('/transfer')
async def transfer_coin(
  transfer: Transfer):
  '''
    Transfer amount of ERC20 tokens to the target address.
  '''
  ### send transfer
  txHash, error = sendTransferTx(transfer.address, transfer.amount)
  if error:
    return JSONResponse(
      status_code = status.HTTP_404_NOT_FOUND,
      content = {"message": str(error)}
    )
  
  return JSONResponse(
    status_code = status.HTTP_200_OK,
    content = { "transaction": txHash }
  )