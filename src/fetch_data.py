import requests
import json
import time
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from web3 import Web3
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Configuration
ALCHEMY_API_KEY = '_iokA7k2k-6itqNiNkP9y'
ETHERSCAN_API_KEY = '83D9EYKQIBRNH8QESVHA3EGM1KKP94NQME'

# Directory setup
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
WALLETS_CSV = DATA_DIR / 'wallets.csv'
RAW_DATA_JSON = DATA_DIR / 'raw_data.json'

# Expanded Compound contract list (all cTokens and core contracts)
COMPOUND_CONTRACTS = {
    'v2': [
        # Core contracts
        '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B',  # Comptroller
        '0xc00e94Cb662C3520282E6f5717214004A7f26888',  # COMP token
        
        # cTokens
        '0x6d903f6003cca6255d85cca4d3b5e5146dc33925',  # cUSDC
        '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',  # cDAI
        '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',  # cETH
        '0x39aa39c021dfbae8fac545936693ac917d5e7563',  # cUSDC (old)
        '0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9',  # cUSDT
        '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4',  # cWBTC
        '0xccf4429db6322d5c611ee964527d42e5d685dd6a',  # cWBTCv2
        '0xface851a4921ce59e912d19329929ce6da6eb0c7',  # cUSDTv2
        
        # Other
        '0xdae7c4d032a1aed2611d5b11b1f6224e9e50d347'   # Lens
    ],
    'v3': [
        '0xc3d688b66703497daa19211eedff47f25384cdc3',  # USDC Mainnet
        '0xa17581a9e3356d9a858b789d68b4d866e593ae94',  # WETH Mainnet
        '0x316f9708bb98af7da9c68c1c3b5e79039cd336e3'   # Rewards
    ]
}

def read_wallets():
    """Read wallet addresses from CSV with validation"""
    if not WALLETS_CSV.exists():
        print(f"Error: {WALLETS_CSV} not found")
        exit(1)
    
    wallets = []
    with open(WALLETS_CSV, 'r') as f:
        for row in csv.reader(f):
            if row and row[0].strip():
                address = row[0].strip().lower()
                if Web3.is_address(address):
                    wallets.append(Web3.to_checksum_address(address))
                else:
                    print(f"Invalid address skipped: {address}")
    return wallets

def fetch_compound_transactions(wallet):
    """Fetch all Compound transactions for a wallet"""
    results = {'v2': [], 'v3': []}
    
    # 1. Check ERC-20 token transfers (where cToken interactions appear)
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet}&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        if data.get('status') == '1':
            for tx in data.get('result', []):
                contract = tx.get('contractAddress', '').lower()
                
                # Check V2 contracts
                if contract in [c.lower() for c in COMPOUND_CONTRACTS['v2']]:
                    results['v2'].append({
                        'hash': tx.get('hash'),
                        'block': tx.get('blockNumber'),
                        'timestamp': tx.get('timeStamp'),
                        'from': tx.get('from'),
                        'to': tx.get('to'),
                        'value': tx.get('value'),
                        'token': tx.get('tokenName', '')
                    })
                
                # Check V3 contracts
                elif contract in [c.lower() for c in COMPOUND_CONTRACTS['v3']]:
                    results['v3'].append({
                        'hash': tx.get('hash'),
                        'block': tx.get('blockNumber'),
                        'timestamp': tx.get('timeStamp'),
                        'from': tx.get('from'),
                        'to': tx.get('to'),
                        'value': tx.get('value'),
                        'token': tx.get('tokenName', '')
                    })
    except Exception as e:
        print(f"Error fetching token transfers for {wallet}: {str(e)}")
    
    # 2. Check normal transactions (for protocol interactions)
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        if data.get('status') == '1':
            for tx in data.get('result', []):
                contract = tx.get('to', '').lower()
                
                if contract in [c.lower() for c in COMPOUND_CONTRACTS['v2'] + COMPOUND_CONTRACTS['v3']]:
                    results['v2' if contract in [c.lower() for c in COMPOUND_CONTRACTS['v2']] else 'v3'].append({
                        'hash': tx.get('hash'),
                        'block': tx.get('blockNumber'),
                        'timestamp': tx.get('timeStamp'),
                        'from': tx.get('from'),
                        'to': tx.get('to'),
                        'value': tx.get('value'),
                        'input': tx.get('input', '')[:100]  # Truncate
                    })
    except Exception as e:
        print(f"Error fetching normal transactions for {wallet}: {str(e)}")
    
    return wallet, results

def main():
    wallets = read_wallets()
    if not wallets:
        print("No valid wallets found")
        return
    
    all_data = {}
    
    print(f"Processing {len(wallets)} wallets...")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fetch_compound_transactions, wallet): wallet for wallet in wallets}
        
        for future in as_completed(futures):
            wallet, data = future.result()
            all_data[wallet] = data
            print(f"Processed {wallet} (V2: {len(data['v2'])}, V3: {len(data['v3'])})")
    
    with open(RAW_DATA_JSON, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nData saved to {RAW_DATA_JSON}")

if __name__ == "__main__":
    main()