#!/usr/bin/env python3
"""
Discrete-Event Simulation Model for Legal Case Processing

This module implements a discrete-event simulation framework for modeling
the flow of legal cases through various stages of the judicial system.
"""

import heapq
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import datetime
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events in the legal case processing system."""
    CASE_FILED = "case_filed"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    HEARING_SCHEDULED = "hearing_scheduled"
    HEARING_CONDUCTED = "hearing_conducted"
    RULING_ISSUED = "ruling_issued"
    APPEAL_FILED = "appeal_filed"
    CASE_CLOSED = "case_closed"
    DOCUMENT_FILED = "document_filed"
    DISCOVERY_COMPLETED = "discovery_completed"


class CaseStatus(Enum):
    """Status of a case in the system."""
    FILED = "filed"
    DISCOVERY = "discovery"
    PRE_TRIAL = "pre_trial"
    TRIAL = "trial"
    RULING = "ruling"
    APPEAL = "appeal"
    CLOSED = "closed"


@dataclass(order=True)
class Event:
    """Represents a discrete event in the simulation."""
    time: float
    event_type: EventType = field(compare=False)
    case_id: str = field(compare=False)
    data: Dict[str, Any] = field(default_factory=dict, compare=False)
    
    def __repr__(self):
        return f"Event(time={self.time}, type={self.event_type.value}, case={self.case_id})"


@dataclass
class Case:
    """Represents a legal case in the system."""
    case_id: str
    case_number: str
    filing_time: float
    status: CaseStatus = CaseStatus.FILED
    priority: int = 1
    complexity: int = 5
    evidence_count: int = 0
    hearings_scheduled: int = 0
    documents_filed: int = 0
    current_stage_entry_time: float = 0.0
    stage_durations: Dict[str, float] = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    
    def transition_to(self, new_status: CaseStatus, current_time: float):
        """Transition case to a new status."""
        if self.status != new_status:
            duration = current_time - self.current_stage_entry_time
            self.stage_durations[self.status.value] = duration
            self.status = new_status
            self.current_stage_entry_time = current_time
            logger.info(f"Case {self.case_number} transitioned to {new_status.value}")


class DiscreteEventSimulation:
    """Main discrete-event simulation engine for case processing."""
    
    def __init__(self, simulation_duration: float = 365.0):
        self.current_time: float = 0.0
        self.simulation_duration: float = simulation_duration
        self.event_queue: List[Event] = []
        self.cases: Dict[str, Case] = {}
        self.statistics: Dict[str, Any] = {
            'cases_filed': 0,
            'cases_closed': 0,
            'hearings_conducted': 0,
            'evidence_submitted': 0,
            'rulings_issued': 0,
            'total_events': 0
        }
        
        logger.info(f"Initialized discrete-event simulation (duration: {simulation_duration} days)")
    
    def schedule_event(self, event: Event):
        """Schedule an event in the event queue."""
        heapq.heappush(self.event_queue, event)
    
    def generate_case_arrival(self, case_number: int) -> Event:
        """Generate a new case arrival event."""
        # Exponential inter-arrival time (average 2 days between cases)
        inter_arrival_time = random.expovariate(1.0 / 2.0)
        arrival_time = self.current_time + inter_arrival_time
        
        case_id = f"CASE-{case_number:05d}"
        case_num = f"(GP) {10000 + case_number}/2025"
        
        return Event(
            time=arrival_time,
            event_type=EventType.CASE_FILED,
            case_id=case_id,
            data={
                'case_number': case_num,
                'priority': random.randint(1, 3),
                'complexity': random.randint(3, 10)
            }
        )
    
    def handle_case_filed(self, event: Event):
        """Handle a case filing event."""
        case = Case(
            case_id=event.case_id,
            case_number=event.data['case_number'],
            filing_time=event.time,
            priority=event.data['priority'],
            complexity=event.data['complexity'],
            current_stage_entry_time=event.time
        )
        self.cases[event.case_id] = case
        self.statistics['cases_filed'] += 1
        
        logger.info(f"Case filed: {case.case_number} at time {event.time:.2f}")
        
        # Schedule evidence submission
        evidence_time = event.time + random.uniform(5, 15)
        self.schedule_event(Event(
            time=evidence_time,
            event_type=EventType.EVIDENCE_SUBMITTED,
            case_id=event.case_id,
            data={'evidence_items': random.randint(5, 20)}
        ))
        
        # Schedule discovery completion
        discovery_time = event.time + random.uniform(20, 45)
        self.schedule_event(Event(
            time=discovery_time,
            event_type=EventType.DISCOVERY_COMPLETED,
            case_id=event.case_id
        ))
    
    def handle_evidence_submitted(self, event: Event):
        """Handle evidence submission event."""
        case = self.cases.get(event.case_id)
        if case:
            case.evidence_count += event.data.get('evidence_items', 1)
            self.statistics['evidence_submitted'] += event.data.get('evidence_items', 1)
            logger.info(f"Evidence submitted for {case.case_number}: {case.evidence_count} items")
    
    def handle_discovery_completed(self, event: Event):
        """Handle discovery completion event."""
        case = self.cases.get(event.case_id)
        if case and case.status == CaseStatus.FILED:
            case.transition_to(CaseStatus.DISCOVERY, event.time)
            
            # Schedule hearing
            hearing_time = event.time + random.uniform(15, 30)
            self.schedule_event(Event(
                time=hearing_time,
                event_type=EventType.HEARING_SCHEDULED,
                case_id=event.case_id
            ))
    
    def handle_hearing_scheduled(self, event: Event):
        """Handle hearing scheduling event."""
        case = self.cases.get(event.case_id)
        if case:
            case.transition_to(CaseStatus.PRE_TRIAL, event.time)
            case.hearings_scheduled += 1
            
            # Schedule hearing conduct
            hearing_conduct_time = event.time + random.uniform(10, 20)
            self.schedule_event(Event(
                time=hearing_conduct_time,
                event_type=EventType.HEARING_CONDUCTED,
                case_id=event.case_id
            ))
    
    def handle_hearing_conducted(self, event: Event):
        """Handle hearing conduct event."""
        case = self.cases.get(event.case_id)
        if case:
            case.transition_to(CaseStatus.TRIAL, event.time)
            self.statistics['hearings_conducted'] += 1
            
            logger.info(f"Hearing conducted for {case.case_number}")
            
            # Schedule ruling
            ruling_time = event.time + random.uniform(5, 15)
            self.schedule_event(Event(
                time=ruling_time,
                event_type=EventType.RULING_ISSUED,
                case_id=event.case_id
            ))
    
    def handle_ruling_issued(self, event: Event):
        """Handle ruling issuance event."""
        case = self.cases.get(event.case_id)
        if case:
            case.transition_to(CaseStatus.RULING, event.time)
            self.statistics['rulings_issued'] += 1
            
            logger.info(f"Ruling issued for {case.case_number}")
            
            # Decide if appeal is filed (20% probability)
            if random.random() < 0.2:
                appeal_time = event.time + random.uniform(10, 20)
                self.schedule_event(Event(
                    time=appeal_time,
                    event_type=EventType.APPEAL_FILED,
                    case_id=event.case_id
                ))
            else:
                # Close case
                close_time = event.time + random.uniform(2, 5)
                self.schedule_event(Event(
                    time=close_time,
                    event_type=EventType.CASE_CLOSED,
                    case_id=event.case_id
                ))
    
    def handle_appeal_filed(self, event: Event):
        """Handle appeal filing event."""
        case = self.cases.get(event.case_id)
        if case:
            case.transition_to(CaseStatus.APPEAL, event.time)
            
            logger.info(f"Appeal filed for {case.case_number}")
            
            # Schedule appeal hearing
            appeal_hearing_time = event.time + random.uniform(30, 60)
            self.schedule_event(Event(
                time=appeal_hearing_time,
                event_type=EventType.HEARING_CONDUCTED,
                case_id=event.case_id
            ))
    
    def handle_case_closed(self, event: Event):
        """Handle case closure event."""
        case = self.cases.get(event.case_id)
        if case:
            case.transition_to(CaseStatus.CLOSED, event.time)
            self.statistics['cases_closed'] += 1
            
            total_duration = event.time - case.filing_time
            logger.info(f"Case closed: {case.case_number} (duration: {total_duration:.2f} days)")
    
    def process_event(self, event: Event):
        """Process a single event."""
        self.current_time = event.time
        self.statistics['total_events'] += 1
        
        # Route event to appropriate handler
        handlers = {
            EventType.CASE_FILED: self.handle_case_filed,
            EventType.EVIDENCE_SUBMITTED: self.handle_evidence_submitted,
            EventType.DISCOVERY_COMPLETED: self.handle_discovery_completed,
            EventType.HEARING_SCHEDULED: self.handle_hearing_scheduled,
            EventType.HEARING_CONDUCTED: self.handle_hearing_conducted,
            EventType.RULING_ISSUED: self.handle_ruling_issued,
            EventType.APPEAL_FILED: self.handle_appeal_filed,
            EventType.CASE_CLOSED: self.handle_case_closed
        }
        
        handler = handlers.get(event.event_type)
        if handler:
            handler(event)
    
    def run(self, num_cases: int = 50) -> Dict[str, Any]:
        """Run the discrete-event simulation."""
        logger.info(f"Starting discrete-event simulation with {num_cases} cases")
        
        # Generate initial case arrivals
        for i in range(num_cases):
            event = self.generate_case_arrival(i + 1)
            if event.time <= self.simulation_duration:
                self.schedule_event(event)
        
        # Process events
        while self.event_queue and self.current_time <= self.simulation_duration:
            event = heapq.heappop(self.event_queue)
            if event.time <= self.simulation_duration:
                self.process_event(event)
        
        # Calculate final statistics
        results = self.calculate_results()
        
        logger.info(f"Simulation completed at time {self.current_time:.2f}")
        logger.info(f"Cases filed: {self.statistics['cases_filed']}, closed: {self.statistics['cases_closed']}")
        
        return results
    
    def calculate_results(self) -> Dict[str, Any]:
        """Calculate simulation results and statistics."""
        closed_cases = [c for c in self.cases.values() if c.status == CaseStatus.CLOSED]
        
        if closed_cases:
            avg_duration = sum(
                sum(c.stage_durations.values()) for c in closed_cases
            ) / len(closed_cases)
            
            avg_evidence = sum(c.evidence_count for c in closed_cases) / len(closed_cases)
        else:
            avg_duration = 0
            avg_evidence = 0
        
        # Calculate stage statistics
        stage_stats = {}
        for status in CaseStatus:
            cases_in_stage = [c for c in self.cases.values() if c.status == status]
            stage_stats[status.value] = {
                'count': len(cases_in_stage),
                'percentage': len(cases_in_stage) / len(self.cases) * 100 if self.cases else 0
            }
        
        return {
            'simulation_type': 'discrete_event',
            'simulation_duration': self.simulation_duration,
            'final_time': self.current_time,
            'statistics': self.statistics,
            'case_metrics': {
                'total_cases': len(self.cases),
                'closed_cases': len(closed_cases),
                'average_duration': avg_duration,
                'average_evidence_items': avg_evidence,
                'closure_rate': len(closed_cases) / len(self.cases) * 100 if self.cases else 0
            },
            'stage_distribution': stage_stats,
            'sample_cases': [
                {
                    'case_id': c.case_id,
                    'case_number': c.case_number,
                    'status': c.status.value,
                    'evidence_count': c.evidence_count,
                    'stage_durations': c.stage_durations
                }
                for c in list(self.cases.values())[:5]
            ]
        }


def run_discrete_event_simulation(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run a discrete-event simulation with the given configuration."""
    if config is None:
        config = {}
    
    simulation_duration = config.get('simulation_duration', 365.0)
    num_cases = config.get('num_cases', 50)
    
    simulation = DiscreteEventSimulation(simulation_duration)
    results = simulation.run(num_cases)
    
    return results


if __name__ == "__main__":
    # Run a sample simulation
    results = run_discrete_event_simulation({'num_cases': 30, 'simulation_duration': 180.0})
    print(f"Simulation completed: {results['case_metrics']['closed_cases']} cases closed")

