#!/usr/bin/env python3
"""
Enhanced System Dynamics Model for Legal Case Flow Analysis v2.2

This module implements an advanced system dynamics simulation framework for modeling
the flow and accumulation of cases through the judicial system using stock-and-flow
dynamics with legal principle integration.

Version: 2.2
Last Updated: 2025-11-02
Enhancements:
- Integration with Level 1 and Level 2 legal principles
- Principle-aware flow modulation
- Constitutional rights impact on case processing
- Multi-jurisdictional support
- Enhanced feedback loops and policy levers
- Temporal dynamics with seasonal and trend effects
- Resource constraint modeling
- Quality-of-justice metrics
"""

import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
import numpy as np
import datetime
import json
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalDomain(Enum):
    """Legal domain enumeration."""
    CIVIL = "civil"
    CRIMINAL = "criminal"
    ADMINISTRATIVE = "administrative"
    CONSTITUTIONAL = "constitutional"
    LABOUR = "labour"


class CaseStage(Enum):
    """Case processing stages."""
    FILED = "filed"
    PRELIMINARY = "preliminary"
    DISCOVERY = "discovery"
    TRIAL = "trial"
    JUDGMENT = "judgment"
    APPEAL = "appeal"
    CLOSED = "closed"


@dataclass
class LegalPrinciple:
    """Represents a legal principle affecting case dynamics."""
    name: str
    level: int  # 1 = first-order, 2 = meta-principle
    domain: List[str]
    confidence: float
    impact_on_processing: float  # Multiplier on processing rate
    impact_on_quality: float  # Impact on justice quality
    
    def applies_to_case(self, case_type: str, jurisdiction: str) -> bool:
        """Determine if principle applies to case."""
        return case_type in self.domain


@dataclass
class Stock:
    """Represents a stock (accumulation) in the system."""
    name: str
    initial_value: float
    current_value: float
    history: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update(self, net_flow: float, dt: float):
        """Update stock based on net flow."""
        self.current_value += net_flow * dt
        self.current_value = max(0, self.current_value)  # Prevent negative stocks
        self.history.append(self.current_value)
    
    def get_average(self, window: int = 10) -> float:
        """Get moving average of stock."""
        if len(self.history) < window:
            return np.mean(self.history) if self.history else self.current_value
        return np.mean(self.history[-window:])


@dataclass
class Flow:
    """Represents a flow (rate) in the system."""
    name: str
    rate: float
    history: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float],
                      principles: List[LegalPrinciple] = None) -> float:
        """Calculate flow rate based on stocks, parameters, and principles."""
        return self.rate
    
    def record(self):
        """Record current rate in history."""
        self.history.append(self.rate)


class CaseFilingFlow(Flow):
    """Flow representing new case filings with principle awareness."""
    
    def __init__(self, name: str, case_domain: LegalDomain):
        super().__init__(name, 0.0)
        self.case_domain = case_domain
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float],
                      principles: List[LegalPrinciple] = None) -> float:
        """Calculate case filing rate with seasonal and trend effects."""
        base_filing_rate = parameters.get('base_filing_rate', 2.0)
        seasonal_factor = parameters.get('seasonal_factor', 1.0)
        trend_factor = parameters.get('trend_factor', 1.0)
        
        # Access to justice principle impact
        access_to_justice_factor = 1.0
        if principles:
            for principle in principles:
                if principle.name == 'access-to-justice' and principle.applies_to_case(
                    self.case_domain.value, 'za'):
                    access_to_justice_factor *= (1 + principle.impact_on_processing)
        
        # Economic factors
        economic_factor = parameters.get('economic_factor', 1.0)
        
        # Add variability
        noise = np.random.normal(0, 0.1)
        
        self.rate = max(0, base_filing_rate * seasonal_factor * trend_factor * 
                       access_to_justice_factor * economic_factor * (1 + noise))
        return self.rate


