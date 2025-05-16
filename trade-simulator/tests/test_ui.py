import unittest
from src.ui.input_panel import InputPanel
from src.ui.output_panel import OutputPanel

class TestUIComponents(unittest.TestCase):

    def setUp(self):
        self.input_panel = InputPanel()
        self.output_panel = OutputPanel()

    def test_input_panel_initialization(self):
        self.assertIsNotNone(self.input_panel)

    def test_output_panel_initialization(self):
        self.assertIsNotNone(self.output_panel)

    def test_input_parameters(self):
        self.input_panel.set_exchange("OKX")
        self.input_panel.set_spot_asset("BTC")
        self.input_panel.set_order_type("market")
        self.input_panel.set_quantity(100)
        self.input_panel.set_volatility(0.05)
        self.input_panel.set_fee_tier("Tier 1")

        self.assertEqual(self.input_panel.exchange, "OKX")
        self.assertEqual(self.input_panel.spot_asset, "BTC")
        self.assertEqual(self.input_panel.order_type, "market")
        self.assertEqual(self.input_panel.quantity, 100)
        self.assertEqual(self.input_panel.volatility, 0.05)
        self.assertEqual(self.input_panel.fee_tier, "Tier 1")

    def test_output_update(self):
        self.output_panel.update_slippage(0.01)
        self.output_panel.update_fees(0.005)
        self.output_panel.update_market_impact(0.02)
        self.output_panel.update_net_cost(0.035)
        self.output_panel.update_maker_taker_proportion(0.6)
        self.output_panel.update_internal_latency(0.1)

        self.assertEqual(self.output_panel.slippage, 0.01)
        self.assertEqual(self.output_panel.fees, 0.005)
        self.assertEqual(self.output_panel.market_impact, 0.02)
        self.assertEqual(self.output_panel.net_cost, 0.035)
        self.assertEqual(self.output_panel.maker_taker_proportion, 0.6)
        self.assertEqual(self.output_panel.internal_latency, 0.1)

if __name__ == '__main__':
    unittest.main()