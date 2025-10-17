# Quick Start Guide: Trust Fraud Case Study

Get started with the trust fraud case study in 5 minutes!

## Prerequisites

```bash
# Ensure you have Python 3.11 or higher and required dependencies
pip install -r requirements.txt
```

## 1. View the Case Data

```bash
# From the repository root directory
python case_studies/trust_fraud_analysis/case_data.py
```

**Expected Output:**
```
Case: Trust Fraud Analysis
Number of agents: 5
Number of events: 10
Number of hyperedges: 7

Agent Centrality Scores:
  BANTJIES (Central Orchestrator): 1.0
  RYNETTE (Revenue Coordinator): 0.46
  JACQUI (Signature Authority): 0.36
  PETER (Manipulated Puppet): 0.15
  DANIEL (Marginalized Whistleblower): -0.15
```

## 2. Run the Analysis

```bash
python case_studies/trust_fraud_analysis/analyze_case.py
```

This will:
- Build a hypergraph with 15 nodes and 7 hyperedges
- Train a HyperGNN model with 2 layers
- Detect 3 communities
- Analyze agent centrality
- Extract temporal patterns
- Generate comprehensive insights

**Analysis Runtime:** ~5-10 seconds

## 3. View the Visualization

### Option A: GitHub
Navigate to:
```
case_studies/trust_fraud_analysis/agent_centrality_graph.mmd
```

GitHub automatically renders Mermaid diagrams.

### Option B: Mermaid Live Editor
1. Copy the contents of `agent_centrality_graph.mmd`
2. Go to https://mermaid.live/
3. Paste and view

### Option C: VSCode
1. Install "Markdown Preview Mermaid Support" extension
2. Open `agent_centrality_graph.mmd`
3. Right-click → "Open Preview"

## 4. Review the Results

Check the generated analysis:
```bash
cat case_studies/trust_fraud_analysis/analysis_results.json
```

**Key Insights:**
- 3 distinct communities detected
- BANTJIES has maximum centrality (1.0)
- Payout motivation (R18M) has highest attention weight (1.0)
- Tight temporal coordination (24-48 hour response times)

## Understanding the Results

### Agent Hierarchy
```
BANTJIES (1.0) - Central orchestrator
    ├── RYNETTE (0.46) - Revenue coordinator
    ├── JACQUI (0.36) - Signature authority
    ├── PETER (0.15) - Manipulated puppet
    └── DANIEL (-0.15) - Marginalized whistleblower (isolated)
```

### Critical Patterns
1. **Financial Control**: BANTJIES → TRUSTEE → AUTHORITY → R18M (weight: 0.95)
2. **Whistleblower Suppression**: DANIEL → REPORTS → HOLIDAY → INTERDICT (weight: 0.87)
3. **Puppet Orchestration**: BANTJIES → PETER → CARDS/INTERDICT (weight: 0.85)

### Temporal Coordination
- Reports filed June 6 → Cards cancelled June 7 (24 hours)
- R10M identified June 10 AM → Dismissal June 10 PM (5 hours)
- Main trustee Aug 11 → Interdict Aug 13 (48 hours)

## Next Steps

### Explore the Code

**Case Data Structure:**
```python
from case_studies.trust_fraud_analysis import get_case_data

data = get_case_data()
print(data['agents'])      # List of agents
print(data['events'])      # List of events
print(data['relationships']) # Hyperedges
print(data['narratives'])  # Hidden narratives
```

**Access Specific Data:**
```python
from case_studies.trust_fraud_analysis import (
    get_centrality_scores,
    get_attention_weights,
    get_agent_by_id
)

# Get all centrality scores
scores = get_centrality_scores()

# Get attention weights for hyperedges
weights = get_attention_weights()

# Get specific agent data
bantjies = get_agent_by_id('BANTJIES')
print(bantjies['role'])  # "Central Orchestrator"
```

### Customize the Analysis

Edit `analyze_case.py` to:
- Change HyperGNN hyperparameters
- Adjust number of communities
- Add new analysis functions
- Export results in different formats

Example:
```python
# Change model configuration
model = HyperGNN(input_dim=128, hidden_dim=64, num_layers=3)

# Detect more communities
communities = model.detect_communities(hypergraph, num_communities=5)
```

### Modify the Visualization

Edit `agent_centrality_graph.mmd` to:
- Change colors (edit `classDef` statements)
- Add new nodes or edges
- Adjust subgraph groupings
- Change layout direction (`TB`, `LR`, `RL`, `BT`)

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'numpy'"
**Solution:**
```bash
pip install numpy
```

### Issue: Diagram doesn't render on GitHub
**Solution:**
- Clear browser cache
- Use Mermaid Live Editor instead
- Check file extension is `.mmd`

### Issue: Analysis takes too long
**Solution:**
- Reduce `num_layers` in HyperGNN initialization
- Reduce `input_dim` and `hidden_dim`
- Reduce number of communities to detect

## Documentation

- **Full Documentation**: See `README.md`
- **Visualization Guide**: See `VISUALIZATION_GUIDE.md`
- **HyperGNN Model**: See `../../models/hyper_gnn/README.md`

## Support

For questions or issues:
1. Check the documentation files
2. Review the code comments
3. Open an issue on GitHub

---

**Estimated Time to Complete:** 5-10 minutes

**Difficulty Level:** Beginner to Intermediate

**What You'll Learn:**
- HyperGNN model usage
- Agent centrality analysis
- Temporal pattern detection
- Mermaid diagram visualization
- Hypergraph data structures
