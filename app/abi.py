EBC20_ABI_BALANCEOF = {
    "inputs": [
    {
      "internalType": "address",
      "name": "account",
      "type": "address"
    }
    ],
    "name": "balanceOf",
    "outputs": [
    {
      "internalType": "uint256",
      "name": "",
      "type": "uint256"
    }
    ],
    "stateMutability": "view",
    "type": "function"
}

EBC20_ABI_TRANSFER = {
    "inputs": [
    {
      "internalType": "address",
      "name": "to",
      "type": "address"
    },
    {
      "internalType": "uint256",
      "name": "amount",
      "type": "uint256"
    }
    ],
    "name": "transfer",
    "outputs": [
    {
      "internalType": "bool",
      "name": "",
      "type": "bool"
    }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
}

ERC20_ABI_BATCH_TRANSFER = {
  "inputs": [
    {
      "internalType": "address[]",
      "name": "accounts",
      "type": "address[]"
    },
    {
      "internalType": "uint256[]",
      "name": "amounts",
      "type": "uint256[]"
    }
  ],
  "name": "batchTransfer",
  "outputs": [
    {
      "internalType": "bool",
      "name": "",
      "type": "bool"
    }
  ],
  "stateMutability": "nonpayable",
  "type": "function"
}

ERC20_ABI = [
    EBC20_ABI_BALANCEOF,
    EBC20_ABI_TRANSFER,
    ERC20_ABI_BATCH_TRANSFER,
]