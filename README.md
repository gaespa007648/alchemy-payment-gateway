# Alchemy-Payment-Gateway
我們可以藉由該服務提供的RESTFUL API與區塊鏈ERC20智能合約溝通，主要提供幾個功能
1. 餘額查詢: GET /balance/{ACCOUNT_ADDRESS}
2. 查詢交易紀錄: GET /transaction/{TRANSACTION_HASH}
3. 單筆轉帳: POST /transfer

需要注意的是，查詢交易紀錄的功能僅限由Alchemy的基於ERC4337的Smart Account發起的交易。另外，轉帳功能會綁定於.env內提供的Metamask帳戶，請確保該帳戶內於欲交易的鏈上具有足夠的token支付手續費。

# 如何使用
首先需要先複製.env.sample為.env，並設置裡面的參數
1. RPC_URL: 請於Alchemy平台註冊並取得目標鏈的RPC_URL
2. SC_ADDRESS: 已部屬的智能合約位址
3. MNEMONIC: 綁定該服務的MetaMask操作帳戶的助記詞

# 查詢交易紀錄
API的功能是解析Transaction hash在鏈上的資料，回傳以下結果
1. from_address: 發起交易的來源錢包位址
2. to_address: 交易目標的錢包位址
3. amount: tokens的數量
4. timestamp: 發起交易的時間，此時間為UTC標準時間

如果您對如何查詢鏈上交易紀錄有興趣，請參考以下文件了解更多: <a href="https://chocolate-sale-552.notion.site/14b9c8e5d7af8008b1b1ce2e300f8df2?pvs=4">如何查詢鏈上交易</a>

[注意] 由於Alchemy發起的交易會將實際智能合約的calldata嵌入在ERC4337協議的資料當中，若EntryPoint較新的情況下可能會發生不相容的問題。
