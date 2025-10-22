#!/usr/bin/env python3
"""
Enhanced Agent-Based Model for Legal Case Analysis

This module implements an advanced agent-based simulation framework for modeling
the behavior and interactions of various entities in legal cases, including
investigators, attorneys, judges, and evidence handlers.

Version: 2.0
Enhancements:
- Agent memory and learning capabilities
- Advanced behavioral patterns and decision-making
- Temporal analysis and pattern recognition
- Network effects and collaboration dynamics
- Performance tracking and adaptation
"""

import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import datetime
from collections import defaultdict
import math

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
    EXPERT_WITNESS = "expert_witness"
    MEDIATOR = "mediator"


class AgentState(Enum):
    """States an agent can be in."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    COLLABORATING = "collaborating"
    LEARNING = "learning"


class TaskPriority(Enum):
    """Priority levels for tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Memory:
    """Agent memory structure for storing experiences and learning."""
    experiences: List[Dict[str, Any]] = field(default_factory=list)
    successful_strategies: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    failed_strategies: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    collaboration_history: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    performance_history: List[float] = field(default_factory=list)
    
    def add_experience(self, experience: Dict[str, Any]) -> None:
        """Add an experience to memory."""
        self.experiences.append(experience)
        if len(self.experiences) > 100:  # Keep last 100 experiences
            self.experiences.pop(0)
    
    def record_strategy_outcome(self, strategy: str, success: bool) -> None:
        """Record the outcome of a strategy."""
        if success:
            self.successful_strategies[strategy] += 1
        else:
            self.failed_strategies[strategy] += 1
    
    def get_strategy_success_rate(self, strategy: str) -> float:
        """Calculate success rate for a strategy."""
        total = self.successful_strategies[strategy] + self.failed_strategies[strategy]
        if total == 0:
            return 0.5  # Unknown strategy, assume 50%
        return self.successful_strategies[strategy] / total
    
    def record_collaboration(self, partner_id: str, outcome_score: float) -> None:
        """Record collaboration outcome with another agent."""
        self.collaboration_history[partner_id].append(outcome_score)
    
    def get_collaboration_score(self, partner_id: str) -> float:
        """Get average collaboration score with a partner."""
        scores = self.collaboration_history.get(partner_id, [0.5])
        return sum(scores) / len(scores)


