# Models Documentation

## Slippage Model
The SlippageModel class estimates expected slippage based on input parameters using linear or quantile regression techniques. The model takes into account the market conditions and the size of the order relative to the order book depth.

### Parameters:
- **Input Parameters**: Quantity, Spot Asset, Market Volatility
- **Output**: Expected Slippage

## Fee Model
The FeeModel class calculates expected transaction fees using a rule-based approach. This model is designed to accommodate different fee tiers based on the selected exchange's documentation.

### Parameters:
- **Input Parameters**: Exchange, Fee Tier, Quantity
- **Output**: Expected Fees

## Market Impact Model
The MarketImpactModel class implements the Almgren-Chriss model to estimate the market impact of executing trades. This model considers the order size and the current market conditions to provide a realistic estimate of the impact on the market price.

### Parameters:
- **Input Parameters**: Quantity, Market Conditions
- **Output**: Expected Market Impact

## Maker/Taker Model
The MakerTakerModel class predicts the proportion of maker and taker orders using logistic regression. This model helps in understanding the trading strategy and its implications on transaction costs.

### Parameters:
- **Input Parameters**: Historical Trade Data, Market Conditions
- **Output**: Maker/Taker Proportion

## Conclusion
These models work together to provide a comprehensive analysis of trading costs and impacts, enabling users to make informed decisions in real-time trading scenarios. Each model is designed to be modular and can be updated or replaced as needed to improve accuracy and performance.