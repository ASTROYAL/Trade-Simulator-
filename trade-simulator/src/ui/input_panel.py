class InputPanel:
    def __init__(self):
        self.exchange = None
        self.spot_asset = None
        self.order_type = None
        self.quantity = None
        self.volatility = None
        self.fee_tier = None

    def gather_inputs(self):
        self.exchange = input("Enter Exchange (e.g., OKX): ")
        self.spot_asset = input("Enter Spot Asset: ")
        self.order_type = input("Enter Order Type (market): ")
        self.quantity = float(input("Enter Quantity (~100 USD equivalent): "))
        self.volatility = float(input("Enter Volatility: "))
        self.fee_tier = input("Enter Fee Tier: ")

    def get_inputs(self):
        return {
            "exchange": self.exchange,
            "spot_asset": self.spot_asset,
            "order_type": self.order_type,
            "quantity": self.quantity,
            "volatility": self.volatility,
            "fee_tier": self.fee_tier,
        }