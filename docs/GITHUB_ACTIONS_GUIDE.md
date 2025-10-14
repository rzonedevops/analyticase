# AnalytiCase GitHub Actions Guide

## Manual Simulation Workflow

The AnalytiCase repository includes a manual GitHub Action that allows you to run the complete simulation suite directly from the GitHub interface. This is useful for:

- Running simulations without local setup
- Automated testing of configuration changes
- Generating results for analysis and reporting
- Collaborative simulation runs with shared results

## How to Use the Manual Simulation Action

### 1. Navigate to Actions

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Find the **"Run AnalytiCase Simulations"** workflow
4. Click **"Run workflow"**

### 2. Configure Your Simulation Run

The workflow provides several input options:

#### Required Inputs

- **Simulation Name**: A descriptive name for your simulation run
  - Examples: `"quarterly_analysis"`, `"baseline_test"`, `"performance_comparison"`
  - This becomes part of the output folder name: `YYYYMMDD_HHMMSS_your_name`

#### Configuration Options

- **Configuration Type**: Choose how to configure the simulation
  - `default`: Uses built-in default parameters (recommended for quick tests)
  - `example_config`: Uses the pre-configured `simulations/example_config.json`
  - `custom`: Allows you to provide your own JSON configuration

- **Custom Configuration**: Only used when "Configuration Type" is set to "custom"
  - Provide a JSON object with simulation parameters
  - See [Configuration Format](#configuration-format) below

#### Advanced Options

- **Timeout Minutes**: Maximum time to allow the simulation to run (default: 30 minutes)
- **Upload Logs**: Whether to upload detailed execution logs as artifacts (default: enabled)
- **Upload Data**: Whether to upload simulation data results as artifacts (default: enabled)

### 3. Monitor the Workflow

Once started, you can:

- Watch the real-time log output in the GitHub Actions interface
- See progress through each simulation model (Agent-Based, Discrete-Event, etc.)
- View summary results in the workflow output

### 4. Access Results

After completion, results are available in multiple ways:

#### Workflow Summary
- Basic statistics and completion status shown in the workflow log
- Summary report displayed directly in the GitHub Actions output

#### Artifacts
Three types of artifacts are automatically generated:

1. **Simulation Logs** (`simulation-logs-TIMESTAMP`)
   - Execution logs for each model
   - Manifest file with run metadata
   - Useful for debugging and understanding execution flow

2. **Simulation Data** (`simulation-data-TIMESTAMP`)
   - Raw JSON results from each simulation model
   - Human-readable reports and summaries
   - Generated legal briefs and analysis

3. **Complete Results** (`complete-simulation-results-TIMESTAMP`)
   - Full simulation output directory
   - Includes everything: logs, data, reports, visualizations folder
   - Best for comprehensive analysis

## Configuration Format

When using "custom" configuration type, provide a JSON object with these optional sections:

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

### Configuration Guidelines

- **Agent-Based Model**:
  - `num_investigators`: Number of investigation agents (default: 5)
  - `num_attorneys`: Number of attorney agents (default: 8)
  - `num_judges`: Number of judge agents (default: 3)
  - `num_steps`: Simulation steps to run (default: 100)

- **Discrete-Event Model**:
  - `num_cases`: Number of cases to simulate (default: 50)
  - `simulation_duration`: Time period in days (default: 365.0)

- **System Dynamics Model**:
  - `duration`: Simulation duration in days (default: 365.0)
  - `dt`: Time step resolution (default: 1.0)

- **HyperGNN Model**:
  - `input_dim`: Input embedding dimension (default: 64)
  - `hidden_dim`: Hidden layer dimension (default: 32)
  - `num_layers`: Number of GNN layers (default: 2)

- **Case-LLM Model**:
  - `model_name`: LLM model to use (default: "gpt-4.1-mini")
  - `generate_brief`: Whether to generate legal briefs (default: true)

## Example Workflows

### Quick Test Run
- **Name**: `"quick_test"`
- **Configuration**: `default`
- **Timeout**: `15` minutes

### Scaled Analysis
- **Name**: `"scaled_analysis_q4"`
- **Configuration**: `example_config`
- **Timeout**: `45` minutes

### Custom Research Run
- **Name**: `"research_deep_analysis"`
- **Configuration**: `custom`
- **Custom Config**:
```json
{
  "agent_based": {
    "num_investigators": 20,
    "num_attorneys": 30,
    "num_judges": 10,
    "num_steps": 500
  },
  "discrete_event": {
    "num_cases": 200,
    "simulation_duration": 1095.0
  }
}
```
- **Timeout**: `60` minutes

## Troubleshooting

### Common Issues

1. **Timeout Errors**
   - Increase the timeout minutes for large simulations
   - Consider reducing simulation parameters (fewer cases, steps, etc.)

2. **Invalid Configuration**
   - Ensure JSON is properly formatted when using custom config
   - Check parameter ranges are reasonable

3. **Missing Results**
   - Verify artifacts were uploaded successfully
   - Check workflow logs for any error messages

### Performance Guidelines

- Default configuration typically runs in 5-10 minutes
- Example configuration may take 15-30 minutes
- Large custom configurations can take 45+ minutes

### Artifact Retention

- Artifacts are kept for 30 days by default
- Download important results promptly for long-term storage
- Consider archiving results to external storage for permanent retention

## Integration with Local Development

Results from GitHub Actions can be used alongside local development:

1. Download artifacts from successful runs
2. Compare with local simulation results
3. Use as baseline data for performance testing
4. Share results with team members via GitHub

## Security Notes

- The workflow runs in a secure GitHub Actions environment
- No sensitive data is exposed in workflow logs
- OpenAI API keys are not required (mock mode is used)
- All results are contained within the repository scope

## Support

For issues or questions:
1. Check the workflow execution logs first
2. Review this documentation
3. Consult the main [README.md](../README.md)
4. Open an issue in the repository with:
   - Workflow run URL
   - Input parameters used
   - Error messages or unexpected behavior