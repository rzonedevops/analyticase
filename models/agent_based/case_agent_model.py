#!/usr/bin/env python3
"""
Agent-Based Model for Legal Case Analysis

This module implements an agent-based simulation framework for modeling
the behavior and interactions of various entities in legal cases, including
investigators, attorneys, judges, and evidence handlers.
"""

import random
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Types of agents in the legal case system."""
    INVESTIGATOR = "investigator"
    ATTORNEY = "attorney"
    JUDGE = "judge"
    EVIDENCE_HANDLER = "evidence_handler"
    COURT_CLERK = "court_clerk"
    WITNESS = "witness"


class AgentState(Enum):
    """States an agent can be in."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"


@dataclass
class Agent:
    """Base agent class for legal case simulation."""
    agent_id: str
    agent_type: AgentType
    name: str
    state: AgentState = AgentState.IDLE
    workload: int = 0
    efficiency: float = 1.0
    cases_handled: List[str] = field(default_factory=list)
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    
    def update(self, time_step: int) -> None:
        """Update agent state based on current workload and time."""
        if self.workload > 0:
            self.state = AgentState.WORKING
            self.workload = max(0, self.workload - int(self.efficiency))
        else:
            self.state = AgentState.IDLE
    
    def assign_task(self, task: Dict[str, Any]) -> bool:
        """Assign a task to the agent."""
        if self.state == AgentState.IDLE or self.workload < 10:
            self.workload += task.get('complexity', 5)
            self.state = AgentState.WORKING
            logger.info(f"Agent {self.name} assigned task: {task.get('description', 'Unknown')}")
            return True
        return False
    
    def interact(self, other_agent: 'Agent', interaction_type: str) -> Dict[str, Any]:
        """Simulate interaction between agents."""
        interaction = {
            'timestamp': datetime.datetime.now().isoformat(),
            'agent_1': self.agent_id,
            'agent_2': other_agent.agent_id,
            'type': interaction_type,
            'outcome': 'success' if random.random() > 0.1 else 'pending'
        }
        self.interactions.append(interaction)
        other_agent.interactions.append(interaction)
        return interaction