class CaseProcessingFlow(Flow):
    """Flow representing case processing through stages with principle awareness."""
    
    def __init__(self, name: str, source_stock: str, processing_time: float,
                 stage: CaseStage):
        super().__init__(name, 0.0)
        self.source_stock = source_stock
        self.processing_time = processing_time
        self.stage = stage
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float],
                      principles: List[LegalPrinciple] = None) -> float:
        """Calculate processing rate with capacity constraints and principle impact."""
        source = stocks.get(self.source_stock)
        if not source or source.current_value == 0:
            self.rate = 0.0
            return self.rate
        
        # Base processing capacity
        capacity = parameters.get('processing_capacity', 10.0)
        efficiency = parameters.get('efficiency', 0.8)
        
        # Principle impact on processing
        principle_factor = 1.0
        if principles:
            for principle in principles:
                # Audi alteram partem (right to be heard) may slow processing but improve quality
                if principle.name == 'audi-alteram-partem':
                    principle_factor *= (1 + principle.impact_on_processing)
                # Procedural fairness requirements
                elif principle.name == 'procedural-fairness':
                    principle_factor *= (1 + principle.impact_on_processing)
        
        # Resource constraints
        resource_availability = parameters.get('resource_availability', 1.0)
        judge_capacity = parameters.get('judge_capacity', 1.0)
        
        # Backlog pressure (increases processing rate when backlog is high)
        backlog_pressure = min(2.0, 1 + (source.current_value / 100))
        
        # Rate limited by capacity, efficiency, and stock availability
        desired_rate = source.current_value / self.processing_time
        actual_rate = min(desired_rate, capacity * efficiency * resource_availability * 
                         judge_capacity * principle_factor * backlog_pressure)
        
        self.rate = max(0, actual_rate)
        return self.rate


class CaseClosureFlow(Flow):
    """Flow representing case closures with outcome tracking."""
    
    def __init__(self, name: str, source_stock: str, closure_time: float):
        super().__init__(name, 0.0)
        self.source_stock = source_stock
        self.closure_time = closure_time
        self.outcomes = {'settled': 0, 'judgment': 0, 'withdrawn': 0}
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float],
                      principles: List[LegalPrinciple] = None) -> float:
        """Calculate closure rate with settlement incentives."""
        source = stocks.get(self.source_stock)
        if not source or source.current_value == 0:
            self.rate = 0.0
            return self.rate
        
        # Base closure rate
        base_rate = source.current_value / self.closure_time
        
        # Settlement incentives
        settlement_factor = parameters.get('settlement_incentive', 1.0)
        
        # Alternative dispute resolution impact
        adr_factor = parameters.get('adr_availability', 1.0)
        
        # Principle impact (e.g., restorative justice encourages settlement)
        principle_factor = 1.0
        if principles:
            for principle in principles:
                if principle.name == 'restorative-justice':
                    principle_factor *= (1 + principle.impact_on_processing)
        
        self.rate = max(0, base_rate * settlement_factor * adr_factor * principle_factor)
        return self.rate


class AppealFlow(Flow):
    """Flow representing appeals with success rate tracking."""
    
    def __init__(self, name: str, source_stock: str, appeal_rate: float):
        super().__init__(name, 0.0)
        self.source_stock = source_stock
        self.appeal_rate = appeal_rate
        self.success_rate = 0.0
    
    def calculate_rate(self, stocks: Dict[str, Stock], parameters: Dict[str, float],
                      principles: List[LegalPrinciple] = None) -> float:
        """Calculate appeal filing rate."""
        source = stocks.get(self.source_stock)
        if not source or source.current_value == 0:
            self.rate = 0.0
            return self.rate
        
        # Base appeal rate (fraction of judgments appealed)
        base_rate = source.current_value * self.appeal_rate
        
        # Access to justice impact on appeals
        access_factor = parameters.get('appeal_access_factor', 1.0)
        
        # Cost of appeals
        cost_barrier = parameters.get('appeal_cost_barrier', 1.0)
        
        self.rate = max(0, base_rate * access_factor / cost_barrier)
        return self.rate


