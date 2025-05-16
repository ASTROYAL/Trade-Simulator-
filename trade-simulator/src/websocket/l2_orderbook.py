class L2OrderBook:
    def __init__(self, url):
        self.url = url
        self.order_book_data = {}
        self.callbacks = []

    def connect(self):
        # Code to establish WebSocket connection
        pass

    def on_message(self, message):
        # Code to process incoming WebSocket messages
        self.order_book_data = self.parse_message(message)
        self.update_callbacks()

    def parse_message(self, message):
        # Code to parse the incoming message and extract order book data
        return {
            "timestamp": message["timestamp"],
            "exchange": message["exchange"],
            "symbol": message["symbol"],
            "asks": message["asks"],
            "bids": message["bids"]
        }

    def update_callbacks(self):
        for callback in self.callbacks:
            callback(self.order_book_data)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def start(self):
        self.connect()
        # Code to keep the WebSocket connection alive
        pass