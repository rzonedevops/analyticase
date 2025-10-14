# Logging System Quick Start Guide

> **New!** You can now run simulations directly from GitHub Actions! See the [GitHub Actions Guide](docs/GITHUB_ACTIONS_GUIDE.md) for a no-setup approach to running simulations.

## 🚀 Quick Start

### Run a Simulation with Logging

```bash
# Basic run with automatic timestamping
python3 simulations/simulation_runner_v2.py

# Named run for easy identification
python3 simulations/simulation_runner_v2.py --name "production_run"

# With custom configuration
python3 simulations/simulation_runner_v2.py --config simulations/example_config.json --name "scaled_test"
```

### Output Location

All outputs are saved to timestamped directories:

```
simulations/results/YYYYMMDD_HHMMSS_[run_name]/
```

Example: `simulations/results/20251014_050740_production_run/`

## 📁 What Gets Created

Each simulation run creates:

### 1. Logs Directory
```
logs/
├── simulation_main.log      # Main orchestration log
├── agent_based.log          # Agent-based model execution
├── discrete_event.log       # Discrete-event simulation
├── system_dynamics.log      # System dynamics model
├── hyper_gnn.log           # HyperGNN analysis
└── case_llm.log            # Case-LLM analysis
```

### 2. Data Directory
```
data/
├── complete_results.json           # All results combined
├── agent_based_results.json        # Agent-based results
├── discrete_event_results.json     # Discrete-event results
├── system_dynamics_results.json    # System dynamics results
├── hypergnn_results.json          # HyperGNN results
└── case_llm_results.json          # Case-LLM results
```

### 3. Reports Directory
```
reports/
├── summary_report.txt    # Human-readable summary
└── legal_brief.txt       # Generated legal brief
```

### 4. Manifest File
```
manifest.json    # Run metadata and configuration
```

## 📊 Viewing Results

### Check the Summary
```bash
cat simulations/results/20251014_050740_production_run/reports/summary_report.txt
```

### View Detailed Logs
```bash
# Main simulation log
cat simulations/results/20251014_050740_production_run/logs/simulation_main.log

# Specific model log
cat simulations/results/20251014_050740_production_run/logs/agent_based.log
```

### Analyze JSON Results
```bash
# Pretty-print complete results
cat simulations/results/20251014_050740_production_run/data/complete_results.json | python3 -m json.tool

# Extract specific metrics
cat simulations/results/20251014_050740_production_run/data/agent_based_results.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Agents: {data['metrics']['total_agents']}, Efficiency: {data['metrics']['average_efficiency']:.2%}\")"
```

## ⚙️ Configuration

### Example Configuration File

Create `my_config.json`:

```json
{
  "agent_based": {
    "num_investigators": 10,
    "num_attorneys": 15,
    "num_judges": 5,
    "num_steps": 200
  },
  "discrete_event": {
    "num_cases": 100,
    "simulation_duration": 730.0
  },
  "system_dynamics": {
    "duration": 730.0,
    "dt": 0.5
  },
  "hyper_gnn": {
    "input_dim": 128,
    "hidden_dim": 64,
    "num_layers": 3
  },
  "case_llm": {
    "model_name": "gpt-4.1-mini",
    "generate_brief": true
  }
}
```

Run with configuration:
```bash
python3 simulations/simulation_runner_v2.py --config my_config.json --name "custom_run"
```

## 🔍 Finding Specific Runs

### List All Runs
```bash
ls -lt simulations/results/
```

### Find Runs by Name
```bash
find simulations/results/ -name "*production_run*" -type d
```

### Find Recent Runs
```bash
find simulations/results/ -name "202510*" -type d | sort -r | head -5
```

## 🛠️ Programmatic Usage

Use the logging system in your own Python scripts:

```python
from simulations.logging_config import setup_logging
import json

# Initialize logging
logger_manager = setup_logging(run_name="my_analysis")
logger = logger_manager.main_logger

# Log messages
logger.info("Starting custom analysis")

# Get model-specific logger
model_logger = logger_manager.get_model_logger("custom_model")
model_logger.info("Processing data...")

# Save results
results = {"metric1": 100, "metric2": 200}
data_path = logger_manager.get_data_path("my_results.json")
with open(data_path, 'w') as f:
    json.dump(results, f, indent=2)

# Create manifest
logger_manager.create_run_manifest({
    "purpose": "Custom analysis",
    "parameters": {"param1": "value1"}
})

# Finalize
logger_manager.finalize()

print(f"Results saved to: {logger_manager.run_dir}")
```

## 📈 Best Practices

1. **Use Descriptive Names**: `--name "q4_production_analysis"` instead of generic names
2. **Keep Configs**: Save your configuration files for reproducibility
3. **Check Logs First**: When debugging, always check the relevant log file
4. **Archive Old Runs**: Periodically move old runs to archive storage
5. **Monitor Disk Space**: Large simulations can generate significant data

## 🎯 Common Tasks

### Compare Two Runs
```bash
# Compare agent efficiency
echo "Run 1:"
cat simulations/results/20251014_050740_production_run/data/agent_based_results.json | grep -o '"average_efficiency": [0-9.]*'

echo "Run 2:"
cat simulations/results/20251014_051234_test_run/data/agent_based_results.json | grep -o '"average_efficiency": [0-9.]*'
```

### Extract All Summaries
```bash
for dir in simulations/results/*/; do
    echo "=== $(basename $dir) ==="
    cat "$dir/reports/summary_report.txt" | grep -A 5 "KEY INSIGHTS"
    echo
done
```

### Clean Up Old Runs
```bash
# Archive runs older than 30 days
find simulations/results/ -name "202*" -type d -mtime +30 -exec mv {} /path/to/archive/ \;
```

## 🆘 Troubleshooting

### Issue: No output directory created
**Check:** Ensure you have write permissions to the simulations/results directory

### Issue: Logs are empty
**Check:** Verify that the simulation actually ran (check return code)

### Issue: Missing model results
**Check:** Look for errors in the corresponding model log file

### Issue: Disk full
**Solution:** Archive or delete old simulation runs

## 📚 Additional Resources

- Full documentation: `simulations/LOGGING_README.md`
- Example configuration: `simulations/example_config.json`
- Main README: `README.md`

## 💡 Tips

- Use `--name` with dates for time-series analysis: `--name "2025-10-14_baseline"`
- Keep a log of your configuration files in version control
- Set up automated archival of old runs to prevent disk space issues
- Use the manifest.json file to track what configurations you've tested

