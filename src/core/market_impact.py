import numpy as np
from typing import List, Tuple
import logging

class AlmgrenChrissModel:
    def __init__(self, eta: float = 0.1, gamma: float = 0.1):
        """
        Initialize the Almgren-Chriss model with parameters:
        eta: Temporary market impact parameter
        gamma: Permanent market impact parameter
        """
        self.eta = eta
        self.gamma = gamma
        self.logger = logging.getLogger(__name__)

    def calculate_impact(self, quantity: float, price: float, depth: int) -> float:
        """
        Calculate market impact using the Almgren-Chriss model
        
        Args:
            quantity: Order quantity
            price: Current market price
            depth: Order book depth
            
        Returns:
            float: Estimated market impact
        """
        try:
            # Calculate temporary impact
            temp_impact = self.eta * (quantity / depth) * price
            
            # Calculate permanent impact
            perm_impact = self.gamma * quantity * price
            
            # Total impact
            total_impact = temp_impact + perm_impact
            
            return total_impact
            
        except Exception as e:
            self.logger.error(f"Error calculating market impact: {str(e)}")
            return 0.0

    def optimize_execution(self, 
                         quantity: float, 
                         price: float, 
                         time_horizon: float,
                         volatility: float) -> List[Tuple[float, float]]:
        """
        Optimize execution schedule using Almgren-Chriss model
        
        Args:
            quantity: Total quantity to execute
            price: Initial price
            time_horizon: Total time for execution
            volatility: Market volatility
            
        Returns:
            List of (time, quantity) tuples representing optimal execution schedule
        """
        try:
            # Model parameters
            kappa = np.sqrt(self.gamma / self.eta)  # Risk aversion parameter
            
            # Time grid
            n_steps = 10
            times = np.linspace(0, time_horizon, n_steps)
            
            # Calculate optimal execution schedule
            schedule = []
            remaining_qty = quantity
            
            for t in times:
                # Calculate optimal quantity at time t
                q_t = quantity * (1 - np.exp(-kappa * (time_horizon - t))) / (1 - np.exp(-kappa * time_horizon))
                
                # Calculate quantity to execute in this step
                step_qty = q_t - (quantity - remaining_qty)
                step_qty = max(0, min(step_qty, remaining_qty))
                
                schedule.append((t, step_qty))
                remaining_qty -= step_qty
                
            return schedule
            
        except Exception as e:
            self.logger.error(f"Error optimizing execution schedule: {str(e)}")
            return [(0, quantity)]  # Return simple immediate execution as fallback 