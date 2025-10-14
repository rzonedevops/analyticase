#!/usr/bin/env python3
"""
Logging Configuration for AnalytiCase Simulations

This module provides centralized logging configuration with timestamped
folder organization for all simulation outputs.
"""

import os
import logging
import datetime
from pathlib import Path
from typing import Optional


class SimulationLogger:
    """Manages logging configuration for simulation runs."""
    
    def __init__(self, base_output_dir: str = None, run_name: str = None):
        """
        Initialize simulation logger with timestamped directory structure.
        
        Args:
            base_output_dir: Base directory for all simulation outputs
            run_name: Optional name for this simulation run
        """
        # Set base output directory
        if base_output_dir is None:
            base_output_dir = os.path.join(
                os.path.dirname(__file__), 
                'results'
            )
        
        self.base_output_dir = Path(base_output_dir)
        
        # Create timestamped run directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if run_name:
            self.run_dir = self.base_output_dir / f"{timestamp}_{run_name}"
        else:
            self.run_dir = self.base_output_dir / timestamp
        
        # Create subdirectories for different output types
        self.logs_dir = self.run_dir / "logs"
        self.data_dir = self.run_dir / "data"
        self.reports_dir = self.run_dir / "reports"
        self.visualizations_dir = self.run_dir / "visualizations"
        
        # Create all directories
        for directory in [self.run_dir, self.logs_dir, self.data_dir, 
                         self.reports_dir, self.visualizations_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Store timestamp
        self.timestamp = timestamp
        
        # Initialize loggers
        self.loggers = {}
        
        # Create main simulation logger
        self.main_logger = self._create_logger(
            'simulation_main',
            self.logs_dir / 'simulation_main.log'
        )
        
        self.main_logger.info(f"Simulation run initialized: {self.run_dir}")
        self.main_logger.info(f"Timestamp: {timestamp}")
    
    def _create_logger(self, name: str, log_file: Path, 
                      level: int = logging.INFO) -> logging.Logger:
        """
        Create a logger with both file and console handlers.
        
        Args:
            name: Logger name
            log_file: Path to log file
            level: Logging level
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        logger.handlers = []
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler (detailed)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # Console handler (simple)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        # Store logger reference
        self.loggers[name] = logger
        
        return logger
    
    def get_model_logger(self, model_name: str) -> logging.Logger:
        """
        Get or create a logger for a specific simulation model.
        
        Args:
            model_name: Name of the simulation model
            
        Returns:
            Logger instance for the model
        """
        logger_name = f'simulation_{model_name}'
        
        if logger_name not in self.loggers:
            log_file = self.logs_dir / f'{model_name}.log'
            logger = self._create_logger(logger_name, log_file)
            logger.info(f"Logger created for model: {model_name}")
        
        return self.loggers[logger_name]
    
    def get_data_path(self, filename: str) -> Path:
        """Get path for data output file."""
        return self.data_dir / filename
    
    def get_report_path(self, filename: str) -> Path:
        """Get path for report output file."""
        return self.reports_dir / filename
    
    def get_visualization_path(self, filename: str) -> Path:
        """Get path for visualization output file."""
        return self.visualizations_dir / filename
    
    def log_simulation_start(self, model_name: str, config: dict):
        """Log the start of a simulation."""
        logger = self.get_model_logger(model_name)
        logger.info("=" * 80)
        logger.info(f"Starting {model_name} simulation")
        logger.info(f"Configuration: {config}")
        logger.info("=" * 80)
    
    def log_simulation_end(self, model_name: str, results: dict):
        """Log the end of a simulation."""
        logger = self.get_model_logger(model_name)
        logger.info("=" * 80)
        logger.info(f"Completed {model_name} simulation")
        logger.info(f"Results summary: {self._summarize_results(results)}")
        logger.info("=" * 80)
    
    def log_error(self, model_name: str, error: Exception):
        """Log an error during simulation."""
        logger = self.get_model_logger(model_name)
        logger.error(f"Error in {model_name} simulation: {str(error)}", exc_info=True)
    
    def _summarize_results(self, results: dict) -> str:
        """Create a brief summary of results."""
        if 'metrics' in results:
            return str(results['metrics'])
        elif 'summary' in results:
            return str(results['summary'])
        else:
            return f"{len(results)} result fields"
    
    def create_run_manifest(self, metadata: dict):
        """Create a manifest file for this simulation run."""
        manifest_path = self.run_dir / 'manifest.json'
        
        import json
        manifest = {
            'timestamp': self.timestamp,
            'run_directory': str(self.run_dir),
            'metadata': metadata,
            'directories': {
                'logs': str(self.logs_dir),
                'data': str(self.data_dir),
                'reports': str(self.reports_dir),
                'visualizations': str(self.visualizations_dir)
            }
        }
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        self.main_logger.info(f"Manifest created: {manifest_path}")
        
        return manifest_path
    
    def finalize(self):
        """Finalize logging and close all handlers."""
        self.main_logger.info("Simulation run finalized")
        self.main_logger.info(f"All outputs saved to: {self.run_dir}")
        
        # Close all handlers
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()


def setup_logging(base_output_dir: str = None, run_name: str = None) -> SimulationLogger:
    """
    Convenience function to set up logging for a simulation run.
    
    Args:
        base_output_dir: Base directory for outputs
        run_name: Optional name for this run
        
    Returns:
        Configured SimulationLogger instance
    """
    return SimulationLogger(base_output_dir, run_name)


if __name__ == "__main__":
    # Test the logging configuration
    logger_manager = setup_logging(run_name="test_run")
    
    # Test main logger
    logger_manager.main_logger.info("Testing main logger")
    
    # Test model logger
    model_logger = logger_manager.get_model_logger("agent_based")
    model_logger.info("Testing model logger")
    
    # Create manifest
    logger_manager.create_run_manifest({
        'purpose': 'Test run',
        'models': ['agent_based', 'discrete_event']
    })
    
    # Finalize
    logger_manager.finalize()
    
    print(f"\nTest outputs created in: {logger_manager.run_dir}")

