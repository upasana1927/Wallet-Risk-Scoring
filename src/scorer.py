from pathlib import Path
import pandas as pd
import numpy as np
from utils import load_transaction_data, preprocess_data, save_risk_scores

def calculate_risk_scores(features):
    """Calculate risk scores (0-1000) based on transaction features"""
    scores = {}
    
    # Convert features to DataFrame
    df = pd.DataFrame.from_dict(features, orient='index')
    
    # Normalize features (0-1 scale)
    df_normalized = df.copy()
    for col in df.columns:
        if df[col].max() > 0:  # Avoid division by zero
            df_normalized[col] = df[col] / df[col].max()
    
    # Weighted scoring (adjust weights as needed)
    weights = {
        'total_tx': 0.25,
        'v2_tx_count': 0.15,
        'v3_tx_count': 0.25,
        'unique_contracts': 0.15,
        'total_value': 0.10,
        'avg_tx_frequency': 0.05,
        'v3_ratio': 0.05
    }
    
    # Calculate weighted score (0-1000)
    for wallet in features:
        weighted_sum = sum(
            df_normalized.loc[wallet, feature] * weight 
            for feature, weight in weights.items()
        )
        scores[wallet] = int(weighted_sum * 1000)
    
    return scores

def main():
    # Load and preprocess data
    data_dir = Path(__file__).parent.parent / 'data'
    wallet_data = load_transaction_data(data_dir)
    features = preprocess_data(wallet_data)
    
    # Calculate risk scores
    risk_scores = calculate_risk_scores(features)
    
    # Save results
    output_dir = Path(__file__).parent.parent / 'output'
    save_risk_scores(risk_scores, output_dir)

if __name__ == "__main__":
    main()