# Trade Simulator Usage Instructions

## Overview
The Trade Simulator is designed to provide a high-performance environment for simulating trades using real-time market data. This document outlines the steps required to set up and use the simulator effectively.

## Prerequisites
- Python 3.7 or higher
- Required libraries listed in `requirements.txt`

## Setup Instructions
1. **Clone the Repository**
   ```
   git clone https://github.com/yourusername/trade-simulator.git
   cd trade-simulator
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Open `src/config/settings.py` to configure the WebSocket endpoint and any other necessary settings.

## Running the Simulator
1. **Start the Application**
   ```
   python src/main.py
   ```

2. **User Interface**
   - The application will launch a user interface with two main panels:
     - **Input Parameters Panel (Left)**
       - Select the exchange (OKX).
       - Choose the spot asset available on the exchange.
       - Specify the order type (market).
       - Enter the quantity (approximately 100 USD equivalent).
       - Set the volatility parameter.
       - Choose the fee tier based on the exchange documentation.
     - **Output Values Panel (Right)**
       - This panel will display the processed output values, including expected slippage, fees, market impact, net cost, maker/taker proportion, and internal latency.

3. **Real-Time Data Processing**
   - The simulator connects to the WebSocket endpoint to receive real-time L2 order book data. The output parameters will update automatically with each new tick.

## Error Handling
- The application includes error handling mechanisms to manage exceptions and ensure smooth operation. Any issues will be logged for review.

## Documentation
- For detailed information on the models and algorithms used, refer to `docs/models.md`.
- For performance optimization techniques, see `docs/optimization.md`.

## Support
For any issues or questions, please refer to the project's GitHub repository or contact the maintainers.