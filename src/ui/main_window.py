from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
import logging
from typing import Dict
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('OKX Trade Simulator')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel (Input Parameters)
        left_panel = self.create_input_panel()
        main_layout.addWidget(left_panel)
        
        # Create right panel (Output Parameters)
        right_panel = self.create_output_panel()
        main_layout.addWidget(right_panel)
        
        # Set layout proportions
        main_layout.setStretch(0, 1)  # Left panel
        main_layout.setStretch(1, 1)  # Right panel
        
    def create_input_panel(self) -> QGroupBox:
        """Create the input parameters panel"""
        panel = QGroupBox("Input Parameters")
        layout = QVBoxLayout()
        
        # Exchange selection (fixed to OKX)
        exchange_layout = QHBoxLayout()
        exchange_layout.addWidget(QLabel("Exchange:"))
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(["OKX"])
        self.exchange_combo.setEnabled(False)  # Disable as we only support OKX
        exchange_layout.addWidget(self.exchange_combo)
        layout.addLayout(exchange_layout)
        
        # Asset selection
        asset_layout = QHBoxLayout()
        asset_layout.addWidget(QLabel("Asset:"))
        self.asset_combo = QComboBox()
        # Add common OKX trading pairs
        self.asset_combo.addItems([
            "BTC-USDT-SWAP",  # BTC Perpetual Swap
            "ETH-USDT-SWAP",  # ETH Perpetual Swap
            "SOL-USDT-SWAP",  # SOL Perpetual Swap
            "BTC-USDT-SPOT",  # BTC Spot
            "ETH-USDT-SPOT"   # ETH Spot
        ])
        asset_layout.addWidget(self.asset_combo)
        layout.addLayout(asset_layout)
        
        # Order type
        order_type_layout = QHBoxLayout()
        order_type_layout.addWidget(QLabel("Order Type:"))
        self.order_type_combo = QComboBox()
        self.order_type_combo.addItems(["Market"])
        order_type_layout.addWidget(self.order_type_combo)
        layout.addLayout(order_type_layout)
        
        # Quantity
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Quantity (USD):"))
        self.quantity_input = QLineEdit()
        self.quantity_input.setText("100")
        quantity_layout.addWidget(self.quantity_input)
        layout.addLayout(quantity_layout)
        
        # Fee tier (OKX standard fee tier)
        fee_layout = QHBoxLayout()
        fee_layout.addWidget(QLabel("Fee Tier:"))
        self.fee_tier_input = QLineEdit()
        self.fee_tier_input.setText("0.0008")  # OKX standard taker fee
        fee_layout.addWidget(self.fee_tier_input)
        layout.addLayout(fee_layout)
        
        # Start/Stop button
        self.start_button = QPushButton("Start Simulation")
        layout.addWidget(self.start_button)
        
        panel.setLayout(layout)
        return panel
        
    def create_output_panel(self) -> QGroupBox:
        """Create the output parameters panel"""
        panel = QGroupBox("Output Parameters")
        layout = QVBoxLayout()
        
        # Create output labels
        self.slippage_label = QLabel("Expected Slippage: --")
        self.fees_label = QLabel("Expected Fees: --")
        self.market_impact_label = QLabel("Expected Market Impact: --")
        self.net_cost_label = QLabel("Net Cost: --")
        self.maker_taker_label = QLabel("Maker/Taker Proportion: --")
        self.latency_label = QLabel("Internal Latency: --")
        
        # Add labels to layout
        layout.addWidget(self.slippage_label)
        layout.addWidget(self.fees_label)
        layout.addWidget(self.market_impact_label)
        layout.addWidget(self.net_cost_label)
        layout.addWidget(self.maker_taker_label)
        layout.addWidget(self.latency_label)
        
        # Add stretch to push labels to the top
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
        
    def update_outputs(self, data: Dict):
        """Update the output parameters with new data"""
        try:
            self.slippage_label.setText(f"Expected Slippage: {data.get('slippage', 0):.4f}")
            self.fees_label.setText(f"Expected Fees: {data.get('fees', 0):.4f}")
            self.market_impact_label.setText(f"Expected Market Impact: {data.get('market_impact', 0):.4f}")
            self.net_cost_label.setText(f"Net Cost: {data.get('net_cost', 0):.4f}")
            
            maker_prop = data.get('maker_proportion', 0)
            taker_prop = data.get('taker_proportion', 0)
            self.maker_taker_label.setText(
                f"Maker/Taker Proportion: {maker_prop:.2f}/{taker_prop:.2f}"
            )
            
            latency = data.get('processing_latency', 0)
            avg_latency = data.get('avg_processing_latency', 0)
            self.latency_label.setText(
                f"Internal Latency: {latency:.2f}ms (Avg: {avg_latency:.2f}ms)"
            )
            
        except Exception as e:
            self.logger.error(f"Error updating outputs: {str(e)}")
            
    def get_input_parameters(self) -> Dict:
        """Get current input parameters"""
        return {
            'exchange': self.exchange_combo.currentText(),
            'asset': self.asset_combo.currentText(),
            'order_type': self.order_type_combo.currentText(),
            'quantity': float(self.quantity_input.text()),
            'fee_tier': float(self.fee_tier_input.text())
        } 