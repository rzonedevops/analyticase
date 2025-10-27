"""
Enhanced Discrete-Event Simulation Model for Legal Case Processing

This module implements an enhanced discrete-event simulation framework that tracks
legal principle applications, resource constraints, and process mining capabilities.

Version: 2.0
Enhancements:
- Legal principle tracking throughout case lifecycle
- Resource constraints (court capacity, attorney availability)
- Process mining integration for bottleneck identification
- Event dependencies and prerequisites
- Probabilistic event triggering based on case characteristics
- Performance metrics and optimization analysis
"""

import heapq
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import datetime
import random
from collections import defaultdict

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
    MOTION_FILED = "motion_filed"
    SETTLEMENT_NEGOTIATION = "settlement_negotiation"
    SETTLEMENT_REACHED = "settlement_reached"
    PRINCIPLE_INVOKED = "principle_invoked"
    PRECEDENT_CITED = "precedent_cited"


class CaseStatus(Enum):
    """Status of a case in the system."""
    FILED = "filed"
    DISCOVERY = "discovery"
    PRE_TRIAL = "pre_trial"
    TRIAL = "trial"
    RULING = "ruling"
    APPEAL = "appeal"
    SETTLEMENT = "settlement"
    CLOSED = "closed"


class CaseType(Enum):
    """Types of legal cases."""
    CONTRACT = "contract"
    DELICT = "delict"
    CRIMINAL = "criminal"
    CONSTITUTIONAL = "constitutional"
    ADMINISTRATIVE = "administrative"
    PROPERTY = "property"


class ResourceType(Enum):
    """Types of resources in the system."""
    JUDGE = "judge"
    ATTORNEY = "attorney"
    COURTROOM = "courtroom"
    CLERK = "clerk"


@dataclass(order=True)
class Event:
    """Represents a discrete event in the simulation."""
    time: float
    event_type: EventType = field(compare=False)
    case_id: str = field(compare=False)
    data: Dict[str, Any] = field(default_factory=dict, compare=False)
    prerequisites: Set[EventType] = field(default_factory=set, compare=False)
    
    def __repr__(self):
        return f"Event(time={self.time:.2f}, type={self.event_type.value}, case={self.case_id})"


@dataclass
class LegalPrincipleInvocation:
    """Tracks invocation of a legal principle in a case."""
    principle_name: str
    invocation_time: float
    invoked_by: str  # agent_id
    case_stage: CaseStatus
    success: bool
    confidence: float
    related_events: List[str] = field(default_factory=list)


@dataclass
class Case:
    """Enhanced case representation with legal principle tracking."""
    case_id: str
    case_number: str
    case_type: CaseType
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
    
    # Legal principle tracking
    principles_invoked: List[LegalPrincipleInvocation] = field(default_factory=list)
    precedents_cited: List[str] = field(default_factory=list)
    
    # Resource tracking
    assigned_judge: Optional[str] = None
    assigned_attorneys: List[str] = field(default_factory=list)
    
    # Outcome tracking
    outcome: Optional[str] = None
    settlement_amount: Optional[float] = None
    closure_time: Optional[float] = None
    
    def transition_to(self, new_status: CaseStatus, current_time: float):
        """Transition case to a new status."""
        if self.status != new_status:
            duration = current_time - self.current_stage_entry_time
            self.stage_durations[self.status.value] = duration
            self.status = new_status
            self.current_stage_entry_time = current_time
            logger.info(f"Case {self.case_number} transitioned to {new_status.value} at time {current_time:.2f}")
    
    def invoke_principle(self, invocation: LegalPrincipleInvocation):
        """Record invocation of a legal principle."""
        self.principles_invoked.append(invocation)
        logger.info(f"Principle {invocation.principle_name} invoked in case {self.case_number}")
    
    def cite_precedent(self, precedent_id: str):
        """Record citation of a precedent."""
        if precedent_id not in self.precedents_cited:
            self.precedents_cited.append(precedent_id)
    
    def get_total_duration(self) -> float:
        """Get total case duration."""
        if self.closure_time:
            return self.closure_time - self.filing_time
        return 0.0