@dataclass
class InvestigatorAgent(Agent):
    """Specialized agent for investigation tasks."""
    evidence_collected: int = 0
    leads_followed: int = 0
    
    def collect_evidence(self, evidence_complexity: int) -> Dict[str, Any]:
        """Collect evidence with varying complexity."""
        success_rate = self.efficiency * (1.0 - evidence_complexity * 0.1)
        success = random.random() < success_rate
        
        if success:
            self.evidence_collected += 1
            logger.info(f"Investigator {self.name} collected evidence (total: {self.evidence_collected})")
        
        return {
            'success': success,
            'evidence_id': f"EVD-{self.evidence_collected:04d}",
            'complexity': evidence_complexity,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def follow_lead(self, lead_quality: float) -> bool:
        """Follow an investigation lead."""
        self.leads_followed += 1
        success = random.random() < (lead_quality * self.efficiency)
        if success:
            self.workload += 3
        return success


@dataclass
class AttorneyAgent(Agent):
    """Specialized agent for legal representation."""
    cases_won: int = 0
    cases_lost: int = 0
    briefs_filed: int = 0
    
    def prepare_brief(self, case_complexity: int) -> Dict[str, Any]:
        """Prepare legal brief for a case."""
        preparation_time = case_complexity * 2
        self.workload += preparation_time
        self.briefs_filed += 1
        
        return {
            'brief_id': f"BRIEF-{self.briefs_filed:04d}",
            'complexity': case_complexity,
            'estimated_completion': preparation_time,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def argue_case(self, case_strength: float) -> bool:
        """Argue a case in court."""
        success_probability = case_strength * self.efficiency * 0.8
        success = random.random() < success_probability
        
        if success:
            self.cases_won += 1
        else:
            self.cases_lost += 1
        
        logger.info(f"Attorney {self.name} {'won' if success else 'lost'} case (W:{self.cases_won} L:{self.cases_lost})")
        return success


@dataclass
class JudgeAgent(Agent):
    """Specialized agent for judicial decisions."""
    cases_adjudicated: int = 0
    rulings_made: int = 0
    
    def review_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review case materials and evidence."""
        review_time = case_data.get('complexity', 5) * 3
        self.workload += review_time
        
        return {
            'review_id': f"REV-{self.cases_adjudicated:04d}",
            'case_id': case_data.get('case_id'),
            'review_time': review_time,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def make_ruling(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a judicial ruling on a case."""
        self.rulings_made += 1
        self.cases_adjudicated += 1
        
        # Simulate ruling based on case strength and evidence
        evidence_weight = case_data.get('evidence_strength', 0.5)
        legal_merit = case_data.get('legal_merit', 0.5)
        
        ruling_score = (evidence_weight * 0.6 + legal_merit * 0.4) * self.efficiency
        ruling = 'favorable' if ruling_score > 0.5 else 'unfavorable'
        
        return {
            'ruling_id': f"RUL-{self.rulings_made:04d}",
            'case_id': case_data.get('case_id'),
            'ruling': ruling,
            'confidence': ruling_score,
            'timestamp': datetime.datetime.now().isoformat()
        }


class CaseAgentSimulation:
    """Main simulation engine for agent-based case modeling."""
    
    def __init__(self, num_investigators: int = 5, num_attorneys: int = 8, num_judges: int = 3):
        self.agents: List[Agent] = []
        self.time_step: int = 0
        self.events: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
        
        # Create agents
        self._initialize_agents(num_investigators, num_attorneys, num_judges)
        
        logger.info(f"Initialized simulation with {len(self.agents)} agents")
    
    def _initialize_agents(self, num_investigators: int, num_attorneys: int, num_judges: int):
        """Initialize all agents in the simulation."""
        # Create investigators
        for i in range(num_investigators):
            agent = InvestigatorAgent(
                agent_id=f"INV-{i+1:03d}",
                agent_type=AgentType.INVESTIGATOR,
                name=f"Investigator {i+1}",
                efficiency=random.uniform(0.7, 1.0)
            )
            self.agents.append(agent)
        
        # Create attorneys
        for i in range(num_attorneys):
            agent = AttorneyAgent(
                agent_id=f"ATT-{i+1:03d}",
                agent_type=AgentType.ATTORNEY,
                name=f"Attorney {i+1}",
                efficiency=random.uniform(0.6, 0.95)
            )
            self.agents.append(agent)
        
        # Create judges
        for i in range(num_judges):
            agent = JudgeAgent(
                agent_id=f"JDG-{i+1:03d}",
                agent_type=AgentType.JUDGE,
                name=f"Judge {i+1}",
                efficiency=random.uniform(0.8, 1.0)
            )
            self.agents.append(agent)
    
    def step(self) -> None:
        """Execute one time step of the simulation."""
        self.time_step += 1
        
        # Update all agents
        for agent in self.agents:
            agent.update(self.time_step)
        
        # Simulate random interactions
        if random.random() < 0.3:
            agent1, agent2 = random.sample(self.agents, 2)
            interaction = agent1.interact(agent2, 'case_discussion')
            self.events.append(interaction)
    
    def run(self, num_steps: int = 100) -> Dict[str, Any]:
        """Run the simulation for a specified number of steps."""
        logger.info(f"Starting simulation for {num_steps} steps")
        
        for _ in range(num_steps):
            self.step()
            
            # Randomly assign tasks to idle agents
            idle_agents = [a for a in self.agents if a.state == AgentState.IDLE]
            if idle_agents and random.random() < 0.4:
                agent = random.choice(idle_agents)
                task = {
                    'description': f'Task at step {self.time_step}',
                    'complexity': random.randint(3, 8)
                }
                agent.assign_task(task)
        
        # Calculate metrics
        self._calculate_metrics()
        
        logger.info(f"Simulation completed: {self.time_step} steps")
        return self.get_results()
    
    def _calculate_metrics(self):
        """Calculate simulation metrics."""
        total_workload = sum(a.workload for a in self.agents)
        avg_efficiency = sum(a.efficiency for a in self.agents) / len(self.agents)
        
        investigators = [a for a in self.agents if isinstance(a, InvestigatorAgent)]
        attorneys = [a for a in self.agents if isinstance(a, AttorneyAgent)]
        judges = [a for a in self.agents if isinstance(a, JudgeAgent)]
        
        self.metrics = {
            'total_agents': len(self.agents),
            'total_workload': total_workload,
            'average_efficiency': avg_efficiency,
            'total_interactions': len(self.events),
            'investigators': {
                'count': len(investigators),
                'total_evidence': sum(a.evidence_collected for a in investigators),
                'total_leads': sum(a.leads_followed for a in investigators)
            },
            'attorneys': {
                'count': len(attorneys),
                'total_briefs': sum(a.briefs_filed for a in attorneys),
                'cases_won': sum(a.cases_won for a in attorneys),
                'cases_lost': sum(a.cases_lost for a in attorneys)
            },
            'judges': {
                'count': len(judges),
                'cases_adjudicated': sum(a.cases_adjudicated for a in judges),
                'rulings_made': sum(a.rulings_made for a in judges)
            }
        }
    
    def get_results(self) -> Dict[str, Any]:
        """Get simulation results."""
        return {
            'simulation_type': 'agent_based',
            'time_steps': self.time_step,
            'metrics': self.metrics,
            'events': self.events[-10:],  # Last 10 events
            'agent_summary': [
                {
                    'id': a.agent_id,
                    'type': a.agent_type.value,
                    'name': a.name,
                    'state': a.state.value,
                    'efficiency': a.efficiency,
                    'interactions': len(a.interactions)
                }
                for a in self.agents
            ]
        }


def run_agent_simulation(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run an agent-based simulation with the given configuration."""
    if config is None:
        config = {}
    
    num_investigators = config.get('num_investigators', 5)
    num_attorneys = config.get('num_attorneys', 8)
    num_judges = config.get('num_judges', 3)
    num_steps = config.get('num_steps', 100)
    
    simulation = CaseAgentSimulation(num_investigators, num_attorneys, num_judges)
    results = simulation.run(num_steps)
    
    return results


if __name__ == "__main__":
    # Run a sample simulation
    results = run_agent_simulation({'num_steps': 50})
    print(f"Simulation completed with {results['metrics']['total_interactions']} interactions")