@dataclass
class Agent:
    """Enhanced base agent class for legal case simulation."""
    agent_id: str
    agent_type: AgentType
    name: str
    state: AgentState = AgentState.IDLE
    workload: int = 0
    efficiency: float = 1.0
    base_efficiency: float = 1.0
    cases_handled: List[str] = field(default_factory=list)
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    memory: Memory = field(default_factory=Memory)
    stress_level: float = 0.0
    expertise_level: float = 0.5
    learning_rate: float = 0.01
    collaboration_preference: float = 0.5
    current_tasks: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize derived attributes."""
        self.base_efficiency = self.efficiency
    
    def update(self, time_step: int) -> None:
        """Update agent state based on current workload and time."""
        # Update workload
        if self.workload > 0:
            self.state = AgentState.WORKING
            work_done = int(self.get_effective_efficiency())
            self.workload = max(0, self.workload - work_done)
            
            # Update stress based on workload
            self.stress_level = min(1.0, self.workload / 20.0)
        else:
            self.state = AgentState.IDLE
            # Stress decreases when idle
            self.stress_level = max(0.0, self.stress_level - 0.05)
        
        # Learn from experiences
        if time_step % 10 == 0:
            self._learn_from_experience()
        
        # Update task priorities
        self._update_task_priorities()
    
    def get_effective_efficiency(self) -> float:
        """Calculate effective efficiency considering stress and expertise."""
        stress_penalty = 1.0 - (self.stress_level * 0.3)  # Up to 30% penalty
        expertise_bonus = 1.0 + (self.expertise_level * 0.2)  # Up to 20% bonus
        return self.base_efficiency * stress_penalty * expertise_bonus
    
    def assign_task(self, task: Dict[str, Any]) -> bool:
        """Assign a task to the agent with priority handling."""
        priority = task.get('priority', TaskPriority.MEDIUM)
        complexity = task.get('complexity', 5)
        
        # Check if agent can take the task
        if self.workload > 15 and priority.value < TaskPriority.HIGH.value:
            return False
        
        # Add task to current tasks
        task['assigned_time'] = datetime.datetime.now().isoformat()
        task['estimated_completion'] = complexity / self.get_effective_efficiency()
        self.current_tasks.append(task)
        
        # Update workload
        self.workload += complexity
        self.state = AgentState.WORKING
        
        logger.info(f"Agent {self.name} assigned task: {task.get('description', 'Unknown')} (Priority: {priority.name})")
        return True
    
    def _update_task_priorities(self) -> None:
        """Update priorities of current tasks based on deadlines."""
        current_time = datetime.datetime.now()
        for task in self.current_tasks:
            if 'deadline' in task:
                deadline = datetime.datetime.fromisoformat(task['deadline'])
                time_remaining = (deadline - current_time).total_seconds()
                if time_remaining < 3600:  # Less than 1 hour
                    task['priority'] = TaskPriority.URGENT
                elif time_remaining < 86400:  # Less than 1 day
                    task['priority'] = TaskPriority.HIGH
    
    def interact(self, other_agent: 'Agent', interaction_type: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulate interaction between agents with learning."""
        # Calculate interaction success based on collaboration history
        collab_score = self.memory.get_collaboration_score(other_agent.agent_id)
        base_success_rate = 0.7 + (collab_score * 0.2)
        
        success = random.random() < base_success_rate
        outcome_score = random.uniform(0.6, 1.0) if success else random.uniform(0.2, 0.5)
        
        interaction = {
            'timestamp': datetime.datetime.now().isoformat(),
            'agent_1': self.agent_id,
            'agent_2': other_agent.agent_id,
            'type': interaction_type,
            'outcome': 'success' if success else 'pending',
            'outcome_score': outcome_score,
            'context': context or {}
        }
        
        # Record interaction in memory
        self.interactions.append(interaction)
        other_agent.interactions.append(interaction)
        
        # Update collaboration history
        self.memory.record_collaboration(other_agent.agent_id, outcome_score)
        other_agent.memory.record_collaboration(self.agent_id, outcome_score)
        
        return interaction
    
    def _learn_from_experience(self) -> None:
        """Learn from past experiences to improve performance."""
        if len(self.memory.performance_history) > 5:
            recent_performance = self.memory.performance_history[-5:]
            avg_performance = sum(recent_performance) / len(recent_performance)
            
            # Adjust expertise based on performance
            if avg_performance > 0.7:
                self.expertise_level = min(1.0, self.expertise_level + self.learning_rate)
            elif avg_performance < 0.4:
                self.expertise_level = max(0.1, self.expertise_level - self.learning_rate * 0.5)
    
    def decide_collaboration(self, other_agent: 'Agent', task_complexity: float) -> bool:
        """Decide whether to collaborate on a task."""
        # Consider collaboration history
        collab_score = self.memory.get_collaboration_score(other_agent.agent_id)
        
        # Consider task complexity
        complexity_factor = min(1.0, task_complexity / 10.0)
        
        # Consider current workload
        workload_factor = 1.0 - (self.workload / 20.0)
        
        # Decision probability
        collaboration_probability = (
            self.collaboration_preference * 0.4 +
            collab_score * 0.3 +
            complexity_factor * 0.2 +
            workload_factor * 0.1
        )
        
        return random.random() < collaboration_probability