class EnhancedCaseDynamicsModel:
    """Enhanced system dynamics model for case flow with legal principle integration."""
    
    def __init__(self, jurisdiction: str = "za", domain: LegalDomain = LegalDomain.CIVIL):
        """Initialize the enhanced case dynamics model."""
        self.jurisdiction = jurisdiction
        self.domain = domain
        self.stocks: Dict[str, Stock] = {}
        self.flows: Dict[str, Flow] = {}
        self.principles: List[LegalPrinciple] = []
        self.parameters: Dict[str, float] = {}
        self.time = 0.0
        self.dt = 0.1  # Time step (e.g., 0.1 months)
        self.quality_metrics: List[float] = []
        
        logger.info(f"Initialized EnhancedCaseDynamicsModel for {jurisdiction} - {domain.value}")
    
    def add_stock(self, name: str, initial_value: float, metadata: Dict[str, Any] = None):
        """Add a stock to the model."""
        self.stocks[name] = Stock(name, initial_value, initial_value, [initial_value],
                                  metadata or {})
        logger.info(f"Added stock: {name} with initial value {initial_value}")
    
    def add_flow(self, flow: Flow):
        """Add a flow to the model."""
        self.flows[flow.name] = flow
        logger.info(f"Added flow: {flow.name}")
    
    def add_principle(self, principle: LegalPrinciple):
        """Add a legal principle affecting dynamics."""
        self.principles.append(principle)
        logger.info(f"Added principle: {principle.name} (Level {principle.level})")
    
    def set_parameter(self, name: str, value: float):
        """Set a model parameter."""
        self.parameters[name] = value
    
    def initialize_default_model(self):
        """Initialize a default case flow model."""
        # Stocks representing case stages
        self.add_stock('filed_cases', 50.0, {'stage': CaseStage.FILED.value})
        self.add_stock('preliminary_cases', 30.0, {'stage': CaseStage.PRELIMINARY.value})
        self.add_stock('discovery_cases', 20.0, {'stage': CaseStage.DISCOVERY.value})
        self.add_stock('trial_cases', 10.0, {'stage': CaseStage.TRIAL.value})
        self.add_stock('judgment_cases', 5.0, {'stage': CaseStage.JUDGMENT.value})
        self.add_stock('appeal_cases', 2.0, {'stage': CaseStage.APPEAL.value})
        self.add_stock('closed_cases', 0.0, {'stage': CaseStage.CLOSED.value})
        
        # Flows
        self.add_flow(CaseFilingFlow('case_filing', self.domain))
        self.add_flow(CaseProcessingFlow('preliminary_processing', 'filed_cases', 2.0,
                                        CaseStage.PRELIMINARY))
        self.add_flow(CaseProcessingFlow('discovery_processing', 'preliminary_cases', 3.0,
                                        CaseStage.DISCOVERY))
        self.add_flow(CaseProcessingFlow('trial_processing', 'discovery_cases', 4.0,
                                        CaseStage.TRIAL))
        self.add_flow(CaseProcessingFlow('judgment_processing', 'trial_cases', 1.0,
                                        CaseStage.JUDGMENT))
        self.add_flow(AppealFlow('appeal_filing', 'judgment_cases', 0.15))
        self.add_flow(CaseProcessingFlow('appeal_processing', 'appeal_cases', 6.0,
                                        CaseStage.APPEAL))
        self.add_flow(CaseClosureFlow('case_closure', 'judgment_cases', 0.5))
        
        # Default parameters
        self.set_parameter('base_filing_rate', 10.0)
        self.set_parameter('seasonal_factor', 1.0)
        self.set_parameter('trend_factor', 1.05)  # 5% annual growth
        self.set_parameter('processing_capacity', 15.0)
        self.set_parameter('efficiency', 0.75)
        self.set_parameter('resource_availability', 0.9)
        self.set_parameter('judge_capacity', 1.0)
        self.set_parameter('settlement_incentive', 1.2)
        self.set_parameter('adr_availability', 1.1)
        self.set_parameter('appeal_access_factor', 1.0)
        self.set_parameter('appeal_cost_barrier', 1.2)
        self.set_parameter('economic_factor', 1.0)
        
        # Add key legal principles
        self.add_principle(LegalPrinciple(
            'audi-alteram-partem', 1, ['civil', 'criminal', 'administrative'],
            1.0, -0.1, 0.3  # Slows processing by 10%, improves quality by 30%
        ))
        self.add_principle(LegalPrinciple(
            'procedural-fairness', 1, ['civil', 'criminal', 'administrative'],
            1.0, -0.05, 0.25
        ))
        self.add_principle(LegalPrinciple(
            'access-to-justice', 1, ['civil', 'criminal'],
            0.95, 0.15, 0.2  # Increases filing by 15%, improves quality by 20%
        ))
        self.add_principle(LegalPrinciple(
            'restorative-justice', 2, ['criminal'],
            0.85, 0.2, 0.15  # Increases settlement by 20%
        ))
    
    def step(self):
        """Execute one time step of the simulation."""
        # Calculate all flow rates
        for flow in self.flows.values():
            flow.calculate_rate(self.stocks, self.parameters, self.principles)
            flow.record()
        
        # Update stocks based on flows
        # Filed cases
        filing_rate = self.flows['case_filing'].rate
        preliminary_rate = self.flows['preliminary_processing'].rate
        self.stocks['filed_cases'].update(filing_rate - preliminary_rate, self.dt)
        
        # Preliminary cases
        discovery_rate = self.flows['discovery_processing'].rate
        self.stocks['preliminary_cases'].update(preliminary_rate - discovery_rate, self.dt)
        
        # Discovery cases
        trial_rate = self.flows['trial_processing'].rate
        self.stocks['discovery_cases'].update(discovery_rate - trial_rate, self.dt)
        
        # Trial cases
        judgment_rate = self.flows['judgment_processing'].rate
        self.stocks['trial_cases'].update(trial_rate - judgment_rate, self.dt)
        
        # Judgment cases
        appeal_rate = self.flows['appeal_filing'].rate
        closure_rate = self.flows['case_closure'].rate
        self.stocks['judgment_cases'].update(judgment_rate - appeal_rate - closure_rate, self.dt)
        
        # Appeal cases
        appeal_processing_rate = self.flows['appeal_processing'].rate
        self.stocks['appeal_cases'].update(appeal_rate - appeal_processing_rate, self.dt)
        
        # Closed cases
        self.stocks['closed_cases'].update(closure_rate + appeal_processing_rate, self.dt)
        
        # Calculate quality metrics
        quality = self.calculate_quality_metric()
        self.quality_metrics.append(quality)
        
        self.time += self.dt
    
    def calculate_quality_metric(self) -> float:
        """Calculate overall justice quality metric based on principles."""
        base_quality = 0.7  # Base quality score
        
        # Principle impact on quality
        for principle in self.principles:
            base_quality += principle.impact_on_quality * principle.confidence * 0.1
        
        # Backlog impact (high backlog reduces quality)
        total_pending = sum(self.stocks[s].current_value 
                          for s in ['filed_cases', 'preliminary_cases', 'discovery_cases',
                                   'trial_cases', 'judgment_cases', 'appeal_cases'])
        backlog_penalty = min(0.3, total_pending / 500)  # Max 30% penalty
        
        # Processing efficiency impact
        efficiency = self.parameters.get('efficiency', 0.75)
        efficiency_bonus = (efficiency - 0.5) * 0.2  # Up to 10% bonus
        
        quality = base_quality - backlog_penalty + efficiency_bonus
        return max(0.0, min(1.0, quality))  # Clamp to [0, 1]
    
    def run(self, duration: float, progress_callback: Optional[Callable] = None):
        """Run the simulation for specified duration."""
        steps = int(duration / self.dt)
        logger.info(f"Running simulation for {duration} time units ({steps} steps)")
        
        for i in range(steps):
            self.step()
            
            if progress_callback and i % 100 == 0:
                progress_callback(i, steps)
            
            # Log periodic updates
            if i % 100 == 0:
                total_pending = sum(self.stocks[s].current_value 
                                  for s in ['filed_cases', 'preliminary_cases', 'discovery_cases',
                                           'trial_cases', 'judgment_cases', 'appeal_cases'])
                logger.info(f"Step {i}/{steps}: Total pending = {total_pending:.1f}, "
                          f"Quality = {self.quality_metrics[-1]:.3f}")
        
        logger.info("Simulation complete")
    
    def get_results(self) -> Dict[str, Any]:
        """Get simulation results."""
        return {
            'stocks': {name: stock.history for name, stock in self.stocks.items()},
            'flows': {name: flow.history for name, flow in self.flows.items()},
            'quality_metrics': self.quality_metrics,
            'parameters': self.parameters,
            'principles': [{'name': p.name, 'level': p.level, 'confidence': p.confidence}
                          for p in self.principles],
            'final_state': {name: stock.current_value for name, stock in self.stocks.items()}
        }
    
    def export_results(self, filename: str):
        """Export results to JSON file."""
        results = self.get_results()
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results exported to {filename}")


