class OutputPanel:
    def __init__(self):
        self.expected_slippage = None
        self.expected_fees = None
        self.expected_market_impact = None
        self.net_cost = None
        self.maker_taker_proportion = None
        self.internal_latency = None

    def update_slippage(self, slippage):
        self.expected_slippage = slippage
        self.refresh_display()

    def update_fees(self, fees):
        self.expected_fees = fees
        self.refresh_display()

    def update_market_impact(self, market_impact):
        self.expected_market_impact = market_impact
        self.refresh_display()

    def update_net_cost(self, net_cost):
        self.net_cost = net_cost
        self.refresh_display()

    def update_maker_taker_proportion(self, proportion):
        self.maker_taker_proportion = proportion
        self.refresh_display()

    def update_internal_latency(self, latency):
        self.internal_latency = latency
        self.refresh_display()

    def refresh_display(self):
        # Code to refresh the UI display with updated values
        pass