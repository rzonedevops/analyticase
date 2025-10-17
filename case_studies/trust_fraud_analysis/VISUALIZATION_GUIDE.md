# Visualization Guide: Agent Centrality Graph

## Overview

The agent centrality graph visualization (`agent_centrality_graph.mmd`) is a Mermaid diagram that provides a comprehensive view of the trust fraud case, showing:

- **Agents** with centrality scores
- **Key events** with timestamps
- **Hypergraph edges** with attention weights
- **Hidden narratives** as subgraphs
- **Temporal relationships** and causal chains

## Viewing the Diagram

### Option 1: GitHub (Recommended)

Simply view the file on GitHub:
```
https://github.com/rzonedevops/analyticase/blob/copilot/create-agent-centrality-graph/case_studies/trust_fraud_analysis/agent_centrality_graph.mmd
```

GitHub automatically renders Mermaid diagrams in `.mmd` files.

### Option 2: Mermaid Live Editor

1. Go to https://mermaid.live/
2. Copy the contents of `agent_centrality_graph.mmd`
3. Paste into the editor
4. The diagram will render automatically

### Option 3: VSCode

1. Install the "Markdown Preview Mermaid Support" extension
2. Create a markdown file with the diagram embedded:

```markdown
# Agent Centrality Graph

\`\`\`mermaid
[paste diagram contents here]
\`\`\`
```

3. Use Markdown Preview (Ctrl+Shift+V)

### Option 4: Export as Image

Using Mermaid Live Editor:
1. Open the diagram as described above
2. Click the "Actions" menu
3. Select "PNG", "SVG", or "PDF" to export

## Understanding the Visualization

### Node Types

#### Agents (Top Row)
- **BANTJIES** (Red, thick border) - Central orchestrator with highest centrality (1.0)
- **RYNETTE** (Orange) - Revenue coordinator (0.46)
- **JACQUI** (Purple) - Signature authority (0.36)
- **PETER** (Cyan) - Manipulated puppet (0.15)
- **DANIEL** (Gray) - Marginalized whistleblower (-0.15)

#### Events (Chronologically arranged)
Color-coded by category:
- **Blue**: Positioning events (TRUSTEE, AUTHORITY)
- **Green**: Whistleblowing (REPORTS)
- **Red**: Crisis response (CARDS)
- **Orange**: Threats (R10M)
- **Dark gray**: Abandonment (HOLIDAY)
- **Yellow**: Bypassing (MAIN)
- **Purple**: Weaponization (INTERDICT)
- **Dark red**: Perjury (AFFIDAVIT), Extraction (R18M)

### Edge Types

#### Solid Arrows (→)
Direct actions or relationships:
- `DANIEL → REPORTS`: Daniel reports fraud
- `PETER → CARDS`: Peter executes card cancellations
- `PETER → INTERDICT`: Peter involved in interdict

#### Dashed Arrows (-.->)
Hypergraph edges with attention weights:
- Shows influence and control relationships
- Weight indicates importance (0.83 to 1.0)
- Higher weights = stronger relationships

#### Double-line Arrows (==>)
Universal motivation:
- R18M payout drives all major actions
- Highest weight (1.0) indicates primary driver

### Subgraphs (Narratives)

Three parallel hidden narratives are highlighted:

1. **NARRATIVE1: Financial Control Architecture**
   - TRUSTEE → AUTHORITY → R18M
   - Building systematic financial control

2. **NARRATIVE2: Whistleblower Neutralization**
   - REPORTS → HOLIDAY → INTERDICT
   - Systematic suppression of fraud reporting

3. **NARRATIVE3: Dual-Layer Operations**
   - CARDS → MAIN → AFFIDAVIT
   - Operating through institutional and legal channels

### Reading the Timeline

Events are arranged chronologically from left to right:

```
July 2024 → Oct 2024 → June 6, 2025 → June 7, 2025 → June 10, 2025 → Aug 11, 2025 → Aug 13, 2025 → May 2026
```

