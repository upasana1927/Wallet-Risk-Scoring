Wallet Risk Scoring System
A system to fetch Compound protocol transactions and calculate risk scores (0-1000) for Ethereum wallets.
📦 System Components

Data Collection: Fetches Compound V2/V3 transactions
Feature Engineering: Processes raw transaction data
Risk Scoring: Calculates wallet risk scores
Visualization: Interactive HTML viewer for risk scores
Output: Generates risk score reports

🛠️ File Structure
wallet-risk-scoring/
├── src/
│   ├── fetch_data.py           # Fetches transaction data
│   ├── risk_scoring.py         # Calculates risk scores
│   └── utils.py                # Helper functions
├── data/
│   ├── wallets.csv             # Input wallet addresses
│   └── raw_data.json           # Raw transaction data
├── output/
│   └── risk_scores.csv         # Final risk scores
├── scores.html             # Interactive CSV viewer
├── requirements.txt            # All Python dependencies
└── README.md

⚙️ Installation

Clone the repository:
git clone https://github.com/your-repo/wallet-risk-scoring.git
cd wallet-risk-scoring

Install dependencies:
pip install -r requirements.txt

Add your API keys to fetch_data.py:

pythonALCHEMY_API_KEY = 'your_alchemy_key'
ETHERSCAN_API_KEY = 'your_etherscan_key'


🚀 Usage
1. Fetch Transaction Data
python src/fetch_data.py

Reads wallets from data/wallets.csv (one address per line)
Saves raw data to data/raw_data.json

2. Calculate Risk Scores
python src/scorer.py

Processes transaction data
Generates output/risk_scores.csv with wallet addresses and scores (0-1000)

3. View Results

Option A: Interactive HTML Viewer (Recommended)

Open scores.html in your browser
Upload your risk_scores.csv file
View data in interactive table with search and statistics

Option B: Direct CSV Access

Open output/risk_scores.csv in Excel/Google Sheets
Or use any CSV viewer application

🔍 Risk Scoring Methodology
Scores calculated using weighted factors:
FactorWeightDescriptionTotal Transactions25%Overall activity levelV2 Transactions15%Legacy protocol usageV3 Transactions25%Current protocol usageUnique Contracts15%Diversity of interactionsTotal Value10%ETH value of transactionsTransaction Frequency5%Time between transactionsV3 Ratio5%Percentage of V3 transactions

📊 Sample Output (risk_scores.csv)
csvwallet,risk_score
0x0039F22efB07A647557C7C5d17854CFD6D489eF3,381
0x1656f1886c5aB634ac19568cd571bC72f385FdF7,135
0x0795732aaCC448030eF374374EaAe57d2965c16C,26

🌐 CSV Viewer Features
The included scores.html provides:

✅ Drag & Drop Upload: Simply drag your CSV file onto the page
✅ Interactive Table: Sortable and searchable data display
✅ Statistics Dashboard: Total wallets, average/min/max scores
✅ Responsive Design: Works on desktop and mobile
✅ No Setup Required: Just open in any modern browser

How to Use CSV Viewer:

Double-click scores.html to open in browser
Upload your risk_scores.csv file
View and analyze your wallet risk data instantly

📋 Resources
API Services:

Alchemy (ALCHEMY_API_KEY)
Etherscan (ETHERSCAN_API_KEY)

Compound Versions:

Compound V2
Compound V3

🧑‍💻 Author
Built by Upasana Ghughtyal
GitHub: https://github.com/upasana1927/Wallet-Risk-Scoring