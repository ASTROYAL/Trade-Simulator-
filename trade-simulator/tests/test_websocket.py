import unittest
from unittest.mock import patch, MagicMock
from src.websocket.l2_orderbook import L2OrderBook

class TestL2OrderBook(unittest.TestCase):

    @patch('src.websocket.l2_orderbook.websocket')
    def test_websocket_connection(self, mock_websocket):
        mock_websocket.connect.return_value = True
        order_book = L2OrderBook('wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP')
        self.assertTrue(order_book.connect())

    @patch('src.websocket.l2_orderbook.websocket')
    def test_process_order_book_data(self, mock_websocket):
        mock_data = {
            "timestamp": "2025-05-04T10:39:13Z",
            "exchange": "OKX",
            "symbol": "BTC-USDT-SWAP",
            "asks": [["95445.5", "9.06"], ["95448", "2.05"]],
            "bids": [["95445.4", "1104.23"], ["95445.3", "0.02"]]
        }
        order_book = L2OrderBook('wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP')
        order_book.process_order_book_data(mock_data)
        self.assertEqual(order_book.asks, mock_data['asks'])
        self.assertEqual(order_book.bids, mock_data['bids'])

    @patch('src.websocket.l2_orderbook.websocket')
    def test_handle_error(self, mock_websocket):
        order_book = L2OrderBook('wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP')
        with self.assertRaises(Exception):
            order_book.handle_error("Connection error")

if __name__ == '__main__':
    unittest.main()