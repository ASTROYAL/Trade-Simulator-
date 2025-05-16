import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime
import logging
from .market_impact import AlmgrenChrissModel

class OrderbookProcessor:
    def __init__(self, quantity: float, fee_tier: float):
        self.quantity = quantity
        self.fee_tier = fee_tier
        self.logger = logging.getLogger(__name__)
        self.market_impact_model = AlmgrenChrissModel()
        
        # Performance tracking
        self.processing_times: List[float] = []
        self.last_update_time: datetime = None
        
        # Cache for calculations
        self._cache = {}
        self._cache_timeout = 1.0  # Cache timeout in seconds

    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached value is still valid"""
        if key not in self._cache:
            return False
        cache_time, _ = self._cache[key]
        return (datetime.now() - cache_time).total_seconds() < self._cache_timeout

    def _get_cached_value(self, key: str):
        """Get cached value if valid"""
        if self._is_cache_valid(key):
            return self._cache[key][1]
        return None

    def _set_cached_value(self, key: str, value):
        """Set cached value with current timestamp"""
        self._cache[key] = (datetime.now(), value)

    def calculate_slippage(self, asks: List[List[float]], quantity: float) -> float:
        """Calculate expected slippage using weighted average price"""
        cache_key = f"slippage_{quantity}_{asks[0][0] if asks else 0}"
        cached_value = self._get_cached_value(cache_key)
        if cached_value is not None:
            return cached_value

        try:
            # Simple implementation using weighted average price
            total_cost = 0
            remaining_quantity = quantity
            
            for price, qty in asks:
                if remaining_quantity <= 0:
                    break
                    
                executed_qty = min(remaining_quantity, qty)
                total_cost += executed_qty * price
                remaining_quantity -= executed_qty
            
            if remaining_quantity > 0:
                self.logger.warning(f"Not enough liquidity for quantity {quantity}")
                return float('inf')
                
            avg_price = total_cost / quantity
            slippage = (avg_price - asks[0][0]) / asks[0][0]
            
            self._set_cached_value(cache_key, slippage)
            return slippage
            
        except Exception as e:
            self.logger.error(f"Error calculating slippage: {str(e)}")
            return 0.0

    def calculate_fees(self, quantity: float, price: float) -> float:
        """Calculate expected fees based on fee tier"""
        cache_key = f"fees_{quantity}_{price}"
        cached_value = self._get_cached_value(cache_key)
        if cached_value is not None:
            return cached_value

        try:
            fees = quantity * price * self.fee_tier
            self._set_cached_value(cache_key, fees)
            return fees
        except Exception as e:
            self.logger.error(f"Error calculating fees: {str(e)}")
            return 0.0

    def calculate_maker_taker_proportion(self, asks: List[List[float]], bids: List[List[float]]) -> Tuple[float, float]:
        """Calculate maker/taker proportion using order book imbalance"""
        cache_key = f"proportion_{len(asks)}_{len(bids)}"
        cached_value = self._get_cached_value(cache_key)
        if cached_value is not None:
            return cached_value

        try:
            # Simple implementation using order book imbalance
            ask_volume = sum(qty for _, qty in asks)
            bid_volume = sum(qty for _, qty in bids)
            total_volume = ask_volume + bid_volume
            
            if total_volume == 0:
                return 0.5, 0.5
                
            maker_prop = bid_volume / total_volume
            taker_prop = 1 - maker_prop
            
            result = (maker_prop, taker_prop)
            self._set_cached_value(cache_key, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating maker/taker proportion: {str(e)}")
            return 0.5, 0.5

    def process_orderbook(self, data: Dict) -> Dict:
        """Process orderbook data and calculate all metrics"""
        start_time = datetime.now()
        
        try:
            asks = data['asks']
            bids = data['bids']
            
            # Calculate metrics
            slippage = self.calculate_slippage(asks, self.quantity)
            fees = self.calculate_fees(self.quantity, asks[0][0])
            market_impact = self.market_impact_model.calculate_impact(
                self.quantity,
                asks[0][0],
                len(asks)
            )
            maker_prop, taker_prop = self.calculate_maker_taker_proportion(asks, bids)
            
            # Calculate net cost
            net_cost = slippage + fees + market_impact
            
            # Calculate processing latency
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            self.processing_times.append(processing_time)
            
            # Keep only last 100 processing times
            if len(self.processing_times) > 100:
                self.processing_times.pop(0)
            
            return {
                'timestamp': data['timestamp'],
                'slippage': slippage,
                'fees': fees,
                'market_impact': market_impact,
                'net_cost': net_cost,
                'maker_proportion': maker_prop,
                'taker_proportion': taker_prop,
                'processing_latency': processing_time,
                'avg_processing_latency': np.mean(self.processing_times)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing orderbook: {str(e)}")
            return {} 