def run_enhanced_simulation():
    """Run an enhanced case dynamics simulation."""
    logger.info("Starting Enhanced Case Dynamics Simulation v2.2")
    
    # Create model
    model = EnhancedCaseDynamicsModel(jurisdiction='za', domain=LegalDomain.CIVIL)
    model.initialize_default_model()
    
    # Run simulation for 120 time units (e.g., 10 years if dt=0.1 months)
    model.run(120.0)
    
    # Get and display results
    results = model.get_results()
    
    logger.info("\n=== Simulation Results ===")
    logger.info(f"Final case counts:")
    for stock_name, value in results['final_state'].items():
        logger.info(f"  {stock_name}: {value:.1f}")
    
    logger.info(f"\nAverage quality metric: {np.mean(results['quality_metrics']):.3f}")
    logger.info(f"Final quality metric: {results['quality_metrics'][-1]:.3f}")
    
    # Calculate throughput
    total_closed = results['final_state']['closed_cases']
    logger.info(f"\nTotal cases closed: {total_closed:.1f}")
    logger.info(f"Average throughput: {total_closed / 120:.2f} cases per time unit")
    
    # Export results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/home/ubuntu/analyticase/simulation_results/system_dynamics_enhanced_v2.2_{timestamp}.json"
    model.export_results(output_file)
    
    return model, results


if __name__ == "__main__":
    model, results = run_enhanced_simulation()
    logger.info("Enhanced System Dynamics simulation complete")
