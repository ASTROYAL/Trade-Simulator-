# Trade Simulator

## Overview
The Trade Simulator is a high-performance application designed to simulate trading activities in real-time using market data from cryptocurrency exchanges. It estimates transaction costs and market impact based on user-defined parameters and real-time order book data.

## Objectives
- Connect to WebSocket endpoints to receive full L2 order book data.
- Estimate transaction costs, including expected slippage, fees, and market impact.
- Provide a user-friendly interface for inputting parameters and displaying results.

## Features
- Real-time processing of order book data.
- Estimation of expected slippage using regression models.
- Calculation of expected fees based on exchange fee tiers.
- Implementation of the Almgren-Chriss model for market impact assessment.
- Prediction of maker/taker proportions using logistic regression.
- Performance analysis and optimization techniques for latency and resource management.

## Project Structure
```
trade-simulator
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui                     # User interface components
│   ├── models                  # Model implementations for calculations
│   ├── websocket               # WebSocket connection management
│   ├── utils                   # Utility functions for logging and error handling
│   └── config                  # Configuration settings
├── tests                       # Unit tests for various components
├── docs                        # Documentation for models, optimization, and usage
├── requirements.txt            # Project dependencies
├── README.md                   # Project overview and instructions
└── .gitignore                  # Files to ignore in version control
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd trade-simulator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the WebSocket endpoint in `src/config/settings.py`.

4. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines
- Input parameters such as exchange, asset, order type, quantity, volatility, and fee tier through the user interface.
- Monitor the output values for expected slippage, fees, market impact, net cost, maker/taker proportion, and internal latency.

## Documentation
Refer to the `docs` directory for detailed documentation on models, optimization techniques, and usage instructions.

## Contribution
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.