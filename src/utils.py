import json
from pathlib import Path
import pandas as pd
import numpy as np

def load_transaction_data(data_dir):
    """Load transaction data from JSON file"""
    data_path = Path(data_dir) / 'raw_data.json'
    with open(data_path, 'r') as f:
        return json.load(f)

def save_risk_scores(scores, output_dir):
    """Save risk scores to CSV"""
    output_path = Path(output_dir) / 'risk_scores.csv'
    Path(output_dir).mkdir(exist_ok=True)
    pd.DataFrame.from_dict(scores, orient='index', columns=['risk_score']).reset_index().rename(columns={'index': 'wallet'}).to_csv(output_path, index=False)
    print(f"✅ Risk scores saved to {output_path}")

def preprocess_data(wallet_data):
    """Extract features from raw transaction data"""
    features = {}
    for wallet, transactions in wallet_data.items():
        v2_tx = transactions['v2']
        v3_tx = transactions['v3']
        all_tx = v2_tx + v3_tx
        
        # Basic transaction counts
        features[wallet] = {
            'total_tx': len(all_tx),
            'v2_tx_count': len(v2_tx),
            'v3_tx_count': len(v3_tx),
            'unique_contracts': len(set(tx.get('to', '') for tx in all_tx)),
            'total_value': sum(int(tx.get('value', 0)) for tx in all_tx) / 1e18,  # Convert from wei
            'avg_tx_frequency': calculate_tx_frequency(all_tx),
            'v3_ratio': len(v3_tx) / (len(all_tx) + 1e-6)  # Avoid division by zero
        }
    return features

def calculate_tx_frequency(transactions):
    """Calculate average time between transactions in days"""
    if len(transactions) < 2:
        return 0
    timestamps = sorted(int(tx['timestamp']) for tx in transactions)
    deltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    return np.mean(deltas) / (24 * 3600) if deltas else 0