@dataclass
class Resource:
    """Represents a resource in the system."""
    resource_id: str
    resource_type: ResourceType
    capacity: int = 1
    current_load: int = 0
    cases_assigned: List[str] = field(default_factory=list)
    availability_schedule: Dict[float, bool] = field(default_factory=dict)
    
    def is_available(self, time: float) -> bool:
        """Check if resource is available at a given time."""
        return self.current_load < self.capacity
    
    def assign_case(self, case_id: str, time: float) -> bool:
        """Assign a case to this resource."""
        if self.is_available(time):
            self.cases_assigned.append(case_id)
            self.current_load += 1
            return True
        return False
    
    def release_case(self, case_id: str):
        """Release a case from this resource."""
        if case_id in self.cases_assigned:
            self.cases_assigned.remove(case_id)
            self.current_load = max(0, self.current_load - 1)


class EventDependencyGraph:
    """Manages event dependencies and prerequisites."""
    
    def __init__(self):
        self.dependencies: Dict[EventType, Set[EventType]] = defaultdict(set)
        self._initialize_dependencies()
    
    def _initialize_dependencies(self):
        """Initialize standard event dependencies."""
        # Discovery must happen after case filing
        self.dependencies[EventType.DISCOVERY_COMPLETED] = {EventType.CASE_FILED}
        
        # Hearing requires discovery and evidence
        self.dependencies[EventType.HEARING_SCHEDULED] = {
            EventType.DISCOVERY_COMPLETED,
            EventType.EVIDENCE_SUBMITTED
        }
        
        # Hearing must be scheduled before conducted
        self.dependencies[EventType.HEARING_CONDUCTED] = {EventType.HEARING_SCHEDULED}
        
        # Ruling requires hearing
        self.dependencies[EventType.RULING_ISSUED] = {EventType.HEARING_CONDUCTED}
        
        # Case closure requires ruling or settlement
        self.dependencies[EventType.CASE_CLOSED] = {EventType.RULING_ISSUED}
    
    def get_prerequisites(self, event_type: EventType) -> Set[EventType]:
        """Get prerequisites for an event type."""
        return self.dependencies.get(event_type, set())
    
    def can_schedule_event(self, event_type: EventType, completed_events: Set[EventType]) -> bool:
        """Check if an event can be scheduled based on completed events."""
        prerequisites = self.get_prerequisites(event_type)
        return prerequisites.issubset(completed_events)


