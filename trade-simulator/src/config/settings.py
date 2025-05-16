# Configuration settings for the trade simulator application

# WebSocket endpoint for L2 orderbook data
WEBSOCKET_ENDPOINT = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

# Default parameters
DEFAULT_EXCHANGE = "OKX"
DEFAULT_SPOT_ASSET = "BTC-USDT"
DEFAULT_ORDER_TYPE = "market"
DEFAULT_QUANTITY = 100  # USD equivalent
DEFAULT_VOLATILITY = 0.02  # Example volatility
DEFAULT_FEE_TIER = "standard"

# Model parameters
SLIPPAGE_MODEL_TYPE = "linear"  # Options: "linear", "quantile"
MAKER_TAKER_MODEL_TYPE = "logistic"  # Options: "logistic", "other"

# Logging settings
LOGGING_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"