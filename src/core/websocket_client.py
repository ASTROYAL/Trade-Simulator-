import asyncio
import json
import logging
import websockets
from typing import Dict, List, Callable, Optional
from datetime import datetime

class WebSocketClient:
    def __init__(self, symbol: str):
        # OKX WebSocket endpoint
        self.url = "wss://ws.okx.com:8443/ws/v5/public"
        self.symbol = symbol
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.callbacks: List[Callable] = []
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.heartbeat_task = None

    async def connect(self):
        """Establish WebSocket connection"""
        try:
            self.websocket = await websockets.connect(self.url)
            self.is_connected = True
            self.logger.info(f"Connected to OKX WebSocket at {self.url}")
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket: {str(e)}")
            raise

    async def subscribe(self):
        """Subscribe to the orderbook channel"""
        if not self.websocket:
            raise ConnectionError("WebSocket not connected")
        
        # OKX subscription message format
        subscribe_message = {
            "op": "subscribe",
            "args": [{
                "channel": "books",
                "instId": self.symbol
            }]
        }
        
        await self.websocket.send(json.dumps(subscribe_message))
        self.logger.info(f"Subscribed to {self.symbol} orderbook")

    async def send_heartbeat(self):
        """Send heartbeat message every 20 seconds"""
        while self.is_connected:
            try:
                if self.websocket:
                    heartbeat_message = {"op": "ping"}
                    await self.websocket.send(json.dumps(heartbeat_message))
                    self.logger.debug("Heartbeat sent")
                await asyncio.sleep(20)  # OKX requires heartbeat every 20 seconds
            except Exception as e:
                self.logger.error(f"Error sending heartbeat: {str(e)}")
                break

    def add_callback(self, callback: Callable):
        """Add a callback function to process incoming messages"""
        self.callbacks.append(callback)

    async def process_message(self, message: str):
        """Process incoming WebSocket message"""
        try:
            data = json.loads(message)
            
            # Handle heartbeat response
            if data.get('op') == 'pong':
                self.logger.debug("Received pong response")
                return
                
            # Handle OKX's message format
            if 'data' in data:
                orderbook_data = data['data'][0]
                timestamp = datetime.fromtimestamp(float(orderbook_data['ts']) / 1000)
                
                # Convert OKX's orderbook format to our internal format
                # OKX sends asks and bids as arrays of [price, size, num_orders, ...]
                asks = [[float(price), float(size)] for price, size, *_ in orderbook_data['asks']]
                bids = [[float(price), float(size)] for price, size, *_ in orderbook_data['bids']]
                
                processed_data = {
                    'timestamp': timestamp,
                    'exchange': 'OKX',
                    'symbol': self.symbol,
                    'asks': asks,
                    'bids': bids
                }
                
                # Notify all callbacks
                for callback in self.callbacks:
                    await callback(processed_data)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode message: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")

    async def start(self):
        """Start the WebSocket client"""
        try:
            await self.connect()
            await self.subscribe()
            
            # Start heartbeat task
            self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
            
            while self.is_connected:
                try:
                    message = await self.websocket.recv()
                    await self.process_message(message)
                except websockets.ConnectionClosed:
                    self.logger.warning("WebSocket connection closed")
                    break
                except Exception as e:
                    self.logger.error(f"Error in WebSocket loop: {str(e)}")
                    break
                    
        except Exception as e:
            self.logger.error(f"WebSocket client error: {str(e)}")
        finally:
            await self.close()

    async def close(self):
        """Close the WebSocket connection"""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
            
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            self.logger.info("WebSocket connection closed") 