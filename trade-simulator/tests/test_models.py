import unittest
from src.models.slippage_model import SlippageModel
from src.models.fee_model import FeeModel
from src.models.market_impact_model import MarketImpactModel
from src.models.maker_taker_model import MakerTakerModel

class TestModels(unittest.TestCase):

    def setUp(self):
        self.slippage_model = SlippageModel()
        self.fee_model = FeeModel()
        self.market_impact_model = MarketImpactModel()
        self.maker_taker_model = MakerTakerModel()

    def test_slippage_estimation(self):
        # Example input parameters
        exchange = "OKX"
        asset = "BTC"
        order_type = "market"
        quantity = 100
        volatility = 0.02
        
        expected_slippage = self.slippage_model.estimate_slippage(exchange, asset, order_type, quantity, volatility)
        self.assertIsInstance(expected_slippage, float)

    def test_fee_calculation(self):
        exchange = "OKX"
        fee_tier = "standard"
        quantity = 100
        
        expected_fees = self.fee_model.calculate_fees(exchange, fee_tier, quantity)
        self.assertIsInstance(expected_fees, float)

    def test_market_impact_calculation(self):
        quantity = 100
        expected_market_impact = self.market_impact_model.calculate_impact(quantity)
        self.assertIsInstance(expected_market_impact, float)

    def test_maker_taker_proportion(self):
        order_type = "market"
        expected_proportion = self.maker_taker_model.predict_proportion(order_type)
        self.assertIsInstance(expected_proportion, float)

if __name__ == '__main__':
    unittest.main()