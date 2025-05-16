import sys
import asyncio
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from ui.main_window import MainWindow
from core.websocket_client import WebSocketClient
from core.orderbook_processor import OrderbookProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebSocketThread(QThread):
    orderbook_update = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol
        self.websocket_client = None
        self.is_running = False
        
    def run(self):
        """Run the WebSocket client in a separate thread"""
        try:
            self.websocket_client = WebSocketClient(self.symbol)
            self.websocket_client.add_callback(self.handle_orderbook)
            
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Start WebSocket client
            self.is_running = True
            loop.run_until_complete(self.websocket_client.start())
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.is_running = False
            
    async def handle_orderbook(self, data):
        """Handle incoming orderbook data"""
        self.orderbook_update.emit(data)
        
    def stop(self):
        """Stop the WebSocket client"""
        self.is_running = False
        if self.websocket_client:
            loop = asyncio.get_event_loop()
            loop.create_task(self.websocket_client.close())

class TradeSimulator:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.websocket_thread = None
        self.orderbook_processor = None
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)  # Update UI every 100ms
        self.update_timer.timeout.connect(self.update_ui)
        self.pending_updates = []
        
        # Connect UI signals
        self.window.start_button.clicked.connect(self.toggle_simulation)
        
    def setup_components(self):
        """Initialize WebSocket client and orderbook processor"""
        try:
            # Get input parameters
            params = self.window.get_input_parameters()
            
            # Initialize WebSocket thread
            self.websocket_thread = WebSocketThread(params['asset'])
            self.websocket_thread.orderbook_update.connect(self.handle_orderbook)
            self.websocket_thread.error_occurred.connect(self.handle_error)
            
            # Initialize orderbook processor
            self.orderbook_processor = OrderbookProcessor(
                quantity=params['quantity'],
                fee_tier=params['fee_tier']
            )
            
        except Exception as e:
            logger.error(f"Error setting up components: {str(e)}")
            self.is_running = False
            
    def toggle_simulation(self):
        """Toggle simulation on/off"""
        if not self.websocket_thread or not self.websocket_thread.is_running:
            self.setup_components()
            self.websocket_thread.start()
            self.update_timer.start()
            self.window.start_button.setText("Stop Simulation")
        else:
            self.websocket_thread.stop()
            self.update_timer.stop()
            self.window.start_button.setText("Start Simulation")
            
    def handle_orderbook(self, data):
        """Handle incoming orderbook data"""
        try:
            if self.orderbook_processor:
                # Process orderbook data
                results = self.orderbook_processor.process_orderbook(data)
                self.pending_updates.append(results)
        except Exception as e:
            logger.error(f"Error processing orderbook: {str(e)}")
            
    def update_ui(self):
        """Update UI with latest results"""
        if self.pending_updates:
            latest_results = self.pending_updates[-1]
            self.window.update_outputs(latest_results)
            self.pending_updates.clear()
            
    def handle_error(self, error_msg):
        """Handle WebSocket errors"""
        logger.error(f"WebSocket error: {error_msg}")
        self.window.show_error(error_msg)
        self.toggle_simulation()  # Stop simulation on error
            
    def run(self):
        """Run the application"""
        self.window.show()
        return self.app.exec()

if __name__ == "__main__":
    simulator = TradeSimulator()
    sys.exit(simulator.run()) 