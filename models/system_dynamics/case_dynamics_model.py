#!/usr/bin/env python3
"""
System Dynamics Model for Legal Case Flow Analysis

This module implements a system dynamics simulation framework for modeling
the flow and accumulation of cases through the judicial system using
stock-and-flow dynamics.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Stock:
    """Represents a stock (accumulation) in the system."""
    name: str
    initial_value: float
    current_value: float
    history: List[float]
    
    def update(self, net_flow: float, dt: float):
        """Update stock based on net flow."""
        self.current_value += net_flow * dt
        self.current_value = max(0, self.current_value)  # Prevent negative stocks
        self.history.append(self.current_value)


@dataclass
class Flow:
    """Represents a flow (rate) in the system."""
    name: str
    rate: float
    history: List[float]
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float]) -> float:
        """Calculate flow rate based on stocks and parameters."""
        # Override in specific flow implementations
        return self.rate
    
    def record(self):
        """Record current rate in history."""
        self.history.append(self.rate)


class CaseFilingFlow(Flow):
    """Flow representing new case filings."""
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float]) -> float:
        """Calculate case filing rate."""
        base_filing_rate = parameters.get('base_filing_rate', 2.0)
        seasonal_factor = parameters.get('seasonal_factor', 1.0)
        
        # Add some variability
        noise = np.random.normal(0, 0.1)
        self.rate = max(0, base_filing_rate * seasonal_factor * (1 + noise))
        return self.rate


class CaseProcessingFlow(Flow):
    """Flow representing case processing through stages."""
    
    def __init__(self, name: str, source_stock: str, processing_time: float):
        super().__init__(name, 0.0, [])
        self.source_stock = source_stock
        self.processing_time = processing_time
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float]) -> float:
        """Calculate processing rate based on source stock and capacity."""
        source = stocks.get(self.source_stock)
        if not source:
            self.rate = 0.0
            return self.rate
        
        # Processing capacity
        capacity = parameters.get('processing_capacity', 10.0)
        efficiency = parameters.get('efficiency', 0.8)
        
        # Rate limited by capacity and stock availability
        desired_rate = source.current_value / self.processing_time
        actual_rate = min(desired_rate, capacity * efficiency)
        
        self.rate = max(0, actual_rate)
        return self.rate


class CaseClosureFlow(Flow):
    """Flow representing case closures."""
    
    def __init__(self, name: str, source_stock: str, closure_time: float):
        super().__init__(name, 0.0, [])
        self.source_stock = source_stock
        self.closure_time = closure_time
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float]) -> float:
        """Calculate closure rate."""
        source = stocks.get(self.source_stock)
        if not source:
            self.rate = 0.0
            return self.rate
        
        closure_efficiency = parameters.get('closure_efficiency', 0.9)
        self.rate = (source.current_value / self.closure_time) * closure_efficiency
        return self.rate


class SystemDynamicsSimulation:
    """Main system dynamics simulation engine."""
    
    def __init__(self, dt: float = 1.0, duration: float = 365.0):
        self.dt = dt  # Time step (days)
        self.duration = duration  # Total simulation duration (days)
        self.current_time = 0.0
        
        # System components
        self.stocks: Dict[str, Stock] = {}
        self.flows: Dict[str, Flow] = {}
        self.parameters: Dict[str, float] = {}
        
        # Initialize default system
        self._initialize_system()
        
        logger.info(f"Initialized system dynamics simulation (dt={dt}, duration={duration})")
    
    def _initialize_system(self):
        """Initialize the case flow system with stocks and flows."""
        # Stocks (case accumulations at different stages)
        self.stocks = {
            'filed_cases': Stock('filed_cases', 50.0, 50.0, [50.0]),
            'discovery_cases': Stock('discovery_cases', 30.0, 30.0, [30.0]),
            'pretrial_cases': Stock('pretrial_cases', 20.0, 20.0, [20.0]),
            'trial_cases': Stock('trial_cases', 10.0, 10.0, [10.0]),
            'ruling_cases': Stock('ruling_cases', 5.0, 5.0, [5.0]),
            'closed_cases': Stock('closed_cases', 0.0, 0.0, [0.0])
        }
        
        # Flows (transitions between stages)
        self.flows = {
            'case_filing': CaseFilingFlow('case_filing', 2.0, []),
            'to_discovery': CaseProcessingFlow('to_discovery', 'filed_cases', 15.0),
            'to_pretrial': CaseProcessingFlow('to_pretrial', 'discovery_cases', 30.0),
            'to_trial': CaseProcessingFlow('to_trial', 'pretrial_cases', 20.0),
            'to_ruling': CaseProcessingFlow('to_ruling', 'trial_cases', 10.0),
            'to_closure': CaseClosureFlow('to_closure', 'ruling_cases', 5.0)
        }
        
        # Parameters
        self.parameters = {
            'base_filing_rate': 2.0,
            'seasonal_factor': 1.0,
            'processing_capacity': 15.0,
            'efficiency': 0.85,
            'closure_efficiency': 0.95
        }
    
    def set_parameter(self, name: str, value: float):
        """Set a simulation parameter."""
        self.parameters[name] = value
    
    def step(self):
        """Execute one time step of the simulation."""
        # Calculate all flow rates
        for flow in self.flows.values():
            flow.calculate_rate(self.stocks, self.parameters)
            flow.record()
        
        # Update stocks based on flows
        # Filed cases: inflow from filing, outflow to discovery
        self.stocks['filed_cases'].update(
            self.flows['case_filing'].rate - self.flows['to_discovery'].rate,
            self.dt
        )
        
        # Discovery cases: inflow from filed, outflow to pretrial
        self.stocks['discovery_cases'].update(
            self.flows['to_discovery'].rate - self.flows['to_pretrial'].rate,
            self.dt
        )
        
        # Pretrial cases: inflow from discovery, outflow to trial
        self.stocks['pretrial_cases'].update(
            self.flows['to_pretrial'].rate - self.flows['to_trial'].rate,
            self.dt
        )
        
        # Trial cases: inflow from pretrial, outflow to ruling
        self.stocks['trial_cases'].update(
            self.flows['to_trial'].rate - self.flows['to_ruling'].rate,
            self.dt
        )
        
        # Ruling cases: inflow from trial, outflow to closure
        self.stocks['ruling_cases'].update(
            self.flows['to_ruling'].rate - self.flows['to_closure'].rate,
            self.dt
        )
        
        # Closed cases: inflow from closure only
        self.stocks['closed_cases'].update(
            self.flows['to_closure'].rate,
            self.dt
        )
        
        self.current_time += self.dt
    
    def run(self) -> Dict[str, Any]:
        """Run the system dynamics simulation."""
        logger.info(f"Starting system dynamics simulation")
        
        num_steps = int(self.duration / self.dt)
        
        for step in range(num_steps):
            self.step()
            
            # Occasional parameter adjustments (simulate policy changes)
            if step == num_steps // 3:
                self.set_parameter('processing_capacity', 18.0)
                logger.info("Policy change: Increased processing capacity to 18.0")
            
            if step == 2 * num_steps // 3:
                self.set_parameter('efficiency', 0.90)
                logger.info("Policy change: Improved efficiency to 0.90")
        
        results = self.calculate_results()
        
        logger.info(f"Simulation completed at time {self.current_time:.2f}")
        logger.info(f"Total cases closed: {self.stocks['closed_cases'].current_value:.2f}")
        
        return results
    
    def calculate_results(self) -> Dict[str, Any]:
        """Calculate simulation results and statistics."""
        # Calculate average stock levels
        avg_stocks = {
            name: np.mean(stock.history) for name, stock in self.stocks.items()
        }
        
        # Calculate total throughput
        total_filed = sum(self.flows['case_filing'].history) * self.dt
        total_closed = self.stocks['closed_cases'].current_value
        
        # Calculate average cycle time (Little's Law approximation)
        avg_wip = sum(avg_stocks.values()) - avg_stocks['closed_cases']
        avg_throughput = total_closed / self.duration if self.duration > 0 else 0
        avg_cycle_time = avg_wip / avg_throughput if avg_throughput > 0 else 0
        
        # System efficiency
        system_efficiency = (total_closed / total_filed * 100) if total_filed > 0 else 0
        
        return {
            'simulation_type': 'system_dynamics',
            'duration': self.duration,
            'time_step': self.dt,
            'final_stocks': {
                name: stock.current_value for name, stock in self.stocks.items()
            },
            'average_stocks': avg_stocks,
            'metrics': {
                'total_cases_filed': total_filed,
                'total_cases_closed': total_closed,
                'average_cycle_time_days': avg_cycle_time,
                'system_efficiency_percent': system_efficiency,
                'average_work_in_progress': avg_wip
            },
            'stock_histories': {
                name: stock.history[-10:] for name, stock in self.stocks.items()
            },
            'flow_histories': {
                name: flow.history[-10:] for name, flow in self.flows.items()
            }
        }
    
    def get_time_series(self) -> Dict[str, List[float]]:
        """Get complete time series data for all stocks."""
        return {
            name: stock.history for name, stock in self.stocks.items()
        }


def run_system_dynamics_simulation(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run a system dynamics simulation with the given configuration."""
    if config is None:
        config = {}
    
    dt = config.get('dt', 1.0)
    duration = config.get('duration', 365.0)
    
    simulation = SystemDynamicsSimulation(dt, duration)
    
    # Apply custom parameters if provided
    if 'parameters' in config:
        for key, value in config['parameters'].items():
            simulation.set_parameter(key, value)
    
    results = simulation.run()
    
    return results


if __name__ == "__main__":
    # Run a sample simulation
    results = run_system_dynamics_simulation({'duration': 180.0})
    print(f"System efficiency: {results['metrics']['system_efficiency_percent']:.2f}%")