@dataclass
class InvestigatorAgent(Agent):
    """Enhanced specialized agent for investigation tasks."""
    evidence_collected: int = 0
    leads_followed: int = 0
    investigation_strategies: List[str] = field(default_factory=lambda: ['systematic', 'intuitive', 'collaborative'])
    evidence_quality_scores: List[float] = field(default_factory=list)
    
    def collect_evidence(self, evidence_complexity: int, strategy: str = 'systematic') -> Dict[str, Any]:
        """Collect evidence with varying complexity and strategies."""
        # Get strategy success rate from memory
        strategy_success_rate = self.memory.get_strategy_success_rate(strategy)
        
        # Calculate success probability
        base_rate = self.get_effective_efficiency() * (1.0 - evidence_complexity * 0.1)
        success_rate = base_rate * (0.7 + strategy_success_rate * 0.3)
        success = random.random() < success_rate
        
        # Calculate evidence quality
        quality_score = random.uniform(0.6, 1.0) if success else random.uniform(0.2, 0.5)
        
        if success:
            self.evidence_collected += 1
            self.evidence_quality_scores.append(quality_score)
            logger.info(f"Investigator {self.name} collected evidence (total: {self.evidence_collected}, quality: {quality_score:.2f})")
        
        # Record strategy outcome
        self.memory.record_strategy_outcome(strategy, success)
        
        # Record performance
        self.memory.performance_history.append(quality_score)
        
        result = {
            'success': success,
            'evidence_id': f"EVD-{self.evidence_collected:04d}",
            'complexity': evidence_complexity,
            'quality_score': quality_score,
            'strategy': strategy,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Add to memory
        self.memory.add_experience({
            'type': 'evidence_collection',
            'result': result
        })
        
        return result
    
    def follow_lead(self, lead_quality: float, strategy: str = 'systematic') -> Dict[str, Any]:
        """Follow an investigation lead with strategic approach."""
        self.leads_followed += 1
        
        strategy_success_rate = self.memory.get_strategy_success_rate(f"lead_{strategy}")
        success_rate = lead_quality * self.get_effective_efficiency() * (0.7 + strategy_success_rate * 0.3)
        success = random.random() < success_rate
        
        if success:
            self.workload += 3
            # Successful lead may reveal more evidence
            if random.random() < 0.4:
                self.collect_evidence(random.randint(3, 7), strategy)
        
        self.memory.record_strategy_outcome(f"lead_{strategy}", success)
        
        return {
            'success': success,
            'lead_id': f"LEAD-{self.leads_followed:04d}",
            'quality': lead_quality,
            'strategy': strategy,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def analyze_evidence_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in collected evidence."""
        if len(self.evidence_quality_scores) < 3:
            return {'status': 'insufficient_data'}
        
        avg_quality = sum(self.evidence_quality_scores) / len(self.evidence_quality_scores)
        quality_trend = 'improving' if self.evidence_quality_scores[-3:] > self.evidence_quality_scores[:3] else 'stable'
        
        return {
            'total_evidence': self.evidence_collected,
            'average_quality': avg_quality,
            'quality_trend': quality_trend,
            'best_strategy': max(self.memory.successful_strategies.items(), 
                                key=lambda x: x[1])[0] if self.memory.successful_strategies else 'systematic'
        }


@dataclass
class AttorneyAgent(Agent):
    """Enhanced specialized agent for legal representation."""
    cases_won: int = 0
    cases_lost: int = 0
    briefs_filed: int = 0
    legal_strategies: List[str] = field(default_factory=lambda: ['aggressive', 'conservative', 'negotiation'])
    case_outcomes: List[Dict[str, Any]] = field(default_factory=list)
    
    def prepare_brief(self, case_complexity: int, strategy: str = 'conservative') -> Dict[str, Any]:
        """Prepare legal brief for a case with strategic approach."""
        strategy_success_rate = self.memory.get_strategy_success_rate(f"brief_{strategy}")
        
        # Adjust preparation time based on strategy and expertise
        base_time = case_complexity * 2
        time_modifier = 1.0 - (self.expertise_level * 0.3)
        preparation_time = int(base_time * time_modifier)
        
        self.workload += preparation_time
        self.briefs_filed += 1
        
        # Calculate brief quality
        quality = self.get_effective_efficiency() * (0.7 + strategy_success_rate * 0.3)
        
        result = {
            'brief_id': f"BRIEF-{self.briefs_filed:04d}",
            'complexity': case_complexity,
            'strategy': strategy,
            'quality': quality,
            'estimated_completion': preparation_time,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.memory.add_experience({
            'type': 'brief_preparation',
            'result': result
        })
        
        return result
    
    def argue_case(self, case_strength: float, strategy: str = 'conservative') -> Dict[str, Any]:
        """Argue a case in court with strategic approach."""
        strategy_success_rate = self.memory.get_strategy_success_rate(f"argue_{strategy}")
        
        # Calculate success probability
        base_probability = case_strength * self.get_effective_efficiency() * 0.8
        strategy_bonus = strategy_success_rate * 0.2
        success_probability = min(0.95, base_probability + strategy_bonus)
        
        success = random.random() < success_probability
        
        if success:
            self.cases_won += 1
        else:
            self.cases_lost += 1
        
        # Record outcome
        outcome = {
            'success': success,
            'case_strength': case_strength,
            'strategy': strategy,
            'win_rate': self.cases_won / (self.cases_won + self.cases_lost) if (self.cases_won + self.cases_lost) > 0 else 0.5,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.case_outcomes.append(outcome)
        self.memory.record_strategy_outcome(f"argue_{strategy}", success)
        self.memory.performance_history.append(1.0 if success else 0.0)
        
        logger.info(f"Attorney {self.name} {'won' if success else 'lost'} case (W:{self.cases_won} L:{self.cases_lost})")
        
        return outcome
    
    def negotiate_settlement(self, case_value: float, opponent_strength: float) -> Dict[str, Any]:
        """Negotiate a settlement with opposing counsel."""
        negotiation_skill = self.get_effective_efficiency() * self.memory.get_strategy_success_rate('negotiation')
        
        # Calculate settlement value
        strength_ratio = case_value / (case_value + opponent_strength)
        settlement_ratio = strength_ratio * (0.7 + negotiation_skill * 0.3)
        settlement_value = case_value * settlement_ratio
        
        success = random.random() < (negotiation_skill * 0.8)
        
        self.memory.record_strategy_outcome('negotiation', success)
        
        return {
            'success': success,
            'settlement_value': settlement_value,
            'original_value': case_value,
            'settlement_ratio': settlement_ratio,
            'timestamp': datetime.datetime.now().isoformat()
        }


@dataclass
class JudgeAgent(Agent):
    """Enhanced specialized agent for judicial decisions."""
    cases_adjudicated: int = 0
    rulings_made: int = 0
    ruling_consistency: float = 0.85
    precedent_adherence: float = 0.90
    
    def review_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review case materials and evidence with thorough analysis."""
        complexity = case_data.get('complexity', 5)
        evidence_count = case_data.get('evidence_count', 0)
        
        # Review time increases with complexity and evidence
        base_time = complexity * 3
        evidence_time = evidence_count * 0.5
        review_time = int((base_time + evidence_time) / self.get_effective_efficiency())
        
        self.workload += review_time
        
        # Analyze case thoroughly
        analysis_depth = self.get_effective_efficiency() * self.expertise_level
        
        result = {
            'review_id': f"REV-{self.cases_adjudicated:04d}",
            'case_id': case_data.get('case_id'),
            'review_time': review_time,
            'analysis_depth': analysis_depth,
            'evidence_reviewed': evidence_count,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.memory.add_experience({
            'type': 'case_review',
            'result': result
        })
        
        return result
    
    def make_ruling(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a judicial ruling on a case with precedent consideration."""
        self.rulings_made += 1
        self.cases_adjudicated += 1
        
        # Gather case factors
        evidence_weight = case_data.get('evidence_strength', 0.5)
        legal_merit = case_data.get('legal_merit', 0.5)
        precedent_alignment = case_data.get('precedent_alignment', 0.5)
        
        # Calculate ruling score with precedent consideration
        ruling_score = (
            evidence_weight * 0.4 +
            legal_merit * 0.3 +
            precedent_alignment * 0.2 +
            self.get_effective_efficiency() * 0.1
        )
        
        # Apply consistency factor
        if len(self.memory.performance_history) > 0:
            avg_past_rulings = sum(self.memory.performance_history[-10:]) / len(self.memory.performance_history[-10:])
            ruling_score = ruling_score * 0.7 + avg_past_rulings * self.ruling_consistency * 0.3
        
        ruling = 'favorable' if ruling_score > 0.5 else 'unfavorable'
        
        # Record performance
        self.memory.performance_history.append(ruling_score)
        
        result = {
            'ruling_id': f"RUL-{self.rulings_made:04d}",
            'case_id': case_data.get('case_id'),
            'ruling': ruling,
            'confidence': ruling_score,
            'evidence_weight': evidence_weight,
            'legal_merit': legal_merit,
            'precedent_alignment': precedent_alignment,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.memory.add_experience({
            'type': 'ruling',
            'result': result
        })
        
        return result
    
    def assess_precedent_impact(self, case_data: Dict[str, Any]) -> float:
        """Assess how well a case aligns with legal precedents."""
        # Simulate precedent analysis
        precedent_factors = case_data.get('precedent_factors', [])
        if not precedent_factors:
            return 0.5
        
        alignment_scores = [random.uniform(0.4, 1.0) for _ in precedent_factors]
        weighted_score = sum(alignment_scores) / len(alignment_scores)
        
        return weighted_score * self.precedent_adherence


class CaseAgentSimulation:
    """Enhanced main simulation engine for agent-based case modeling."""
    
    def __init__(self, num_investigators: int = 5, num_attorneys: int = 8, num_judges: int = 3):
        self.agents: List[Agent] = []
        self.time_step: int = 0
        self.events: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
        self.collaboration_network: Dict[str, List[str]] = defaultdict(list)
        self.case_pipeline: List[Dict[str, Any]] = []
        
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
                efficiency=random.uniform(0.7, 1.0),
                expertise_level=random.uniform(0.3, 0.7),
                collaboration_preference=random.uniform(0.4, 0.8)
            )
            self.agents.append(agent)
        
        # Create attorneys
        for i in range(num_attorneys):
            agent = AttorneyAgent(
                agent_id=f"ATT-{i+1:03d}",
                agent_type=AgentType.ATTORNEY,
                name=f"Attorney {i+1}",
                efficiency=random.uniform(0.6, 0.95),
                expertise_level=random.uniform(0.4, 0.8),
                collaboration_preference=random.uniform(0.3, 0.7)
            )
            self.agents.append(agent)
        
        # Create judges
        for i in range(num_judges):
            agent = JudgeAgent(
                agent_id=f"JDG-{i+1:03d}",
                agent_type=AgentType.JUDGE,
                name=f"Judge {i+1}",
                efficiency=random.uniform(0.8, 1.0),
                expertise_level=random.uniform(0.6, 0.9),
                collaboration_preference=random.uniform(0.2, 0.5)
            )
            self.agents.append(agent)
    
    def step(self) -> None:
        """Execute one time step of the simulation."""
        self.time_step += 1
        
        # Update all agents
        for agent in self.agents:
            agent.update(self.time_step)
        
        # Simulate interactions with collaboration decisions
        if random.random() < 0.3:
            agent1, agent2 = random.sample(self.agents, 2)
            
            # Check if agents decide to collaborate
            if agent1.decide_collaboration(agent2, random.uniform(3, 8)):
                interaction = agent1.interact(agent2, 'case_collaboration', 
                                             {'time_step': self.time_step})
                self.events.append(interaction)
                
                # Update collaboration network
                self.collaboration_network[agent1.agent_id].append(agent2.agent_id)
                self.collaboration_network[agent2.agent_id].append(agent1.agent_id)
        
        # Simulate case progression
        self._progress_cases()
    
    def _progress_cases(self) -> None:
        """Progress cases through the pipeline."""
        for case in self.case_pipeline:
            case['time_in_system'] = case.get('time_in_system', 0) + 1
            
            # Move case through stages
            if case['stage'] == 'investigation' and case['time_in_system'] > 20:
                case['stage'] = 'litigation'
            elif case['stage'] == 'litigation' and case['time_in_system'] > 50:
                case['stage'] = 'adjudication'
            elif case['stage'] == 'adjudication' and case['time_in_system'] > 70:
                case['stage'] = 'completed'
    
    def run(self, num_steps: int = 100) -> Dict[str, Any]:
        """Run the simulation for a specified number of steps."""
        logger.info(f"Starting enhanced simulation for {num_steps} steps")
        
        # Initialize some cases
        for i in range(5):
            self.case_pipeline.append({
                'case_id': f"CASE-{i+1:04d}",
                'stage': 'investigation',
                'complexity': random.randint(3, 9),
                'time_in_system': 0
            })
        
        for _ in range(num_steps):
            self.step()
            
            # Assign tasks to agents based on case needs
            self._assign_tasks_intelligently()
            
            # Periodically add new cases
            if self.time_step % 30 == 0:
                self.case_pipeline.append({
                    'case_id': f"CASE-{len(self.case_pipeline)+1:04d}",
                    'stage': 'investigation',
                    'complexity': random.randint(3, 9),
                    'time_in_system': 0
                })
        
        # Calculate comprehensive metrics
        self._calculate_metrics()
        
        logger.info(f"Simulation completed: {self.time_step} steps")
        return self.get_results()
    
    def _assign_tasks_intelligently(self) -> None:
        """Intelligently assign tasks based on agent capabilities and case needs."""
        active_cases = [c for c in self.case_pipeline if c['stage'] != 'completed']
        
        for case in active_cases:
            if random.random() < 0.3:  # Assign tasks probabilistically
                # Find appropriate agent type for case stage
                if case['stage'] == 'investigation':
                    eligible_agents = [a for a in self.agents if isinstance(a, InvestigatorAgent)]
                elif case['stage'] == 'litigation':
                    eligible_agents = [a for a in self.agents if isinstance(a, AttorneyAgent)]
                elif case['stage'] == 'adjudication':
                    eligible_agents = [a for a in self.agents if isinstance(a, JudgeAgent)]
                else:
                    continue
                
                # Select best available agent
                idle_agents = [a for a in eligible_agents if a.state == AgentState.IDLE]
                if idle_agents:
                    # Choose agent with highest expertise and lowest workload
                    best_agent = max(idle_agents, 
                                   key=lambda a: a.expertise_level - (a.workload / 20.0))
                    
                    task = {
                        'description': f"{case['stage']} for {case['case_id']}",
                        'complexity': case['complexity'],
                        'priority': TaskPriority.MEDIUM,
                        'case_id': case['case_id']
                    }
                    best_agent.assign_task(task)
    
    def _calculate_metrics(self):
        """Calculate comprehensive simulation metrics."""
        total_workload = sum(a.workload for a in self.agents)
        avg_efficiency = sum(a.get_effective_efficiency() for a in self.agents) / len(self.agents)
        avg_expertise = sum(a.expertise_level for a in self.agents) / len(self.agents)
        avg_stress = sum(a.stress_level for a in self.agents) / len(self.agents)
        
        investigators = [a for a in self.agents if isinstance(a, InvestigatorAgent)]
        attorneys = [a for a in self.agents if isinstance(a, AttorneyAgent)]
        judges = [a for a in self.agents if isinstance(a, JudgeAgent)]
        
        # Calculate collaboration metrics
        total_collaborations = sum(len(partners) for partners in self.collaboration_network.values())
        avg_collaborations = total_collaborations / len(self.agents) if self.agents else 0
        
        # Calculate case metrics
        completed_cases = [c for c in self.case_pipeline if c['stage'] == 'completed']
        avg_case_time = sum(c['time_in_system'] for c in completed_cases) / len(completed_cases) if completed_cases else 0
        
        self.metrics = {
            'total_agents': len(self.agents),
            'total_workload': total_workload,
            'average_efficiency': avg_efficiency,
            'average_expertise': avg_expertise,
            'average_stress': avg_stress,
            'total_interactions': len(self.events),
            'total_collaborations': total_collaborations,
            'average_collaborations_per_agent': avg_collaborations,
            'cases': {
                'total': len(self.case_pipeline),
                'completed': len(completed_cases),
                'average_time': avg_case_time,
                'in_investigation': len([c for c in self.case_pipeline if c['stage'] == 'investigation']),
                'in_litigation': len([c for c in self.case_pipeline if c['stage'] == 'litigation']),
                'in_adjudication': len([c for c in self.case_pipeline if c['stage'] == 'adjudication'])
            },
            'investigators': {
                'count': len(investigators),
                'total_evidence': sum(a.evidence_collected for a in investigators),
                'total_leads': sum(a.leads_followed for a in investigators),
                'avg_evidence_quality': sum(sum(a.evidence_quality_scores) / len(a.evidence_quality_scores) 
                                          if a.evidence_quality_scores else 0 for a in investigators) / len(investigators) if investigators else 0
            },
            'attorneys': {
                'count': len(attorneys),
                'total_briefs': sum(a.briefs_filed for a in attorneys),
                'cases_won': sum(a.cases_won for a in attorneys),
                'cases_lost': sum(a.cases_lost for a in attorneys),
                'win_rate': sum(a.cases_won for a in attorneys) / (sum(a.cases_won for a in attorneys) + sum(a.cases_lost for a in attorneys)) if (sum(a.cases_won for a in attorneys) + sum(a.cases_lost for a in attorneys)) > 0 else 0
            },
            'judges': {
                'count': len(judges),
                'cases_adjudicated': sum(a.cases_adjudicated for a in judges),
                'rulings_made': sum(a.rulings_made for a in judges),
                'avg_ruling_confidence': sum(sum(a.memory.performance_history) / len(a.memory.performance_history) 
                                            if a.memory.performance_history else 0.5 for a in judges) / len(judges) if judges else 0
            }
        }
    
    def get_results(self) -> Dict[str, Any]:
        """Get comprehensive simulation results."""
        return {
            'simulation_type': 'agent_based_enhanced',
            'version': '2.0',
            'time_steps': self.time_step,
            'metrics': self.metrics,
            'events': self.events[-20:],  # Last 20 events
            'collaboration_network': dict(self.collaboration_network),
            'agent_summary': [
                {
                    'id': a.agent_id,
                    'type': a.agent_type.value,
                    'name': a.name,
                    'state': a.state.value,
                    'efficiency': a.get_effective_efficiency(),
                    'base_efficiency': a.base_efficiency,
                    'expertise': a.expertise_level,
                    'stress': a.stress_level,
                    'interactions': len(a.interactions),
                    'collaborations': len(self.collaboration_network.get(a.agent_id, [])),
                    'performance_trend': 'improving' if len(a.memory.performance_history) > 5 and 
                                       sum(a.memory.performance_history[-3:]) > sum(a.memory.performance_history[:3]) 
                                       else 'stable'
                }
                for a in self.agents
            ],
            'case_pipeline': self.case_pipeline
        }


def run_agent_simulation(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run an enhanced agent-based simulation with the given configuration."""
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
    results = run_agent_simulation({'num_steps': 150})
    print(f"Enhanced simulation completed:")
    print(f"  - Total interactions: {results['metrics']['total_interactions']}")
    print(f"  - Cases completed: {results['metrics']['cases']['completed']}")
    print(f"  - Average efficiency: {results['metrics']['average_efficiency']:.2f}")
    print(f"  - Attorney win rate: {results['metrics']['attorneys']['win_rate']:.2%}")

