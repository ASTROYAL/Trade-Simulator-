import asyncio
import websockets
import json
from ui.input_panel import InputPanel
from ui.output_panel import OutputPanel
from websocket.l2_orderbook import L2OrderBook
from models.slippage_model import SlippageModel
from models.fee_model import FeeModel
from models.market_impact_model import MarketImpactModel
from models.maker_taker_model import MakerTakerModel
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class TradeSimulator:
    def __init__(self):
        self.input_panel = InputPanel()
        self.output_panel = OutputPanel()
        self.order_book = L2OrderBook(self.process_order_book)
        self.slippage_model = SlippageModel()
        self.fee_model = FeeModel()
        self.market_impact_model = MarketImpactModel()
        self.maker_taker_model = MakerTakerModel()
        self.logger = Logger()
        self.error_handler = ErrorHandler()

    async def connect_websocket(self):
        try:
            async with websockets.connect("wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP") as websocket:
                while True:
                    response = await websocket.recv()
                    order_book_data = json.loads(response)
                    self.order_book.update(order_book_data)
        except Exception as e:
            self.error_handler.handle(e)

    def process_order_book(self, order_book_data):
        try:
            slippage = self.slippage_model.estimate_slippage(self.input_panel.get_parameters())
            fees = self.fee_model.calculate_fees(self.input_panel.get_parameters())
            market_impact = self.market_impact_model.calculate_impact(order_book_data)
            maker_taker_proportion = self.maker_taker_model.predict_proportion(order_book_data)

            net_cost = slippage + fees + market_impact

            self.output_panel.update_output(slippage, fees, market_impact, net_cost, maker_taker_proportion)
        except Exception as e:
            self.error_handler.handle(e)

    def run(self):
        self.input_panel.display()
        asyncio.run(self.connect_websocket())

if __name__ == "__main__":
    simulator = TradeSimulator()
    simulator.run()