# Implementation Verification Checklist

This checklist helps verify that the AnalytiCase implementation conforms to the Z++ formal specification.

## Table of Contents

1. [Core Data Structures](#core-data-structures)
2. [Legal Case Management](#legal-case-management)
3. [ZA Judiciary Integration](#za-judiciary-integration)
4. [Simulation Models](#simulation-models)
5. [Analysis Operations](#analysis-operations)
6. [System Invariants](#system-invariants)

---

## Core Data Structures

### Node Class

**File:** `models/hyper_gnn/hypergnn_model.py::Node`

- [ ] **Attributes**
  - [ ] `nodeId` exists and is unique
  - [ ] `nodeType` is from valid set of types
  - [ ] `attributes` can store arbitrary JSON data
  - [ ] `embedding` is a sequence/array of real numbers
  - [ ] `embeddingDim` is tracked

- [ ] **Invariants**
  - [ ] `embeddingDim > 0` when embedding is initialized
  - [ ] `length(embedding) == embeddingDim`
  - [ ] All embedding values are in range [-1.0, 1.0]

- [ ] **Operations**
  - [ ] `InitializeNodeEmbedding(dim)` creates embedding of correct size
  - [ ] Embedding initialization doesn't change other attributes

**Test Cases:**
```python
def test_node_embedding_initialization():
    node = Node(nodeId="n1", nodeType="person")
    node.initialize_embedding(dim=64)
    assert len(node.embeddings) == 64
    assert all(-1.0 <= e <= 1.0 for e in node.embeddings)
```

---

### Hyperedge Class

**File:** `models/hyper_gnn/hypergnn_model.py::Hyperedge`

- [ ] **Attributes**
  - [ ] `edgeId` exists and is unique
  - [ ] `nodes` is a set/collection of node IDs
  - [ ] `edgeType` is from valid set of types
  - [ ] `weight` is a real number
  - [ ] `attributes` can store arbitrary JSON data
  - [ ] `attentionWeights` maps node IDs to weights (optional)

- [ ] **Invariants**
  - [ ] `size(nodes) >= 2` (at least two nodes)
  - [ ] `0 <= weight <= 1`
  - [ ] If `attentionWeights` exists:
    - [ ] Keys are subset of `nodes`
    - [ ] All weights in range [0, 1]
    - [ ] Sum of weights equals 1.0

- [ ] **Operations**
  - [ ] `AddNodeToHyperedge(node, attWeight)` validates inputs
  - [ ] Node addition updates both `nodes` and `attentionWeights`
  - [ ] Cannot add duplicate nodes

**Test Cases:**
```python
def test_hyperedge_node_addition():
    edge = Hyperedge(edgeId="e1", nodes={"n1", "n2"}, edgeType="transaction")
    initial_size = len(edge.nodes)
    edge.add_node("n3", 0.33)
    assert len(edge.nodes) == initial_size + 1
    assert "n3" in edge.nodes
```

---

### Hypergraph Class

**File:** `models/hyper_gnn/hypergnn_model.py::Hypergraph`

- [ ] **Attributes**
  - [ ] `nodes` maps node IDs to Node objects
  - [ ] `hyperedges` maps edge IDs to Hyperedge objects
  - [ ] `nodeToEdges` maps node IDs to sets of edge IDs

- [ ] **Invariants**
  - [ ] `domain(nodeToEdges) == domain(nodes)`
  - [ ] For each node `n`: `nodeToEdges[n] == {e | n in hyperedges[e].nodes}`
  - [ ] For each edge `e`: `hyperedges[e].nodes ⊆ domain(nodes)`
  - [ ] No orphaned nodes or edges

- [ ] **Operations**
  - [ ] `AddNode(node)` validates uniqueness
  - [ ] `AddNode(node)` initializes empty edge set
  - [ ] `AddHyperedge(edge)` validates all nodes exist
  - [ ] `AddHyperedge(edge)` updates `nodeToEdges` for all nodes
  - [ ] `GetNodeNeighbors(nodeId)` returns correct neighbors
  - [ ] `HypergraphStatistics()` computes correct metrics

**Test Cases:**
```python
def test_hypergraph_consistency():
    graph = Hypergraph()
    node1 = Node(nodeId="n1", nodeType="person")
    node2 = Node(nodeId="n2", nodeType="organization")
    
    graph.add_node(node1)
    graph.add_node(node2)
    
    edge = Hyperedge(edgeId="e1", nodes={"n1", "n2"}, edgeType="transaction")
    graph.add_hyperedge(edge)
    
    # Verify consistency
    assert "n1" in graph.node_to_edges
    assert "e1" in graph.node_to_edges["n1"]
    assert "e1" in graph.node_to_edges["n2"]
```

---

## Legal Case Management

### Party Class

**File:** Implementation-dependent

- [ ] **Attributes**
  - [ ] `partyId` unique identifier
  - [ ] `name` is non-empty string
  - [ ] `partyType` from {plaintiff, defendant, witness, expert}
  - [ ] `contactInfo` stores contact data
  - [ ] `legalRepresentation` is set of node IDs

- [ ] **Invariants**
  - [ ] `length(name) > 0`

---

### LegalCase Class

**File:** Implementation-dependent (likely in case management module)

- [ ] **Attributes**
  - [ ] `caseId` unique identifier
  - [ ] `caseNumber` court case number
  - [ ] `courtCode` court identifier
  - [ ] `caseType` from valid case types
  - [ ] `title` non-empty string
  - [ ] `status` from valid statuses
  - [ ] `filingDate` timestamp
  - [ ] `plaintiff` Party object
  - [ ] `defendant` Party object
  - [ ] `hypergraph` Hypergraph instance
  - [ ] `documents` set of file paths
  - [ ] `events` sequence of event IDs

- [ ] **Invariants**
  - [ ] `length(title) > 0`
  - [ ] `plaintiff.partyType == "plaintiff"`
  - [ ] `defendant.partyType == "defendant"`
  - [ ] `plaintiff.partyId in hypergraph.nodes`
  - [ ] `defendant.partyId in hypergraph.nodes`

- [ ] **Operations**
  - [ ] `CreateCase(...)` initializes all required fields
  - [ ] `CreateCase(...)` sets status to "filed"
  - [ ] `CreateCase(...)` adds plaintiff and defendant to hypergraph
  - [ ] `UpdateCaseStatus(newStatus)` validates transition
  - [ ] `AddDocument(document)` prevents duplicates

**Test Cases:**
```python
def test_case_creation():
    plaintiff = Party(name="John Doe", partyType="plaintiff")
    defendant = Party(name="Acme Corp", partyType="defendant")
    
    case = LegalCase.create_case(
        caseNumber="(GP) 12345/2025",
        courtCode="GP",
        caseType="civil",
        title="Breach of Contract",
        plaintiff=plaintiff,
        defendant=defendant
    )
    
    assert case.status == "filed"
    assert plaintiff.partyId in case.hypergraph.nodes
    assert defendant.partyId in case.hypergraph.nodes
```

---

## ZA Judiciary Integration

### CourtOnlineCase Class

**File:** `za_judiciary_integration/api/za_judiciary_api.py::CourtOnlineCase`

- [ ] **Attributes**
  - [ ] `case` LegalCase instance
  - [ ] `courtOnlineId` non-empty string
  - [ ] `eFilingEnabled` boolean
  - [ ] `eFilingStatus` from {enabled, disabled, suspended}
  - [ ] `filingHistory` sequence of timestamps
  - [ ] `digitalSignature` string

- [ ] **Invariants**
  - [ ] `length(courtOnlineId) > 0`
  - [ ] `eFilingEnabled == true iff eFilingStatus == "enabled"`
  - [ ] `case.status in {filed, pending, active} implies length(filingHistory) > 0`

- [ ] **Operations**
  - [ ] `ValidateCaseNumber()` checks format "(PREFIX) NUMBER/YEAR"
  - [ ] Prefix is 2-3 uppercase letters
  - [ ] Number is 4-6 digits
  - [ ] Year is 4 digits
  - [ ] `EnableEFiling(signature)` validates status
  - [ ] `EnableEFiling(signature)` requires non-empty signature

**Test Cases:**
```python
def test_case_number_validation():
    valid_numbers = ["(GP) 12345/2025", "(WCC) 123456/2024", "(GJ) 1234/2025"]
    invalid_numbers = ["GP12345/2025", "(GP)12345/2025", "(GP) 12/2025"]
    
    for num in valid_numbers:
        assert validate_case_number(num) == True
    
    for num in invalid_numbers:
        assert validate_case_number(num) == False
```

---

### CaseLinesBundle Class

**File:** `za_judiciary_integration/api/za_judiciary_api.py::CaseLinesBundle`

- [ ] **Attributes**
  - [ ] `bundleId` unique identifier
  - [ ] `caseId` case reference
  - [ ] `bundleName` non-empty string
  - [ ] `bundleType` from valid bundle types
  - [ ] `status` from valid bundle statuses
  - [ ] `documents` sequence of Documents
  - [ ] `totalPages` natural number
  - [ ] `paginationComplete` boolean
  - [ ] `redactionComplete` boolean
  - [ ] `createdAt` timestamp

- [ ] **Invariants**
  - [ ] `length(bundleName) > 0`
  - [ ] `totalPages == sum(doc.pageCount for doc in documents)`
  - [ ] `paginationComplete iff all(doc.paginated for doc in documents)`
  - [ ] `redactionComplete iff all(doc.redacted for doc in documents)`
  - [ ] `status == "accepted" implies paginationComplete and redactionComplete`

- [ ] **Operations**
  - [ ] `AddDocumentToBundle(doc)` prevents duplicates
  - [ ] `AddDocumentToBundle(doc)` updates totalPages
  - [ ] `AddDocumentToBundle(doc)` updates completion flags
  - [ ] `SubmitBundle()` requires status == "review"
  - [ ] `SubmitBundle()` requires paginationComplete and redactionComplete
  - [ ] `SubmitBundle()` requires non-empty documents

**Test Cases:**
```python
def test_bundle_submission_requirements():
    bundle = CaseLinesBundle(bundleName="Evidence", bundleType="evidence")
    
    # Cannot submit empty bundle
    with pytest.raises(ValidationError):
        bundle.submit()
    
    # Add document but not paginated/redacted
    doc = Document(fileName="test.pdf", pageCount=10, paginated=False, redacted=False)
    bundle.add_document(doc)
    
    # Still cannot submit
    with pytest.raises(ValidationError):
        bundle.submit()
    
    # Complete pagination and redaction
    doc.paginated = True
    doc.redacted = True
    bundle.status = "review"
    
    # Now can submit
    bundle.submit()
    assert bundle.status == "submitted"
```

---

## Simulation Models

### Agent Class

**File:** `models/agent_based/*.py`

- [ ] **Attributes**
  - [ ] `agentId` unique identifier
  - [ ] `agentType` from valid agent types
  - [ ] `workload` natural number
  - [ ] `efficiency` real number
  - [ ] `interactions` set of agent IDs
  - [ ] `caseAssignments` set of case IDs

- [ ] **Invariants**
  - [ ] `0 <= efficiency <= 1`
  - [ ] `agentId not in interactions` (cannot interact with self)

- [ ] **Operations**
  - [ ] `AssignCase(case)` prevents duplicate assignments
  - [ ] `AssignCase(case)` increments workload
  - [ ] `RecordInteraction(other)` validates other != self
  - [ ] `RecordInteraction(other)` prevents duplicate interactions

---

### SimulationRun Class

**File:** `simulations/*.py`

- [ ] **Attributes**
  - [ ] `runId` unique identifier
  - [ ] `simulationType` from valid simulation types
  - [ ] `startTime` timestamp
  - [ ] `endTime` timestamp
  - [ ] `configuration` JSON data
  - [ ] `agents` map of agent ID to Agent
  - [ ] `events` sequence of SimulationEvent
  - [ ] `results` JSON data
  - [ ] `status` from {running, completed, failed}

- [ ] **Invariants**
  - [ ] `status == "completed" implies length(events) > 0`
  - [ ] Events are temporally ordered: `events[i].timestamp <= events[i+1].timestamp`

- [ ] **Operations**
  - [ ] `InitializeSimulation(type, config)` sets status to "running"
  - [ ] `AddSimulationEvent(event)` validates status == "running"
  - [ ] `AddSimulationEvent(event)` prevents duplicate event IDs
  - [ ] `AddSimulationEvent(event)` maintains temporal ordering
  - [ ] `CompleteSimulation(results)` requires non-empty events
  - [ ] `CompleteSimulation(results)` sets status to "completed"

**Test Cases:**
```python
def test_event_temporal_ordering():
    sim = SimulationRun(simulationType="discrete_event")
    sim.initialize()
    
    event1 = SimulationEvent(eventId="e1", timestamp=10.0)
    event2 = SimulationEvent(eventId="e2", timestamp=5.0)
    
    sim.add_event(event1)
    
    # Adding event with earlier timestamp should fail or be inserted correctly
    try:
        sim.add_event(event2)
        # If insertion is allowed, verify ordering
        timestamps = [e.timestamp for e in sim.events]
        assert timestamps == sorted(timestamps)
    except ValidationError:
        # Alternatively, may reject out-of-order events
        pass
```

---

## Analysis Operations

### Community Detection

- [ ] `DetectCommunities(algorithm)` requires non-empty graph
- [ ] Returns disjoint communities
- [ ] Union of communities equals all nodes
- [ ] At least 1 community returned

### Centrality Analysis

- [ ] `ComputeCentrality(nodeId, metric)` validates node exists
- [ ] Returns value in range [0, 1]
- [ ] Different metrics supported

### Temporal Pattern Detection

- [ ] `DetectTemporalPatterns(timeWindow)` validates timeWindow > 0
- [ ] All patterns have length >= 2
- [ ] Confidence in range [0, 1]

### Link Prediction

- [ ] `PredictLinks(source, target, method)` validates nodes exist
- [ ] Validates source != target
- [ ] Returns probability in range [0, 1]

---

## System Invariants

### Hypergraph Consistency

Run this check after every graph operation:

```python
def verify_hypergraph_consistency(graph):
    # All nodes in nodeToEdges
    assert set(graph.node_to_edges.keys()) == set(graph.nodes.keys())
    
    # All edge nodes exist
    for edge_id, edge in graph.hyperedges.items():
        assert edge.nodes.issubset(graph.nodes.keys())
    
    # nodeToEdges is correct
    for node_id in graph.nodes.keys():
        expected_edges = {
            e_id for e_id, e in graph.hyperedges.items()
            if node_id in e.nodes
        }
        assert graph.node_to_edges[node_id] == expected_edges
```

### Case Status Transitions

Valid transitions:
```python
VALID_TRANSITIONS = {
    "filed": {"pending", "active", "archived"},
    "pending": {"active", "closed", "archived"},
    "active": {"closed", "archived"},
    "closed": {"archived"},
    "archived": {"archived"}  # Terminal state
}

def validate_status_transition(current, new):
    return new in VALID_TRANSITIONS[current]
```

### Bundle Submission Rules

```python
def can_submit_bundle(bundle):
    return (
        bundle.status == "review" and
        bundle.paginationComplete and
        bundle.redactionComplete and
        len(bundle.documents) > 0
    )
```

### Event Temporal Ordering

```python
def verify_event_ordering(events):
    timestamps = [e.timestamp for e in events]
    assert timestamps == sorted(timestamps)
```

---

## Verification Tools

### Automated Testing

Create property-based tests using hypothesis:

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=128))
def test_node_embedding_dimension(dim):
    node = Node(nodeId="n1", nodeType="person")
    node.initialize_embedding(dim)
    assert len(node.embeddings) == dim
```

### Runtime Invariant Checking

Add assertions to implementation:

```python
class Hypergraph:
    def add_node(self, node):
        self._check_invariants()  # Before
        # ... implementation ...
        self._check_invariants()  # After
    
    def _check_invariants(self):
        assert set(self.node_to_edges.keys()) == set(self.nodes.keys())
        # ... other invariants ...
```

### Static Analysis

Use type checking:

```python
from typing import Dict, Set
from dataclasses import dataclass

@dataclass
class Hypergraph:
    nodes: Dict[str, Node]
    hyperedges: Dict[str, Hyperedge]
    node_to_edges: Dict[str, Set[str]]
```

---

## Verification Status

Track verification progress:

| Component | Implementation | Invariants | Operations | Tests | Status |
|-----------|---------------|------------|------------|-------|--------|
| Node | ✓ | ✓ | ✓ | ✓ | Complete |
| Hyperedge | ✓ | ✓ | ✓ | ✓ | Complete |
| Hypergraph | ✓ | ✓ | ✓ | ✓ | Complete |
| LegalCase | ✓ | ✓ | ✓ | ⚠ | Partial |
| CourtOnlineCase | ✓ | ✓ | ✓ | ⚠ | Partial |
| CaseLinesBundle | ✓ | ✓ | ✓ | ⚠ | Partial |
| Agent | ✓ | ✓ | ✓ | ⚠ | Partial |
| SimulationRun | ✓ | ✓ | ✓ | ⚠ | Partial |

Legend:
- ✓ Complete
- ⚠ Partial
- ✗ Not implemented
- - Not applicable

---

## Continuous Verification

1. **CI/CD Integration**: Run verification tests on every commit
2. **Coverage Tracking**: Ensure all invariants are tested
3. **Regression Testing**: Prevent violations of previously verified properties
4. **Documentation**: Keep this checklist updated with implementation changes

## References

- See `SPECIFICATION.md` for detailed formal specification
- See `NOTATION_GUIDE.md` for Z++ notation explanations
- See `README.md` for overview and compilation instructions
