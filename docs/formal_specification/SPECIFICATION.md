# AnalytiCase Z++ Formal Specification (Markdown Version)

> **Note**: This is a simplified Markdown version of the formal specification. For the complete LaTeX version with full mathematical notation, see `analyticase_zpp_spec.tex`.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Types](#basic-types)
3. [Core Data Structures](#core-data-structures)
4. [Legal Case Management](#legal-case-management)
5. [ZA Judiciary Integration](#za-judiciary-integration)
6. [Simulation Models](#simulation-models)
7. [Analysis Operations](#analysis-operations)
8. [System Invariants](#system-invariants)
9. [Examples](#examples)

## Introduction

This document provides a formal specification of the AnalytiCase system using Z++, an object-oriented extension of the Z notation. The specification defines the core data structures, operations, and invariants that govern the system's behavior.

### Purpose

- Formally define core data structures and operations
- Specify pre-conditions, post-conditions, and invariants
- Document state transitions and system behaviors
- Provide a rigorous foundation for implementation verification

### Scope

- Core hypergraph data structures
- Legal case management
- ZA Judiciary integration (Court Online and CaseLines)
- Simulation models and execution
- Analysis operations

## Basic Types

### Given Sets

```
CASEID, NODEID, EDGEID, AGENTID, EVENTID, RUNID, BUNDLEID
TIMESTAMP, FILEPATH, COURTCODE, CASENO, JSONDATA
```

### Enumerated Types

**Node Types:**
```
NODETYPE ::= person | organization | event | document | evidence | court
```

**Edge Types:**
```
EDGETYPE ::= transaction | communication | attendance | ownership | relationship
```

**Case Status:**
```
CASESTATUS ::= filed | pending | active | closed | archived
```

**Case Type:**
```
CASETYPE ::= civil | criminal | commercial | constitutional
```

**Agent Type:**
```
AGENTTYPE ::= investigator | attorney | judge | clerk
```

**Simulation Type:**
```
SIMTYPE ::= agent_based | discrete_event | system_dynamics | hypergnn | case_llm
```

**Bundle Type:**
```
BUNDLETYPE ::= pleadings | evidence | correspondence | orders
```

**Bundle Status:**
```
BUNDLESTATUS ::= draft | review | submitted | accepted
```

## Core Data Structures

### Node Class

Represents an entity in the hypergraph with attributes and embeddings.

**State:**
- `nodeId: NODEID` - Unique identifier
- `nodeType: NODETYPE` - Type of node
- `attributes: JSONDATA` - Additional attributes
- `embedding: sequence of real numbers` - Vector embedding
- `embeddingDim: natural number` - Dimension of embedding

**Invariants:**
- `embeddingDim > 0`
- `length(embedding) = embeddingDim`
- `all values in embedding are in range [-1.0, 1.0]`

**Operations:**

```
InitializeNodeEmbedding(dim: natural number)
  Pre-condition: dim > 0
  Post-condition: 
    - embeddingDim' = dim
    - length(embedding') = dim
    - nodeId, nodeType, attributes unchanged
```

### Hyperedge Class

Connects multiple nodes with a specific relationship type and weight.

**State:**
- `edgeId: EDGEID` - Unique identifier
- `nodes: set of NODEID` - Connected nodes
- `edgeType: EDGETYPE` - Type of relationship
- `weight: real number` - Edge weight
- `attributes: JSONDATA` - Additional attributes
- `attentionWeights: map from NODEID to real` - Attention mechanism weights

**Invariants:**
- `size(nodes) >= 2` - At least two nodes
- `0 <= weight <= 1` - Weight normalized
- `domain(attentionWeights) ⊆ nodes` - Weights only for edge nodes
- `all attention weights in range [0, 1]`
- `sum of all attention weights = 1.0` - Normalized attention

**Operations:**

```
AddNodeToHyperedge(node: NODEID, attWeight: real)
  Pre-condition:
    - node not in nodes
    - 0 <= attWeight <= 1
  Post-condition:
    - nodes' = nodes ∪ {node}
    - attentionWeights' = attentionWeights ∪ {node → attWeight}
    - edgeId, edgeType, weight, attributes unchanged
```

### Hypergraph Class

Manages the complete graph structure with nodes and hyperedges.

**State:**
- `nodes: map from NODEID to Node` - All nodes
- `hyperedges: map from EDGEID to Hyperedge` - All hyperedges
- `nodeToEdges: map from NODEID to set of EDGEID` - Node-to-edge index

**Invariants:**
- `domain(nodeToEdges) = domain(nodes)` - Index covers all nodes
- For each node n: `nodeToEdges(n) = {e | n ∈ hyperedges(e).nodes}`
- For each edge e: `hyperedges(e).nodes ⊆ domain(nodes)` - All edge nodes exist

**Operations:**

```
AddNode(node: Node)
  Pre-condition: node.nodeId not in domain(nodes)
  Post-condition:
    - nodes' = nodes ∪ {node.nodeId → node}
    - nodeToEdges' = nodeToEdges ∪ {node.nodeId → ∅}
    - hyperedges unchanged

AddHyperedge(edge: Hyperedge)
  Pre-condition:
    - edge.edgeId not in domain(hyperedges)
    - edge.nodes ⊆ domain(nodes)
  Post-condition:
    - hyperedges' = hyperedges ∪ {edge.edgeId → edge}
    - For each n in edge.nodes: nodeToEdges'(n) = nodeToEdges(n) ∪ {edge.edgeId}
    - nodes unchanged

GetNodeNeighbors(nodeId: NODEID) returns set of NODEID
  Pre-condition: nodeId in domain(nodes)
  Returns: union of (hyperedges(e).nodes \ {nodeId}) for all e in nodeToEdges(nodeId)

HypergraphStatistics() returns statistics
  Returns:
    - numNodes: number of nodes
    - numEdges: number of hyperedges
    - avgNodeDegree: average number of edges per node
    - maxNodeDegree: maximum node degree
    - avgEdgeSize: average number of nodes per edge
    - maxEdgeSize: maximum edge size
```

## Legal Case Management

### Party Class

**State:**
- `partyId: NODEID` - Unique identifier
- `name: string` - Party name
- `partyType: {plaintiff, defendant, witness, expert}` - Role
- `contactInfo: JSONDATA` - Contact information
- `legalRepresentation: set of NODEID` - Representatives

**Invariants:**
- `length(name) > 0`

### LegalCase Class

**State:**
- `caseId: CASEID` - Unique identifier
- `caseNumber: CASENO` - Court case number
- `courtCode: COURTCODE` - Court identifier
- `caseType: CASETYPE` - Type of case
- `title: string` - Case title
- `status: CASESTATUS` - Current status
- `filingDate: TIMESTAMP` - When filed
- `plaintiff: Party` - Plaintiff information
- `defendant: Party` - Defendant information
- `hypergraph: Hypergraph` - Case relationship graph
- `documents: set of FILEPATH` - Attached documents
- `events: sequence of EVENTID` - Case events

**Invariants:**
- `length(title) > 0`
- `plaintiff.partyType = plaintiff`
- `defendant.partyType = defendant`
- `plaintiff.partyId in domain(hypergraph.nodes)`
- `defendant.partyId in domain(hypergraph.nodes)`

**Operations:**

```
CreateCase(caseNum: CASENO, court: COURTCODE, type: CASETYPE,
           title: string, plaintiff: Party, defendant: Party)
  Pre-condition:
    - length(title) > 0
    - plaintiff.partyType = plaintiff
    - defendant.partyType = defendant
  Post-condition:
    - caseNumber' = caseNum
    - courtCode' = court
    - caseType' = type
    - title' = title
    - status' = filed
    - plaintiff' = plaintiff
    - defendant' = defendant
    - documents' = ∅
    - events' = empty sequence
    - hypergraph'.nodes = {plaintiff.partyId → plaintiff, defendant.partyId → defendant}
    - hypergraph'.hyperedges = ∅

UpdateCaseStatus(newStatus: CASESTATUS)
  Pre-condition: newStatus is a valid transition from current status
  Post-condition:
    - status' = newStatus
    - All other fields unchanged

AddDocument(document: FILEPATH)
  Pre-condition: document not in documents
  Post-condition:
    - documents' = documents ∪ {document}
    - caseId, caseNumber, status, hypergraph, events unchanged
```

## ZA Judiciary Integration

### CourtOnlineCase Class

**State:**
- `case: LegalCase` - Underlying case
- `courtOnlineId: string` - Court Online system ID
- `eFilingEnabled: boolean` - E-filing status
- `eFilingStatus: {enabled, disabled, suspended}` - Detailed status
- `filingHistory: sequence of TIMESTAMP` - Filing timestamps
- `digitalSignature: string` - Signature for e-filing

**Invariants:**
- `length(courtOnlineId) > 0`
- `eFilingEnabled = true iff eFilingStatus = enabled`
- `case.status in {filed, pending, active} implies length(filingHistory) > 0`

**Operations:**

```
ValidateCaseNumber() returns boolean
  Returns: true if case.caseNumber matches pattern "(PREFIX) NUMBER/YEAR"
    where:
      - PREFIX is 2-3 uppercase letters
      - NUMBER is 4-6 digits
      - YEAR is 4 digits

EnableEFiling(signature: string)
  Pre-condition:
    - eFilingStatus ≠ suspended
    - length(signature) > 0
  Post-condition:
    - eFilingEnabled' = true
    - eFilingStatus' = enabled
    - digitalSignature' = signature
    - case, courtOnlineId unchanged
```

### Document Class

**State:**
- `documentId: NODEID` - Unique identifier
- `fileName: string` - File name
- `fileType: {pdf, docx, txt, image}` - File format
- `pageCount: natural number` - Number of pages
- `filePath: FILEPATH` - Location
- `uploadDate: TIMESTAMP` - When uploaded
- `redacted: boolean` - Redaction complete
- `paginated: boolean` - Pagination complete

**Invariants:**
- `length(fileName) > 0`
- `pageCount > 0`

### CaseLinesBundle Class

**State:**
- `bundleId: BUNDLEID` - Unique identifier
- `caseId: CASEID` - Associated case
- `bundleName: string` - Bundle name
- `bundleType: BUNDLETYPE` - Type of bundle
- `status: BUNDLESTATUS` - Current status
- `documents: sequence of Document` - Bundled documents
- `totalPages: natural number` - Total page count
- `paginationComplete: boolean` - All documents paginated
- `redactionComplete: boolean` - All documents redacted
- `createdAt: TIMESTAMP` - Creation time

**Invariants:**
- `length(bundleName) > 0`
- `totalPages = sum of pageCount for all documents`
- `paginationComplete iff all documents are paginated`
- `redactionComplete iff all documents are redacted`
- `status = accepted implies paginationComplete and redactionComplete`

**Operations:**

```
AddDocumentToBundle(doc: Document)
  Pre-condition: doc not in documents
  Post-condition:
    - documents' = documents + doc (append)
    - totalPages' = totalPages + doc.pageCount
    - paginationComplete' = paginationComplete and doc.paginated
    - redactionComplete' = redactionComplete and doc.redacted
    - bundleId, bundleName, bundleType, status unchanged

SubmitBundle() returns TIMESTAMP
  Pre-condition:
    - status = review
    - paginationComplete = true
    - redactionComplete = true
    - length(documents) > 0
  Post-condition:
    - status' = submitted
    - bundleId, documents, totalPages unchanged
  Returns: submission timestamp
```

## Simulation Models

### Agent Class

**State:**
- `agentId: AGENTID` - Unique identifier
- `agentType: AGENTTYPE` - Role type
- `workload: natural number` - Current workload
- `efficiency: real number` - Performance metric
- `interactions: set of AGENTID` - Interacted agents
- `caseAssignments: set of CASEID` - Assigned cases

**Invariants:**
- `0 <= efficiency <= 1`
- `agentId not in interactions` - Cannot interact with self

**Operations:**

```
AssignCase(case: CASEID)
  Pre-condition: case not in caseAssignments
  Post-condition:
    - caseAssignments' = caseAssignments ∪ {case}
    - workload' = workload + 1
    - agentId, agentType, efficiency, interactions unchanged

RecordInteraction(other: AGENTID)
  Pre-condition:
    - other ≠ agentId
    - other not in interactions
  Post-condition:
    - interactions' = interactions ∪ {other}
    - agentId, agentType, workload, efficiency, caseAssignments unchanged
```

### SimulationEvent Class

**State:**
- `eventId: EVENTID` - Unique identifier
- `eventType: {filing, hearing, ruling, closure}` - Event type
- `timestamp: real number` - Simulation time
- `caseId: CASEID` - Associated case
- `involvedAgents: set of AGENTID` - Participating agents
- `duration: real number` - Event duration
- `outcome: JSONDATA` - Event result

**Invariants:**
- `timestamp >= 0`
- `duration > 0`
- `size(involvedAgents) > 0`

### SimulationRun Class

**State:**
- `runId: RUNID` - Unique identifier
- `simulationType: SIMTYPE` - Type of simulation
- `startTime: TIMESTAMP` - Start time
- `endTime: TIMESTAMP` - End time
- `configuration: JSONDATA` - Simulation parameters
- `agents: map from AGENTID to Agent` - All agents
- `events: sequence of SimulationEvent` - All events
- `results: JSONDATA` - Simulation results
- `status: {running, completed, failed}` - Current status

**Invariants:**
- `status = completed implies length(events) > 0`
- Events are temporally ordered: for all i < j: `events(i).timestamp <= events(j).timestamp`

**Operations:**

```
InitializeSimulation(type: SIMTYPE, config: JSONDATA)
  Post-condition:
    - simulationType' = type
    - configuration' = config
    - status' = running
    - agents' = ∅
    - events' = empty sequence
    - results' = {}

AddSimulationEvent(event: SimulationEvent)
  Pre-condition:
    - status = running
    - event.eventId not in {e.eventId | e in events}
  Post-condition:
    - events' = events + event (append)
    - runId, simulationType, status, agents unchanged

CompleteSimulation(results: JSONDATA)
  Pre-condition:
    - status = running
    - length(events) > 0
  Post-condition:
    - status' = completed
    - results' = results
    - runId, simulationType, agents, events unchanged
```

## Analysis Operations

### Community Detection

```
DetectCommunities(algorithm: {louvain, spectral, label_propagation})
  returns set of (set of NODEID)
  
  Pre-condition: size(nodes) > 0
  Post-condition:
    - Union of all communities = domain(nodes)
    - Communities are disjoint (no overlap)
    - At least 1 community
```

### Centrality Analysis

```
ComputeCentrality(nodeId: NODEID,
                  metric: {degree, betweenness, closeness, eigenvector})
  returns real number
  
  Pre-condition: nodeId in domain(nodes)
  Post-condition: result in range [0, 1]
```

### Temporal Pattern Detection

```
DetectTemporalPatterns(timeWindow: real) 
  returns (patterns: set of sequences, confidence: real)
  
  Pre-condition: timeWindow > 0
  Post-condition:
    - All patterns have length >= 2
    - 0 <= confidence <= 1
```

### Link Prediction

```
PredictLinks(sourceNode: NODEID, targetNode: NODEID,
             method: {common_neighbors, jaccard, adamic_adar, preferential_attachment})
  returns real number (probability)
  
  Pre-condition:
    - sourceNode in domain(nodes)
    - targetNode in domain(nodes)
    - sourceNode ≠ targetNode
  Post-condition: result in range [0, 1]
```

## System Invariants

### Hypergraph Consistency

For all Hypergraph instances:
1. All nodes have entries in nodeToEdges index
2. All hyperedge nodes exist in the node set
3. nodeToEdges mapping is consistent with actual edges

**Formal statement:**
```
For all n in domain(nodes):
  n in domain(nodeToEdges)

For all e in domain(hyperedges):
  hyperedges(e).nodes ⊆ domain(nodes)

For all n in domain(nodes):
  nodeToEdges(n) = {e in domain(hyperedges) | n in hyperedges(e).nodes}
```

### Case Status Transitions

Valid state transitions for LegalCase:

```
filed → {pending, active, archived}
pending → {active, closed, archived}
active → {closed, archived}
closed → {archived}
archived → {archived} (terminal)
```

### Bundle Submission Rules

For CaseLinesBundle to be submitted:

```
status = submitted implies:
  - paginationComplete = true
  - redactionComplete = true
  - length(documents) > 0
```

### Simulation Event Ordering

For all SimulationRun instances:

```
For all indices i, j where i < j:
  events(i).timestamp <= events(j).timestamp
```

## Examples

### Example 1: Creating a Trust Fraud Case

```
Input:
  plaintiff = Party(name="John Doe", partyType=plaintiff)
  defendant = Party(name="Acme Trust Co.", partyType=defendant)
  caseNum = "(GP) 12345/2025"
  court = "GP"
  type = civil
  title = "Trust Fraud Investigation"

Operation: CreateCase(caseNum, court, type, title, plaintiff, defendant)

Result:
  caseNumber = "(GP) 12345/2025"
  status = filed
  hypergraph.nodes = {plaintiff.partyId, defendant.partyId}
  documents = ∅
  events = empty sequence
```

### Example 2: Building a Hypergraph

```
Starting with empty Hypergraph:

Step 1: AddNode(Node(nodeId=n1, nodeType=person))
  Result: nodes = {n1 → Node1}

Step 2: AddNode(Node(nodeId=n2, nodeType=organization))
  Result: nodes = {n1 → Node1, n2 → Node2}

Step 3: AddNode(Node(nodeId=n3, nodeType=document))
  Result: nodes = {n1 → Node1, n2 → Node2, n3 → Node3}

Step 4: AddHyperedge(Hyperedge(edgeId=e1, nodes={n1, n2}, edgeType=transaction))
  Result: 
    hyperedges = {e1 → Edge1}
    nodeToEdges(n1) = {e1}
    nodeToEdges(n2) = {e1}

Step 5: AddHyperedge(Hyperedge(edgeId=e2, nodes={n1, n2, n3}, edgeType=ownership))
  Result:
    hyperedges = {e1 → Edge1, e2 → Edge2}
    nodeToEdges(n1) = {e1, e2}
    nodeToEdges(n2) = {e1, e2}
    nodeToEdges(n3) = {e2}

Final Statistics:
  numNodes = 3
  numEdges = 2
  avgNodeDegree = 5/3 ≈ 1.67
  maxNodeDegree = 2
  avgEdgeSize = 2.5
  maxEdgeSize = 3
```

### Example 3: CaseLines Bundle Workflow

```
Initial state:
  bundle = CaseLinesBundle(
    bundleName = "Evidence Bundle 1",
    bundleType = evidence,
    status = draft,
    documents = empty
  )

Step 1: AddDocumentToBundle(Document(fileName="exhibit_a.pdf", pageCount=10, 
                                       paginated=true, redacted=true))
  Result:
    documents = [Doc1]
    totalPages = 10
    paginationComplete = true
    redactionComplete = true

Step 2: AddDocumentToBundle(Document(fileName="exhibit_b.pdf", pageCount=5,
                                       paginated=true, redacted=false))
  Result:
    documents = [Doc1, Doc2]
    totalPages = 15
    paginationComplete = true
    redactionComplete = false  // Doc2 not redacted

// Cannot submit yet because redactionComplete = false

Step 3: Update Doc2 to set redacted = true
  Result:
    redactionComplete = true

Step 4: Update status to review
  Result: status = review

Step 5: SubmitBundle()
  Pre-conditions satisfied:
    ✓ status = review
    ✓ paginationComplete = true
    ✓ redactionComplete = true
    ✓ documents not empty
  
  Result:
    status = submitted
    Returns: submission timestamp
```

## Conclusion

This formal specification provides a rigorous mathematical foundation for the AnalytiCase system. It can be used for:

- **Implementation verification**: Ensure code matches the specification
- **Test generation**: Derive test cases from pre/post-conditions
- **Documentation**: Provide precise, unambiguous definitions
- **Formal reasoning**: Prove properties about the system
- **Maintenance**: Guide future enhancements with clear contracts

For the complete specification with full mathematical notation, see the LaTeX version: `analyticase_zpp_spec.tex`

## References

1. Spivey, J. M. (1992). *The Z Notation: A Reference Manual*. Prentice Hall.
2. Duke, R., Rose, G., & Smith, G. (1995). *Object-Z: A Specification Language*. Computer Standards & Interfaces.
3. Potter, B., Sinclair, J., & Till, D. (1996). *An Introduction to Formal Specification and Z*. Prentice Hall.
