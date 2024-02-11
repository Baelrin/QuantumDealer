---

# Quantum Dealer

Quantum Dealer is a machine learning-based trading bot that uses sentiment analysis to make buy or sell decisions based on news headlines. It leverages the power of Alpaca's paper trading platform to simulate trades without risking real money.

## Features

- Sentiment Analysis: Uses FinBERT to analyze the sentiment of news headlines related to a specific stock symbol.
- Backtesting: Tests the strategy against historical data to evaluate its performance.
- Paper Trading: Executes trades on Alpaca's paper trading platform, allowing users to test strategies without financial risk.

## Prerequisites

- Python  3.7+
- An Alpaca account with API keys
- Environment variables for `ALPACA_API_KEY` and `ALPACA_API_SECRET`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Baelrin/quantum-dealer.git
   ```
2. Navigate to the project directory:
   ```
   cd quantum-dealer
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables:

- `ALPACA_API_KEY`: Your Alpaca API key
- `ALPACA_API_SECRET`: Your Alpaca API secret

## Usage

To run the backtest simulation:

```bash
python master.py
```

To execute live trades (ensure you understand the risks involved):

```bash
# Uncomment the relevant lines in master.py
# python master.py
```

## Contributing

Contributions are welcome! Please read the contributing guide before submitting pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