Key patterns:
- **24-hour response**: REPORTS (June 6) → CARDS (June 7)
- **Same-day action**: R10M (AM) → HOLIDAY (PM) on June 10
- **2-day coordination**: MAIN (Aug 11) → INTERDICT (Aug 13)

## Analytical Insights from the Visualization

### Power Structure (Centrality Scores)

The visual size and color intensity of nodes reflect their centrality:

- **1.0** (BANTJIES): Maximum influence, controls all major actions
- **0.46** (RYNETTE): High operational control
- **0.36** (JACQUI): Significant authority
- **0.15** (PETER): Low influence, executes orders
- **-0.15** (DANIEL): Isolated and marginalized

### Network Patterns

1. **Hub-and-Spoke**: BANTJIES at center with connections to all major nodes
2. **Sequential Chains**: Events linked in temporal sequences
3. **Feedback Loops**: Actions trigger reactions (e.g., REPORTS → CARDS)
4. **Parallel Tracks**: Multiple narratives operate simultaneously

### Attention Weights

Edge weights reveal relationship importance:

- **1.0**: Payout motivation (universal driver)
- **0.95**: Financial information control (critical path)
- **0.92**: Trust governance manipulation
- **0.89**: Oversight authority abuse
- **0.87**: Whistleblower neutralization
- **0.85**: Puppet orchestration
- **0.83**: Timeline coordination

Higher weights indicate stronger evidence and more significant relationships.

## Customizing the Visualization

### Modifying Colors

To change node colors, edit the `classDef` statements at the bottom:

```mermaid
classDef orchestrator fill:#ff6b6b,stroke:#d63447,stroke-width:4px,color:#fff
```

### Adding New Nodes

To add a new node:

1. Define the node with its label:
```mermaid
NEWNODE["`**NEW NODE**
Description
Centrality: 0.5`"]:::nodetype
```

2. Add edges:
```mermaid
BANTJIES -.->|0.80| NEWNODE
```

3. Update subgraphs if needed

### Adjusting Layout

Mermaid uses automatic layout, but you can influence it by:
- Node declaration order affects vertical position
- Edge order affects connection routing
- Subgraph grouping affects node clustering

## Integration with Analysis Code

The visualization corresponds to the data structure in `case_data.py`:

```python
from case_data import get_case_data, get_centrality_scores

# Get all case data
case_data = get_case_data()

# Agents in the visualization
agents = case_data['agents']  # BANTJIES, RYNETTE, JACQUI, PETER, DANIEL

# Events in the visualization
events = case_data['events']  # TRUSTEE, AUTHORITY, REPORTS, etc.

# Hyperedges with weights
relationships = case_data['relationships']

# Hidden narratives
narratives = case_data['narratives']
```

Run the analysis to verify the visualization data:

```bash
python case_studies/trust_fraud_analysis/analyze_case.py
```

## Troubleshooting

### Diagram Doesn't Render

1. **Check Syntax**: Ensure all quotes and brackets are properly closed
2. **Validate Mermaid**: Use Mermaid Live Editor to check for syntax errors
3. **Browser Cache**: Clear cache if viewing on GitHub
4. **Plugin Issues**: Update VSCode Mermaid extension to latest version

### Performance Issues

For large diagrams:
- Reduce the number of edges
- Simplify subgraphs
- Use fewer style definitions
- Split into multiple diagrams

### Export Quality

For high-quality exports:
1. Use Mermaid Live Editor
2. Select SVG format (vector, scalable)
3. For presentations, export as PNG at 300 DPI
4. For documentation, use SVG or embed in markdown

## Additional Resources

- **Mermaid Documentation**: https://mermaid.js.org/
- **Mermaid Flowchart Syntax**: https://mermaid.js.org/syntax/flowchart.html
- **HyperGNN Model**: See `models/hyper_gnn/README.md`
- **Case Study Documentation**: See `case_studies/trust_fraud_analysis/README.md`

## License

This visualization guide is part of the AnalytiCase framework and follows the same license terms as the main repository.
