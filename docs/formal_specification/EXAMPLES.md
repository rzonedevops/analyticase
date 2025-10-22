# Formal Specification Examples

This document provides practical examples of how the Z++ formal specification maps to implementation and usage.

## Table of Contents

1. [Basic Hypergraph Example](#basic-hypergraph-example)
2. [Legal Case Example](#legal-case-example)
3. [ZA Judiciary Integration Example](#za-judiciary-integration-example)
4. [Simulation Example](#simulation-example)
5. [Verification Example](#verification-example)

---

## Basic Hypergraph Example

### Formal Specification

From `SPECIFICATION.md`:

```
AddNode(node: Node)
  Pre-condition: node.nodeId not in domain(nodes)
  Post-condition:
    - nodes' = nodes ∪ {node.nodeId → node}
    - nodeToEdges' = nodeToEdges ∪ {node.nodeId → ∅}
    - hyperedges unchanged
```

### Python Implementation

```python
class Hypergraph:
    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}
        self.node_to_edges = {}
    
    def add_node(self, node):
        # Pre-condition check
        if node.node_id in self.nodes:
            raise ValueError(f"Node {node.node_id} already exists")
        
        # Operation
        self.nodes[node.node_id] = node
        self.node_to_edges[node.node_id] = set()
        
        # Post-condition is satisfied by design
```

### Usage Example

```python
# Create a hypergraph for a fraud case
graph = Hypergraph()

# Add nodes
suspect = Node(node_id="suspect_1", node_type="person", 
               attributes={"name": "John Doe"})
company = Node(node_id="company_1", node_type="organization",
               attributes={"name": "Acme Trust Co."})
transaction = Node(node_id="tx_001", node_type="event",
                   attributes={"amount": 100000, "date": "2025-01-15"})

graph.add_node(suspect)
graph.add_node(company)
graph.add_node(transaction)

# Verify post-conditions
assert suspect.node_id in graph.nodes
assert suspect.node_id in graph.node_to_edges
assert graph.node_to_edges[suspect.node_id] == set()

# Add hyperedge connecting them
edge = Hyperedge(
    edge_id="fraud_transaction",
    nodes={suspect.node_id, company.node_id, transaction.node_id},
    edge_type="transaction",
    weight=0.8,
    attributes={"suspicious": True}
)

graph.add_hyperedge(edge)

# Verify hypergraph consistency invariant
for node_id in graph.nodes:
    expected_edges = {
        e_id for e_id, e in graph.hyperedges.items()
        if node_id in e.nodes
    }
    assert graph.node_to_edges[node_id] == expected_edges

print(f"Graph has {len(graph.nodes)} nodes and {len(graph.hyperedges)} edges")
```

---

## Legal Case Example

### Formal Specification

From `SPECIFICATION.md`:

```
CreateCase(caseNum: CASENO, court: COURTCODE, type: CASETYPE,
           title: string, plaintiff: Party, defendant: Party)
  Pre-condition:
    - length(title) > 0
    - plaintiff.partyType = plaintiff
    - defendant.partyType = defendant
  Post-condition:
    - caseNumber' = caseNum
    - status' = filed
    - plaintiff.partyId and defendant.partyId in hypergraph.nodes
```

### Python Implementation

```python
class LegalCase:
    def __init__(self, case_id):
        self.case_id = case_id
        self.case_number = None
        self.court_code = None
        self.case_type = None
        self.title = None
        self.status = None
        self.filing_date = None
        self.plaintiff = None
        self.defendant = None
        self.hypergraph = Hypergraph()
        self.documents = set()
        self.events = []
    
    @classmethod
    def create_case(cls, case_number, court_code, case_type, title,
                    plaintiff, defendant):
        # Pre-condition checks
        if not title or len(title) == 0:
            raise ValueError("Title must be non-empty")
        if plaintiff.party_type != "plaintiff":
            raise ValueError("Plaintiff party type must be 'plaintiff'")
        if defendant.party_type != "defendant":
            raise ValueError("Defendant party type must be 'defendant'")
        
        # Create case
        case = cls(case_id=f"case_{case_number.replace(' ', '_')}")
        
        # Set attributes (post-conditions)
        case.case_number = case_number
        case.court_code = court_code
        case.case_type = case_type
        case.title = title
        case.status = "filed"
        case.filing_date = datetime.now()
        case.plaintiff = plaintiff
        case.defendant = defendant
        
        # Add parties to hypergraph
        plaintiff_node = Node(
            node_id=plaintiff.party_id,
            node_type="person",
            attributes={"name": plaintiff.name, "role": "plaintiff"}
        )
        defendant_node = Node(
            node_id=defendant.party_id,
            node_type="organization",
            attributes={"name": defendant.name, "role": "defendant"}
        )
        
        case.hypergraph.add_node(plaintiff_node)
        case.hypergraph.add_node(defendant_node)
        
        return case
```

### Usage Example

```python
# Create parties
plaintiff = Party(
    party_id="party_001",
    name="John Doe",
    party_type="plaintiff",
    contact_info={"email": "john@example.com"}
)

defendant = Party(
    party_id="party_002",
    name="Acme Trust Co.",
    party_type="defendant",
    contact_info={"email": "legal@acme.com"}
)

# Create case
case = LegalCase.create_case(
    case_number="(GP) 12345/2025",
    court_code="GP",
    case_type="civil",
    title="Trust Fraud Investigation",
    plaintiff=plaintiff,
    defendant=defendant
)

# Verify post-conditions
assert case.status == "filed"
assert case.case_number == "(GP) 12345/2025"
assert plaintiff.party_id in case.hypergraph.nodes
assert defendant.party_id in case.hypergraph.nodes

print(f"Created case: {case.title}")
print(f"Status: {case.status}")
print(f"Parties in graph: {len(case.hypergraph.nodes)}")
```

---

## ZA Judiciary Integration Example

### Formal Specification

From `SPECIFICATION.md`:

```
ValidateCaseNumber() returns boolean
  Returns: true if case.caseNumber matches pattern "(PREFIX) NUMBER/YEAR"

SubmitBundle() returns TIMESTAMP
  Pre-condition:
    - status = review
    - paginationComplete = true
    - redactionComplete = true
    - length(documents) > 0
  Post-condition:
    - status' = submitted
```

### Python Implementation

```python
import re
from datetime import datetime

class CourtOnlineCase:
    def __init__(self, case):
        self.case = case
        self.court_online_id = None
        self.e_filing_enabled = False
        self.e_filing_status = "disabled"
        self.filing_history = []
        self.digital_signature = None
    
    def validate_case_number(self):
        """Validate ZA case number format"""
        pattern = r'^\([A-Z]{2,3}\)\s*\d{4,6}\/\d{4}$'
        return bool(re.match(pattern, self.case.case_number))
    
    def enable_e_filing(self, signature):
        if self.e_filing_status == "suspended":
            raise ValueError("E-filing is suspended")
        if not signature or len(signature) == 0:
            raise ValueError("Digital signature required")
        
        self.e_filing_enabled = True
        self.e_filing_status = "enabled"
        self.digital_signature = signature
        return True

class CaseLinesBundle:
    def __init__(self, bundle_id, case_id, bundle_name, bundle_type):
        self.bundle_id = bundle_id
        self.case_id = case_id
        self.bundle_name = bundle_name
        self.bundle_type = bundle_type
        self.status = "draft"
        self.documents = []
        self.total_pages = 0
        self.pagination_complete = True
        self.redaction_complete = True
        self.created_at = datetime.now()
    
    def add_document(self, document):
        if document in self.documents:
            raise ValueError("Document already in bundle")
        
        self.documents.append(document)
        self.total_pages += document.page_count
        self.pagination_complete = (
            self.pagination_complete and document.paginated
        )
        self.redaction_complete = (
            self.redaction_complete and document.redacted
        )
    
    def submit_bundle(self):
        # Pre-condition checks
        if self.status != "review":
            raise ValueError(f"Cannot submit bundle with status {self.status}")
        if not self.pagination_complete:
            raise ValueError("Pagination not complete")
        if not self.redaction_complete:
            raise ValueError("Redaction not complete")
        if len(self.documents) == 0:
            raise ValueError("Cannot submit empty bundle")
        
        # Post-condition
        self.status = "submitted"
        submission_time = datetime.now()
        
        return submission_time
```

### Usage Example

```python
# Create Court Online case
case = LegalCase.create_case(
    case_number="(GP) 12345/2025",
    court_code="GP",
    case_type="civil",
    title="Trust Fraud Investigation",
    plaintiff=plaintiff,
    defendant=defendant
)

co_case = CourtOnlineCase(case)

# Validate case number
if co_case.validate_case_number():
    print("✓ Case number format is valid")
    
    # Enable e-filing
    co_case.enable_e_filing(signature="SHA256:abc123...")
    print(f"✓ E-filing enabled: {co_case.e_filing_enabled}")

# Create CaseLines bundle
bundle = CaseLinesBundle(
    bundle_id="bundle_001",
    case_id=case.case_id,
    bundle_name="Evidence Bundle 1",
    bundle_type="evidence"
)

# Add documents
doc1 = Document(
    document_id="doc_001",
    file_name="exhibit_a.pdf",
    file_type="pdf",
    page_count=10,
    paginated=True,
    redacted=True
)

doc2 = Document(
    document_id="doc_002",
    file_name="exhibit_b.pdf",
    file_type="pdf",
    page_count=5,
    paginated=True,
    redacted=True
)

bundle.add_document(doc1)
bundle.add_document(doc2)

print(f"Bundle has {len(bundle.documents)} documents")
print(f"Total pages: {bundle.total_pages}")

# Verify invariants before submission
assert bundle.total_pages == sum(d.page_count for d in bundle.documents)
assert bundle.pagination_complete == all(d.paginated for d in bundle.documents)
assert bundle.redaction_complete == all(d.redacted for d in bundle.documents)

# Submit bundle
bundle.status = "review"
submission_time = bundle.submit_bundle()

print(f"✓ Bundle submitted at {submission_time}")
print(f"✓ Final status: {bundle.status}")
```

---

## Simulation Example

### Formal Specification

From `SPECIFICATION.md`:

```
InitializeSimulation(type: SIMTYPE, config: JSONDATA)
  Post-condition:
    - simulationType' = type
    - status' = running
    - events' = empty sequence

AddSimulationEvent(event: SimulationEvent)
  Pre-condition:
    - status = running
    - event.eventId not in {e.eventId | e in events}
  Post-condition:
    - events' = events + event (append)
    - Temporal ordering maintained
```

### Python Implementation

```python
class SimulationRun:
    def __init__(self, run_id):
        self.run_id = run_id
        self.simulation_type = None
        self.configuration = None
        self.status = None
        self.agents = {}
        self.events = []
        self.results = None
        self.start_time = None
        self.end_time = None
    
    def initialize(self, simulation_type, configuration):
        self.simulation_type = simulation_type
        self.configuration = configuration
        self.status = "running"
        self.agents = {}
        self.events = []
        self.results = {}
        self.start_time = datetime.now()
    
    def add_event(self, event):
        # Pre-condition checks
        if self.status != "running":
            raise ValueError(f"Cannot add event: simulation is {self.status}")
        
        event_ids = {e.event_id for e in self.events}
        if event.event_id in event_ids:
            raise ValueError(f"Event {event.event_id} already exists")
        
        # Check temporal ordering
        if self.events and event.timestamp < self.events[-1].timestamp:
            raise ValueError(
                f"Event timestamp {event.timestamp} violates temporal ordering"
            )
        
        # Add event
        self.events.append(event)
    
    def complete(self, results):
        # Pre-condition
        if self.status != "running":
            raise ValueError(f"Cannot complete: simulation is {self.status}")
        if len(self.events) == 0:
            raise ValueError("Cannot complete simulation with no events")
        
        # Post-condition
        self.status = "completed"
        self.results = results
        self.end_time = datetime.now()
```

### Usage Example

```python
# Initialize simulation
sim = SimulationRun(run_id="sim_001")
sim.initialize(
    simulation_type="discrete_event",
    configuration={"num_cases": 100, "duration": 365}
)

print(f"Simulation {sim.run_id} initialized")
print(f"Type: {sim.simulation_type}")
print(f"Status: {sim.status}")

# Add agents
agent1 = Agent(
    agent_id="agent_001",
    agent_type="investigator",
    efficiency=0.85
)
agent2 = Agent(
    agent_id="agent_002",
    agent_type="attorney",
    efficiency=0.90
)

sim.agents[agent1.agent_id] = agent1
sim.agents[agent2.agent_id] = agent2

# Add events (must be temporally ordered)
event1 = SimulationEvent(
    event_id="event_001",
    event_type="filing",
    timestamp=0.0,
    case_id="case_001",
    involved_agents={agent1.agent_id},
    duration=1.0
)

event2 = SimulationEvent(
    event_id="event_002",
    event_type="hearing",
    timestamp=30.0,
    case_id="case_001",
    involved_agents={agent1.agent_id, agent2.agent_id},
    duration=2.0
)

event3 = SimulationEvent(
    event_id="event_003",
    event_type="ruling",
    timestamp=60.0,
    case_id="case_001",
    involved_agents={agent2.agent_id},
    duration=0.5
)

# Add events in order
sim.add_event(event1)
sim.add_event(event2)
sim.add_event(event3)

# Verify temporal ordering invariant
timestamps = [e.timestamp for e in sim.events]
assert timestamps == sorted(timestamps), "Temporal ordering violated!"

print(f"Added {len(sim.events)} events")

# Complete simulation
results = {
    "total_events": len(sim.events),
    "total_agents": len(sim.agents),
    "average_efficiency": sum(a.efficiency for a in sim.agents.values()) / len(sim.agents)
}

sim.complete(results)

print(f"Simulation completed: {sim.status}")
print(f"Duration: {sim.end_time - sim.start_time}")
print(f"Results: {sim.results}")
```

---

## Verification Example

### Verifying Hypergraph Consistency

```python
def verify_hypergraph_invariants(graph):
    """Verify all hypergraph invariants from formal specification"""
    
    errors = []
    
    # Invariant 1: domain(nodeToEdges) == domain(nodes)
    if set(graph.node_to_edges.keys()) != set(graph.nodes.keys()):
        errors.append("Node-to-edges index doesn't match nodes")
    
    # Invariant 2: For each edge, all nodes exist
    for edge_id, edge in graph.hyperedges.items():
        if not edge.nodes.issubset(graph.nodes.keys()):
            errors.append(f"Edge {edge_id} references non-existent nodes")
    
    # Invariant 3: nodeToEdges is consistent
    for node_id in graph.nodes.keys():
        expected_edges = {
            e_id for e_id, e in graph.hyperedges.items()
            if node_id in e.nodes
        }
        actual_edges = graph.node_to_edges[node_id]
        if expected_edges != actual_edges:
            errors.append(f"Node {node_id} has inconsistent edge index")
    
    if errors:
        raise AssertionError("Invariant violations:\n" + "\n".join(errors))
    
    return True

# Usage
graph = Hypergraph()
# ... build graph ...

try:
    verify_hypergraph_invariants(graph)
    print("✓ All hypergraph invariants satisfied")
except AssertionError as e:
    print(f"✗ Invariant violations detected:\n{e}")
```

### Property-Based Testing

Using `hypothesis` for property-based testing:

```python
from hypothesis import given, strategies as st

@given(
    dim=st.integers(min_value=1, max_value=256),
    num_nodes=st.integers(min_value=2, max_value=10)
)
def test_hypergraph_properties(dim, num_nodes):
    """Test hypergraph properties hold for any valid input"""
    graph = Hypergraph()
    
    # Add nodes
    nodes = []
    for i in range(num_nodes):
        node = Node(node_id=f"n{i}", node_type="person")
        node.initialize_embedding(dim)
        graph.add_node(node)
        nodes.append(node)
    
    # Property: All nodes in index
    assert len(graph.node_to_edges) == num_nodes
    
    # Add hyperedge
    edge = Hyperedge(
        edge_id="e1",
        nodes={n.node_id for n in nodes[:3]},
        edge_type="transaction"
    )
    graph.add_hyperedge(edge)
    
    # Property: Consistency maintained
    verify_hypergraph_invariants(graph)
    
    # Property: Statistics are correct
    stats = graph.get_statistics()
    assert stats['num_nodes'] == num_nodes
    assert stats['num_hyperedges'] == 1
```

### Runtime Invariant Checking

```python
def with_invariant_checking(cls):
    """Decorator to add invariant checking to all methods"""
    original_setattr = cls.__setattr__
    
    def checked_setattr(self, name, value):
        original_setattr(self, name, value)
        if hasattr(self, '_check_invariants'):
            self._check_invariants()
    
    cls.__setattr__ = checked_setattr
    return cls

@with_invariant_checking
class VerifiedHypergraph(Hypergraph):
    def _check_invariants(self):
        """Called after every attribute change"""
        if not hasattr(self, 'nodes'):
            return  # Still initializing
        
        verify_hypergraph_invariants(self)

# Usage
graph = VerifiedHypergraph()
# Any invariant violation will be caught immediately
```

---

## Summary

These examples demonstrate:

1. **Specification to Implementation**: How formal specifications translate to code
2. **Pre/Post-condition Checking**: Runtime validation of contracts
3. **Invariant Verification**: Ensuring system consistency
4. **Property-Based Testing**: Automated verification of properties
5. **Practical Usage**: Real-world application of the formal model

For complete formal specifications, see:
- `SPECIFICATION.md` - Full Z++ specification
- `VERIFICATION_CHECKLIST.md` - Detailed verification guide
- `NOTATION_GUIDE.md` - Z++ notation reference
