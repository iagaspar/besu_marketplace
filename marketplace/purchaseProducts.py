from web3 import Web3
from eth_utils import to_checksum_address

# Conectar ao nó Besu
w3 = Web3(Web3.HTTPProvider('http://10.20.30.7:8545'))

# Endereço e chave privada do comprador
buyer_address = to_checksum_address('0xf60ae6888ea28296c396cbbe66bce5eda6d52e55')
buyer_private_key = '0xff217c41ce24b70ff300d6a570d548408d24f9d3a762acd5d53786c15460ba6e'

# Endereço do contrato implantado
contract_address = '0x3E4AF42359eC199970E5264Fa73e0295b2d942F6'

# Criar instância do contrato
checksum_address = to_checksum_address(contract_address)
contract_abi = [
    {
        "constant": True,
        "inputs": [{"name": "", "type": "uint256"}],
        "name": "products",
        "outputs": [
            {"name": "id", "type": "uint256"},
            {"name": "name", "type": "string"},
            {"name": "price", "type": "uint256"},
            {"name": "owner", "type": "address payable"},
            {"name": "purchased", "type": "bool"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "_id", "type": "uint256"}],
        "name": "purchaseProduct",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "id", "type": "uint256"},
            {"indexed": False, "name": "name", "type": "string"},
            {"indexed": False, "name": "price", "type": "uint256"},
            {"indexed": False, "name": "owner", "type": "address payable"},
            {"indexed": False, "name": "purchased", "type": "bool"}
        ],
        "name": "ProductPurchased",
        "type": "event"
    }
]
contract = w3.eth.contract(address=checksum_address, abi=contract_abi)

# ID do produto a ser comprado (assumindo que é o primeiro produto disponível)
product_id_to_purchase = 1

# Chamar a função purchaseProduct do contrato
transaction_data = contract.functions.purchaseProduct(product_id_to_purchase).build_transaction({
    'from': buyer_address,
    'gas': 2000000,
    'gasPrice': Web3.to_wei('1', 'gwei'),
    'nonce': w3.eth.get_transaction_count(buyer_address),
    'value': 0  # Não enviamos Ether diretamente, pois a função purchaseProduct é payable
})

# Assinar e enviar a transação
signed_transaction = w3.eth.account.sign_transaction(transaction_data, buyer_private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Esperar pela confirmação da transação
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Extrair os logs de eventos
event_logs = contract.events.ProductPurchased().process_receipt(transaction_receipt)
for log in event_logs:
    print("Produto comprado:", log['args'])

print(f'Transação enviada. Hash: {transaction_hash.hex()}')