class DiscreteEventSimulation:
    """Enhanced discrete-event simulation engine with resource management."""
    
    def __init__(self, simulation_duration: float = 365.0, num_judges: int = 5,
                 num_attorneys: int = 20, num_courtrooms: int = 10):
        self.current_time: float = 0.0
        self.simulation_duration: float = simulation_duration
        self.event_queue: List[Event] = []
        self.cases: Dict[str, Case] = {}
        self.resources: Dict[str, Resource] = {}
        self.dependency_graph = EventDependencyGraph()
        
        # Track completed events per case
        self.case_completed_events: Dict[str, Set[EventType]] = defaultdict(set)
        
        # Statistics
        self.statistics: Dict[str, Any] = {
            'cases_filed': 0,
            'cases_closed': 0,
            'hearings_conducted': 0,
            'evidence_submitted': 0,
            'rulings_issued': 0,
            'settlements_reached': 0,
            'principles_invoked': 0,
            'precedents_cited': 0,
            'total_events': 0,
            'resource_utilization': defaultdict(list),
            'bottlenecks': []
        }
        
        # Process mining data
        self.event_log: List[Dict[str, Any]] = []
        self.case_variants: Dict[str, int] = defaultdict(int)
        
        # Initialize resources
        self._initialize_resources(num_judges, num_attorneys, num_courtrooms)
        
        logger.info(f"Initialized enhanced discrete-event simulation (duration: {simulation_duration} days)")
    
    def _initialize_resources(self, num_judges: int, num_attorneys: int, num_courtrooms: int):
        """Initialize system resources."""
        # Create judges
        for i in range(num_judges):
            self.resources[f"judge_{i}"] = Resource(
                resource_id=f"judge_{i}",
                resource_type=ResourceType.JUDGE,
                capacity=3  # Can handle 3 cases simultaneously
            )
        
        # Create attorneys
        for i in range(num_attorneys):
            self.resources[f"attorney_{i}"] = Resource(
                resource_id=f"attorney_{i}",
                resource_type=ResourceType.ATTORNEY,
                capacity=5  # Can handle 5 cases simultaneously
            )
        
        # Create courtrooms
        for i in range(num_courtrooms):
            self.resources[f"courtroom_{i}"] = Resource(
                resource_id=f"courtroom_{i}",
                resource_type=ResourceType.COURTROOM,
                capacity=1  # One case at a time
            )
    
    def schedule_event(self, event: Event):
        """Schedule an event in the event queue."""
        heapq.heappush(self.event_queue, event)
    
    def can_schedule_event(self, event: Event, case_id: str) -> bool:
        """Check if an event can be scheduled based on dependencies."""
        completed = self.case_completed_events[case_id]
        return self.dependency_graph.can_schedule_event(event.event_type, completed)
    
    def allocate_resource(self, resource_type: ResourceType, case_id: str) -> Optional[str]:
        """Allocate a resource of the specified type to a case."""
        available_resources = [
            r for r in self.resources.values()
            if r.resource_type == resource_type and r.is_available(self.current_time)
        ]
        
        if available_resources:
            # Select resource with lowest load
            resource = min(available_resources, key=lambda r: r.current_load)
            if resource.assign_case(case_id, self.current_time):
                return resource.resource_id
        
        return None
    
    def release_resource(self, resource_id: str, case_id: str):
        """Release a resource from a case."""
        if resource_id in self.resources:
            self.resources[resource_id].release_case(case_id)
    
    def generate_case_arrival(self, case_number: int) -> Event:
        """Generate a new case arrival event."""
        # Exponential inter-arrival time (average 2 days between cases)
        inter_arrival_time = random.expovariate(1.0 / 2.0)
        arrival_time = self.current_time + inter_arrival_time
        
        case_id = f"CASE-{case_number:05d}"
        case_num = f"(GP) {10000 + case_number}/2025"
        case_type = random.choice(list(CaseType))
        
        return Event(
            time=arrival_time,
            event_type=EventType.CASE_FILED,
            case_id=case_id,
            data={
                'case_number': case_num,
                'case_type': case_type,
                'priority': random.randint(1, 3),
                'complexity': random.randint(3, 10)
            }
        )
    
    def handle_case_filed(self, event: Event):
        """Handle a case filing event."""
        case = Case(
            case_id=event.case_id,
            case_number=event.data['case_number'],
            case_type=event.data['case_type'],
            filing_time=event.time,
            priority=event.data['priority'],
            complexity=event.data['complexity'],
            current_stage_entry_time=event.time
        )
        self.cases[event.case_id] = case
        self.statistics['cases_filed'] += 1
        self.case_completed_events[event.case_id].add(EventType.CASE_FILED)
        
        # Allocate judge and attorneys
        judge_id = self.allocate_resource(ResourceType.JUDGE, event.case_id)
        if judge_id:
            case.assigned_judge = judge_id
        
        attorney_id = self.allocate_resource(ResourceType.ATTORNEY, event.case_id)
        if attorney_id:
            case.assigned_attorneys.append(attorney_id)
        
        logger.info(f"Case filed: {case.case_number} at time {event.time:.2f}")
        
        # Log event for process mining
        self._log_event(event)
        
        # Schedule subsequent events based on case type and complexity
        self._schedule_case_events(case, event.time)
    
    def _schedule_case_events(self, case: Case, current_time: float):
        """Schedule events for a case based on its characteristics."""
        # Evidence submission (depends on complexity)
        evidence_delay = random.uniform(5, 15) * (case.complexity / 5)
        self.schedule_event(Event(
            time=current_time + evidence_delay,
            event_type=EventType.EVIDENCE_SUBMITTED,
            case_id=case.case_id,
            data={'evidence_items': random.randint(5, 20)}
        ))
        
        # Discovery completion
        discovery_delay = random.uniform(20, 60) * (case.complexity / 5)
        self.schedule_event(Event(
            time=current_time + discovery_delay,
            event_type=EventType.DISCOVERY_COMPLETED,
            case_id=case.case_id,
            data={}
        ))
        
        # Probabilistic settlement negotiation (higher for contract/civil cases)
        if case.case_type in [CaseType.CONTRACT, CaseType.DELICT]:
            if random.random() < 0.4:  # 40% chance of settlement attempt
                settlement_delay = random.uniform(30, 90)
                self.schedule_event(Event(
                    time=current_time + settlement_delay,
                    event_type=EventType.SETTLEMENT_NEGOTIATION,
                    case_id=case.case_id,
                    data={}
                ))
    
    def handle_evidence_submitted(self, event: Event):
        """Handle evidence submission event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        case.evidence_count += event.data.get('evidence_items', 1)
        self.statistics['evidence_submitted'] += 1
        self.case_completed_events[event.case_id].add(EventType.EVIDENCE_SUBMITTED)
        
        logger.info(f"Evidence submitted for case {case.case_number}: {case.evidence_count} items")
        self._log_event(event)
    
    def handle_discovery_completed(self, event: Event):
        """Handle discovery completion event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        case.transition_to(CaseStatus.PRE_TRIAL, event.time)
        self.case_completed_events[event.case_id].add(EventType.DISCOVERY_COMPLETED)
        
        logger.info(f"Discovery completed for case {case.case_number}")
        self._log_event(event)
        
        # Schedule hearing if prerequisites met
        if self.can_schedule_event(Event(time=0, event_type=EventType.HEARING_SCHEDULED, case_id=case.case_id), case.case_id):
            hearing_delay = random.uniform(10, 30)
            self.schedule_event(Event(
                time=event.time + hearing_delay,
                event_type=EventType.HEARING_SCHEDULED,
                case_id=case.case_id,
                data={}
            ))
    
    def handle_hearing_scheduled(self, event: Event):
        """Handle hearing scheduling event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        # Allocate courtroom
        courtroom_id = self.allocate_resource(ResourceType.COURTROOM, case.case_id)
        if not courtroom_id:
            # Reschedule if no courtroom available
            logger.warning(f"No courtroom available for case {case.case_number}, rescheduling")
            self.schedule_event(Event(
                time=event.time + random.uniform(5, 10),
                event_type=EventType.HEARING_SCHEDULED,
                case_id=case.case_id,
                data={}
            ))
            return
        
        case.hearings_scheduled += 1
        self.case_completed_events[event.case_id].add(EventType.HEARING_SCHEDULED)
        
        logger.info(f"Hearing scheduled for case {case.case_number} in {courtroom_id}")
        self._log_event(event)
        
        # Schedule hearing conduct
        hearing_delay = random.uniform(1, 5)
        self.schedule_event(Event(
            time=event.time + hearing_delay,
            event_type=EventType.HEARING_CONDUCTED,
            case_id=case.case_id,
            data={'courtroom': courtroom_id}
        ))
    
    def handle_hearing_conducted(self, event: Event):
        """Handle hearing conducted event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        case.transition_to(CaseStatus.TRIAL, event.time)
        self.statistics['hearings_conducted'] += 1
        self.case_completed_events[event.case_id].add(EventType.HEARING_CONDUCTED)
        
        # Release courtroom
        courtroom_id = event.data.get('courtroom')
        if courtroom_id:
            self.release_resource(courtroom_id, case.case_id)
        
        logger.info(f"Hearing conducted for case {case.case_number}")
        self._log_event(event)
        
        # Invoke legal principles during hearing
        self._invoke_principles_for_case(case, event.time)
        
        # Schedule ruling
        ruling_delay = random.uniform(5, 20)
        self.schedule_event(Event(
            time=event.time + ruling_delay,
            event_type=EventType.RULING_ISSUED,
            case_id=case.case_id,
            data={}
        ))
    
    def _invoke_principles_for_case(self, case: Case, time: float):
        """Invoke relevant legal principles for a case."""
        # Map case types to common principles
        principle_mapping = {
            CaseType.CONTRACT: ['pacta-sunt-servanda', 'consensus-ad-idem', 'bona-fides'],
            CaseType.DELICT: ['damnum-injuria-datum', 'culpa', 'causation'],
            CaseType.CRIMINAL: ['nullum-crimen-sine-lege', 'in-dubio-pro-reo'],
            CaseType.CONSTITUTIONAL: ['supremacy-of-constitution', 'rule-of-law'],
            CaseType.ADMINISTRATIVE: ['audi-alteram-partem', 'nemo-iudex-in-causa-sua'],
            CaseType.PROPERTY: ['nemo-plus-iuris', 'nemo-dat-quod-non-habet']
        }
        
        principles = principle_mapping.get(case.case_type, [])
        
        for principle_name in principles:
            if random.random() < 0.7:  # 70% chance of invoking each principle
                invocation = LegalPrincipleInvocation(
                    principle_name=principle_name,
                    invocation_time=time,
                    invoked_by=case.assigned_judge or "unknown",
                    case_stage=case.status,
                    success=random.random() < 0.8,  # 80% success rate
                    confidence=random.uniform(0.7, 0.95)
                )
                case.invoke_principle(invocation)
                self.statistics['principles_invoked'] += 1
                
                # Schedule principle invocation event
                self.schedule_event(Event(
                    time=time,
                    event_type=EventType.PRINCIPLE_INVOKED,
                    case_id=case.case_id,
                    data={'principle': principle_name}
                ))
    
    def handle_settlement_negotiation(self, event: Event):
        """Handle settlement negotiation event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        # Settlement success probability based on case complexity
        settlement_prob = 0.5 - (case.complexity / 20)
        
        if random.random() < settlement_prob:
            # Settlement reached
            case.transition_to(CaseStatus.SETTLEMENT, event.time)
            case.settlement_amount = random.uniform(10000, 1000000)
            self.statistics['settlements_reached'] += 1
            
            logger.info(f"Settlement reached for case {case.case_number}: R{case.settlement_amount:.2f}")
            self._log_event(event)
            
            # Schedule case closure
            self.schedule_event(Event(
                time=event.time + random.uniform(1, 5),
                event_type=EventType.CASE_CLOSED,
                case_id=case.case_id,
                data={'closure_reason': 'settlement'}
            ))
        else:
            logger.info(f"Settlement negotiation failed for case {case.case_number}")
    
    def handle_ruling_issued(self, event: Event):
        """Handle ruling issued event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        case.transition_to(CaseStatus.RULING, event.time)
        case.outcome = random.choice(['plaintiff', 'defendant'])
        self.statistics['rulings_issued'] += 1
        self.case_completed_events[event.case_id].add(EventType.RULING_ISSUED)
        
        logger.info(f"Ruling issued for case {case.case_number}: {case.outcome} wins")
        self._log_event(event)
        
        # Cite precedents
        num_precedents = random.randint(1, 5)
        for i in range(num_precedents):
            precedent_id = f"PRECEDENT-{random.randint(1, 100)}"
            case.cite_precedent(precedent_id)
            self.statistics['precedents_cited'] += 1
        
        # Schedule case closure
        closure_delay = random.uniform(1, 5)
        self.schedule_event(Event(
            time=event.time + closure_delay,
            event_type=EventType.CASE_CLOSED,
            case_id=case.case_id,
            data={'closure_reason': 'ruling'}
        ))
    
    def handle_case_closed(self, event: Event):
        """Handle case closure event."""
        case = self.cases.get(event.case_id)
        if not case:
            return
        
        case.transition_to(CaseStatus.CLOSED, event.time)
        case.closure_time = event.time
        self.statistics['cases_closed'] += 1
        self.case_completed_events[event.case_id].add(EventType.CASE_CLOSED)
        
        # Release resources
        if case.assigned_judge:
            self.release_resource(case.assigned_judge, case.case_id)
        for attorney_id in case.assigned_attorneys:
            self.release_resource(attorney_id, case.case_id)
        
        logger.info(f"Case closed: {case.case_number} (duration: {case.get_total_duration():.2f} days)")
        self._log_event(event)
        
        # Record case variant for process mining
        variant = self._get_case_variant(case)
        self.case_variants[variant] += 1
    
    def _get_case_variant(self, case: Case) -> str:
        """Get the process variant for a case (sequence of event types)."""
        event_sequence = [e.event_type.value for e in sorted(case.events, key=lambda x: x.time)]
        return " -> ".join(event_sequence)
    
    def _log_event(self, event: Event):
        """Log event for process mining."""
        case = self.cases.get(event.case_id)
        if case:
            case.events.append(event)
        
        self.event_log.append({
            'timestamp': event.time,
            'case_id': event.case_id,
            'event_type': event.event_type.value,
            'data': event.data
        })
        self.statistics['total_events'] += 1
    
    def run_simulation(self, num_cases: int = 100) -> Dict[str, Any]:
        """Run the simulation for a specified number of cases."""
        logger.info(f"Starting simulation with {num_cases} cases")
        
        # Generate initial case arrivals
        for i in range(num_cases):
            event = self.generate_case_arrival(i)
            if event.time < self.simulation_duration:
                self.schedule_event(event)
        
        # Process events
        while self.event_queue and self.current_time < self.simulation_duration:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            # Handle event based on type
            if event.event_type == EventType.CASE_FILED:
                self.handle_case_filed(event)
            elif event.event_type == EventType.EVIDENCE_SUBMITTED:
                self.handle_evidence_submitted(event)
            elif event.event_type == EventType.DISCOVERY_COMPLETED:
                self.handle_discovery_completed(event)
            elif event.event_type == EventType.HEARING_SCHEDULED:
                self.handle_hearing_scheduled(event)
            elif event.event_type == EventType.HEARING_CONDUCTED:
                self.handle_hearing_conducted(event)
            elif event.event_type == EventType.SETTLEMENT_NEGOTIATION:
                self.handle_settlement_negotiation(event)
            elif event.event_type == EventType.RULING_ISSUED:
                self.handle_ruling_issued(event)
            elif event.event_type == EventType.CASE_CLOSED:
                self.handle_case_closed(event)
            
            # Update resource utilization statistics
            if int(self.current_time) % 10 == 0:
                self._record_resource_utilization()
        
        logger.info(f"Simulation completed at time {self.current_time:.2f}")
        return self.get_simulation_results()
    
    def _record_resource_utilization(self):
        """Record resource utilization at current time."""
        for resource_id, resource in self.resources.items():
            utilization = resource.current_load / resource.capacity if resource.capacity > 0 else 0
            self.statistics['resource_utilization'][resource.resource_type.value].append(utilization)
    
    def get_simulation_results(self) -> Dict[str, Any]:
        """Get comprehensive simulation results."""
        # Calculate average case duration
        closed_cases = [c for c in self.cases.values() if c.status == CaseStatus.CLOSED]
        avg_duration = sum(c.get_total_duration() for c in closed_cases) / len(closed_cases) if closed_cases else 0
        
        # Calculate stage durations
        stage_durations = defaultdict(list)
        for case in closed_cases:
            for stage, duration in case.stage_durations.items():
                stage_durations[stage].append(duration)
        
        avg_stage_durations = {
            stage: sum(durations) / len(durations)
            for stage, durations in stage_durations.items()
        }
        
        # Resource utilization
        avg_resource_utilization = {
            resource_type: sum(utils) / len(utils) if utils else 0
            for resource_type, utils in self.statistics['resource_utilization'].items()
        }
        
        # Process mining insights
        top_variants = sorted(self.case_variants.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Principle invocation analysis
        principle_counts = defaultdict(int)
        for case in self.cases.values():
            for invocation in case.principles_invoked:
                principle_counts[invocation.principle_name] += 1
        
        return {
            'simulation_time': self.current_time,
            'statistics': dict(self.statistics),
            'cases_filed': self.statistics['cases_filed'],
            'cases_closed': self.statistics['cases_closed'],
            'avg_case_duration': avg_duration,
            'avg_stage_durations': avg_stage_durations,
            'resource_utilization': avg_resource_utilization,
            'top_process_variants': top_variants,
            'principle_invocations': dict(principle_counts),
            'settlement_rate': self.statistics['settlements_reached'] / self.statistics['cases_filed'] if self.statistics['cases_filed'] > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    sim = DiscreteEventSimulation(
        simulation_duration=365.0,
        num_judges=5,
        num_attorneys=20,
        num_courtrooms=10
    )
    
    results = sim.run_simulation(num_cases=100)
    
    print("\n=== Simulation Results ===")
    print(f"Cases Filed: {results['cases_filed']}")
    print(f"Cases Closed: {results['cases_closed']}")
    print(f"Average Case Duration: {results['avg_case_duration']:.2f} days")
    print(f"Settlement Rate: {results['settlement_rate']:.2%}")
    print(f"\nPrinciples Invoked: {results['principle_invocations']}")
    print(f"\nResource Utilization: {results['resource_utilization']}")

