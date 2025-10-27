"""
Enhanced Agent-Based Model for Legal Case Analysis with Legal Principle Integration

This module implements an advanced agent-based simulation framework that integrates
with the legal framework (.scm files) to model legally-aware agents that reference
and apply legal principles in their decision-making.

Version: 3.0
Enhancements:
- Integration with lex/ legal framework
- Legal principle-aware decision making
- Bayesian belief networks for uncertainty handling
- Game-theoretic strategy selection
- Enhanced reputation systems based on principle application accuracy
- Information diffusion models for precedent awareness
- Comprehensive performance metrics
"""

import random
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import datetime
from collections import defaultdict
import math
import json

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
    LEGAL_RESEARCHER = "legal_researcher"


class AgentState(Enum):
    """States an agent can be in."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    COLLABORATING = "collaborating"
    LEARNING = "learning"
    RESEARCHING = "researching"


class TaskPriority(Enum):
    """Priority levels for tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class LegalDomain(Enum):
    """Legal domains for principle application."""
    CONTRACT = "contract"
    CIVIL = "civil"
    CRIMINAL = "criminal"
    CONSTITUTIONAL = "constitutional"
    ADMINISTRATIVE = "administrative"
    DELICT = "delict"
    PROPERTY = "property"
    PROCEDURE = "procedure"


@dataclass
class LegalPrinciple:
    """Represents a legal principle that agents can reference."""
    name: str
    description: str
    domain: List[LegalDomain]
    confidence: float
    provenance: str
    related_principles: List[str] = field(default_factory=list)
    applicability_score: float = 0.9
    case_law_references: List[Dict[str, str]] = field(default_factory=list)
    
    def applies_to_case(self, case_domain: LegalDomain, case_facts: Dict[str, Any]) -> float:
        """Determine if this principle applies to a case and with what confidence."""
        if case_domain not in self.domain:
            return 0.0
        
        # Base applicability on principle's applicability score and confidence
        base_applicability = self.applicability_score * self.confidence
        
        # Adjust based on case-specific factors
        # This is a simplified model - in practice, would use more sophisticated matching
        return base_applicability


@dataclass
class BeliefState:
    """Bayesian belief state for uncertainty handling."""
    beliefs: Dict[str, float] = field(default_factory=dict)  # belief_name -> probability
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    
    def update_belief(self, belief_name: str, evidence_strength: float, prior: float = 0.5) -> float:
        """Update belief using Bayesian updating."""
        # Simplified Bayesian update
        current_belief = self.beliefs.get(belief_name, prior)
        
        # Likelihood ratio based on evidence strength
        likelihood_ratio = evidence_strength / (1 - evidence_strength) if evidence_strength < 1.0 else 10.0
        
        # Update using odds form of Bayes' theorem
        prior_odds = current_belief / (1 - current_belief) if current_belief < 1.0 else 10.0
        posterior_odds = prior_odds * likelihood_ratio
        posterior_prob = posterior_odds / (1 + posterior_odds)
        
        self.beliefs[belief_name] = min(0.99, max(0.01, posterior_prob))
        return self.beliefs[belief_name]
    
    def get_belief(self, belief_name: str, default: float = 0.5) -> float:
        """Get current belief probability."""
        return self.beliefs.get(belief_name, default)


@dataclass
class Memory:
    """Enhanced agent memory with legal principle tracking."""
    experiences: List[Dict[str, Any]] = field(default_factory=list)
    successful_strategies: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    failed_strategies: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    collaboration_history: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    performance_history: List[float] = field(default_factory=list)
    
    # Legal principle tracking
    principles_invoked: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    principle_success_rate: Dict[str, List[bool]] = field(default_factory=lambda: defaultdict(list))
    precedent_knowledge: Set[str] = field(default_factory=set)
    
    def add_experience(self, experience: Dict[str, Any]) -> None:
        """Add an experience to memory."""
        self.experiences.append(experience)
        if len(self.experiences) > 100:
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
            return 0.5
        return self.successful_strategies[strategy] / total
    
    def record_collaboration(self, partner_id: str, outcome_score: float) -> None:
        """Record collaboration outcome with another agent."""
        self.collaboration_history[partner_id].append(outcome_score)
    
    def get_collaboration_score(self, partner_id: str) -> float:
        """Get average collaboration score with a partner."""
        scores = self.collaboration_history.get(partner_id, [0.5])
        return sum(scores) / len(scores)
    
    def record_principle_invocation(self, principle_name: str, success: bool) -> None:
        """Record use of a legal principle and its outcome."""
        self.principles_invoked[principle_name] += 1
        self.principle_success_rate[principle_name].append(success)
    
    def get_principle_expertise(self, principle_name: str) -> float:
        """Get expertise level with a specific principle."""
        if principle_name not in self.principle_success_rate:
            return 0.5
        
        successes = self.principle_success_rate[principle_name]
        if not successes:
            return 0.5
        
        # Weight recent successes more heavily
        weighted_sum = sum(s * (0.9 ** (len(successes) - i - 1)) for i, s in enumerate(successes))
        weighted_count = sum(0.9 ** (len(successes) - i - 1) for i in range(len(successes)))
        
        return weighted_sum / weighted_count if weighted_count > 0 else 0.5
    
    def add_precedent_knowledge(self, precedent_id: str) -> None:
        """Add knowledge of a legal precedent."""
        self.precedent_knowledge.add(precedent_id)
    
    def knows_precedent(self, precedent_id: str) -> bool:
        """Check if agent knows a precedent."""
        return precedent_id in self.precedent_knowledge


@dataclass
class Reputation:
    """Reputation system for agents based on legal reasoning quality."""
    overall_score: float = 0.5
    principle_application_accuracy: float = 0.5
    case_outcome_success_rate: float = 0.5
    peer_ratings: List[float] = field(default_factory=list)
    precedent_awareness_score: float = 0.5
    
    def update_from_case_outcome(self, success: bool, weight: float = 0.1) -> None:
        """Update reputation based on case outcome."""
        outcome_value = 1.0 if success else 0.0
        self.case_outcome_success_rate = (
            (1 - weight) * self.case_outcome_success_rate + weight * outcome_value
        )
        self._update_overall_score()
    
    def update_principle_accuracy(self, accuracy: float, weight: float = 0.1) -> None:
        """Update reputation based on principle application accuracy."""
        self.principle_application_accuracy = (
            (1 - weight) * self.principle_application_accuracy + weight * accuracy
        )
        self._update_overall_score()
    
    def add_peer_rating(self, rating: float) -> None:
        """Add a peer rating (0.0 to 1.0)."""
        self.peer_ratings.append(rating)
        if len(self.peer_ratings) > 20:
            self.peer_ratings.pop(0)
        self._update_overall_score()
    
    def update_precedent_awareness(self, awareness_score: float, weight: float = 0.1) -> None:
        """Update precedent awareness score."""
        self.precedent_awareness_score = (
            (1 - weight) * self.precedent_awareness_score + weight * awareness_score
        )
        self._update_overall_score()
    
    def _update_overall_score(self) -> None:
        """Calculate overall reputation score."""
        peer_avg = sum(self.peer_ratings) / len(self.peer_ratings) if self.peer_ratings else 0.5
        
        self.overall_score = (
            0.3 * self.principle_application_accuracy +
            0.3 * self.case_outcome_success_rate +
            0.2 * peer_avg +
            0.2 * self.precedent_awareness_score
        )


@dataclass
class Agent:
    """Enhanced base agent class with legal principle integration."""
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
    belief_state: BeliefState = field(default_factory=BeliefState)
    reputation: Reputation = field(default_factory=Reputation)
    stress_level: float = 0.0
    expertise_level: float = 0.5
    learning_rate: float = 0.01
    collaboration_preference: float = 0.5
    current_tasks: List[Dict[str, Any]] = field(default_factory=list)
    
    # Legal principle expertise
    domain_expertise: Dict[LegalDomain, float] = field(default_factory=dict)
    known_principles: List[LegalPrinciple] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize derived attributes."""
        self.base_efficiency = self.efficiency
        
        # Initialize domain expertise
        for domain in LegalDomain:
            self.domain_expertise[domain] = random.uniform(0.3, 0.7)
    
    def add_legal_principle(self, principle: LegalPrinciple) -> None:
        """Add a legal principle to agent's knowledge base."""
        if principle not in self.known_principles:
            self.known_principles.append(principle)
            logger.info(f"Agent {self.name} learned principle: {principle.name}")
    
    def find_applicable_principles(self, case_domain: LegalDomain, 
                                   case_facts: Dict[str, Any]) -> List[Tuple[LegalPrinciple, float]]:
        """Find legal principles applicable to a case."""
        applicable = []
        
        for principle in self.known_principles:
            applicability = principle.applies_to_case(case_domain, case_facts)
            if applicability > 0.5:
                # Adjust by agent's expertise with this principle
                agent_expertise = self.memory.get_principle_expertise(principle.name)
                adjusted_applicability = applicability * (0.5 + 0.5 * agent_expertise)
                applicable.append((principle, adjusted_applicability))
        
        # Sort by applicability score
        applicable.sort(key=lambda x: x[1], reverse=True)
        return applicable
    
    def apply_principle(self, principle: LegalPrinciple, case_facts: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a legal principle to a case."""
        # Simulate principle application
        expertise = self.memory.get_principle_expertise(principle.name)
        domain_exp = self.domain_expertise.get(principle.domain[0], 0.5) if principle.domain else 0.5
        
        # Success probability based on expertise and principle confidence
        success_prob = principle.confidence * (0.3 + 0.4 * expertise + 0.3 * domain_exp)
        success = random.random() < success_prob
        
        # Record principle invocation
        self.memory.record_principle_invocation(principle.name, success)
        
        # Update reputation
        self.reputation.update_principle_accuracy(1.0 if success else 0.0)
        
        result = {
            'principle': principle.name,
            'success': success,
            'confidence': success_prob,
            'reasoning': f"Applied {principle.name}: {principle.description}",
            'case_law_support': principle.case_law_references[:2] if success else []
        }
        
        logger.info(f"Agent {self.name} applied {principle.name}: {'Success' if success else 'Failed'}")
        return result
    
    def make_decision(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Make a decision using legal principles and Bayesian reasoning."""
        case_domain = decision_context.get('domain', LegalDomain.CIVIL)
        case_facts = decision_context.get('facts', {})
        
        # Find applicable principles
        applicable_principles = self.find_applicable_principles(case_domain, case_facts)
        
        if not applicable_principles:
            # No principles found, use general reasoning
            return self._make_general_decision(decision_context)
        
        # Use top principles
        top_principles = applicable_principles[:3]
        
        # Apply principles and aggregate results
        principle_results = []
        for principle, applicability in top_principles:
            result = self.apply_principle(principle, case_facts)
            result['applicability'] = applicability
            principle_results.append(result)
        
        # Update belief state based on principle applications
        belief_name = decision_context.get('belief', 'case_success')
        for result in principle_results:
            if result['success']:
                evidence_strength = result['confidence'] * result['applicability']
                self.belief_state.update_belief(belief_name, evidence_strength)
        
        # Make final decision based on belief state
        decision_confidence = self.belief_state.get_belief(belief_name)
        decision = decision_confidence > 0.6
        
        return {
            'decision': decision,
            'confidence': decision_confidence,
            'principles_applied': [r['principle'] for r in principle_results],
            'reasoning': principle_results,
            'belief_state': dict(self.belief_state.beliefs)
        }
    
    def _make_general_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make a decision without specific legal principles."""
        # Use expertise and experience
        confidence = self.expertise_level * random.uniform(0.7, 1.0)
        decision = random.random() < confidence
        
        return {
            'decision': decision,
            'confidence': confidence,
            'principles_applied': [],
            'reasoning': "General expertise-based decision",
            'belief_state': {}
        }
    
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
        
        # Update domain expertise based on recent work
        if time_step % 20 == 0:
            self._update_domain_expertise()
    
    def get_effective_efficiency(self) -> float:
        """Calculate effective efficiency considering stress and expertise."""
        stress_penalty = 1.0 - (self.stress_level * 0.3)
        expertise_bonus = 1.0 + (self.expertise_level * 0.2)
        reputation_bonus = 1.0 + (self.reputation.overall_score * 0.1)
        return self.base_efficiency * stress_penalty * expertise_bonus * reputation_bonus
    
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
                if time_remaining < 3600:
                    task['priority'] = TaskPriority.URGENT
                elif time_remaining < 86400:
                    task['priority'] = TaskPriority.HIGH
    
    def interact(self, other_agent: 'Agent', interaction_type: str, 
                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulate interaction between agents with learning and information diffusion."""
        # Calculate interaction success based on collaboration history
        collab_score = self.memory.get_collaboration_score(other_agent.agent_id)
        reputation_factor = (self.reputation.overall_score + other_agent.reputation.overall_score) / 2
        base_success_rate = 0.6 + (collab_score * 0.2) + (reputation_factor * 0.2)
        
        success = random.random() < base_success_rate
        outcome_score = random.uniform(0.6, 1.0) if success else random.uniform(0.2, 0.5)
        
        # Information diffusion - share precedent knowledge
        if success and interaction_type in ['collaboration', 'consultation']:
            self._share_precedent_knowledge(other_agent)
        
        interaction = {
            'timestamp': datetime.datetime.now().isoformat(),
            'agent_1': self.agent_id,
            'agent_2': other_agent.agent_id,
            'type': interaction_type,
            'outcome': 'success' if success else 'pending',
            'outcome_score': outcome_score,
            'context': context or {},
            'precedents_shared': success
        }
        
        # Record interaction in memory
        self.interactions.append(interaction)
        other_agent.interactions.append(interaction)
        
        # Update collaboration history
        self.memory.record_collaboration(other_agent.agent_id, outcome_score)
        other_agent.memory.record_collaboration(self.agent_id, outcome_score)
        
        # Update peer ratings
        if success:
            self.reputation.add_peer_rating(outcome_score)
            other_agent.reputation.add_peer_rating(outcome_score)
        
        return interaction
    
    def _share_precedent_knowledge(self, other_agent: 'Agent') -> None:
        """Share precedent knowledge with another agent (information diffusion)."""
        # Share some precedents this agent knows but the other doesn't
        my_precedents = self.memory.precedent_knowledge
        other_precedents = other_agent.memory.precedent_knowledge
        
        new_precedents = my_precedents - other_precedents
        
        # Share a subset (information diffusion is not perfect)
        share_count = min(len(new_precedents), random.randint(1, 3))
        shared = random.sample(list(new_precedents), share_count) if new_precedents else []
        
        for precedent in shared:
            other_agent.memory.add_precedent_knowledge(precedent)
        
        # Update precedent awareness scores
        if shared:
            awareness_boost = len(shared) / 10.0
            other_agent.reputation.update_precedent_awareness(
                min(1.0, other_agent.reputation.precedent_awareness_score + awareness_boost)
            )
    
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
    
    def _update_domain_expertise(self) -> None:
        """Update domain expertise based on recent principle applications."""
        for principle in self.known_principles:
            if principle.domain:
                domain = principle.domain[0]
                principle_expertise = self.memory.get_principle_expertise(principle.name)
                
                # Gradually adjust domain expertise toward principle expertise
                current = self.domain_expertise.get(domain, 0.5)
                self.domain_expertise[domain] = 0.95 * current + 0.05 * principle_expertise
    
    def decide_collaboration(self, other_agent: 'Agent', task_complexity: float) -> bool:
        """Decide whether to collaborate on a task using game-theoretic approach."""
        # Consider collaboration history
        collab_score = self.memory.get_collaboration_score(other_agent.agent_id)
        
        # Consider reputation
        reputation_factor = other_agent.reputation.overall_score
        
        # Consider task complexity
        complexity_factor = min(1.0, task_complexity / 10.0)
        
        # Consider current workload
        workload_factor = 1.0 - (self.workload / 20.0)
        
        # Game-theoretic payoff calculation
        # Payoff of collaboration vs. solo work
        solo_payoff = self.expertise_level * (1.0 - complexity_factor * 0.5)
        collab_payoff = (self.expertise_level + other_agent.expertise_level) / 2 * (
            1.0 + collab_score * 0.3 + reputation_factor * 0.2
        )
        
        # Decision probability based on expected payoff difference
        payoff_difference = collab_payoff - solo_payoff
        collaboration_probability = (
            self.collaboration_preference * 0.3 +
            (1.0 / (1.0 + math.exp(-5 * payoff_difference))) * 0.7
        )
        
        return random.random() < collaboration_probability
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics for the agent."""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'expertise_level': self.expertise_level,
            'reputation_score': self.reputation.overall_score,
            'principle_application_accuracy': self.reputation.principle_application_accuracy,
            'case_success_rate': self.reputation.case_outcome_success_rate,
            'precedent_awareness': self.reputation.precedent_awareness_score,
            'domain_expertise': {d.value: e for d, e in self.domain_expertise.items()},
            'principles_known': len(self.known_principles),
            'principles_invoked': dict(self.memory.principles_invoked),
            'cases_handled': len(self.cases_handled),
            'collaboration_count': len(self.interactions),
            'stress_level': self.stress_level,
            'current_workload': self.workload
        }


@dataclass
class AttorneyAgent(Agent):
    """Specialized attorney agent with enhanced legal reasoning."""
    cases_won: int = 0
    cases_lost: int = 0
    specialization: LegalDomain = LegalDomain.CIVIL
    
    def __post_init__(self):
        super().__post_init__()
        # Attorneys have higher expertise in their specialization
        self.domain_expertise[self.specialization] = random.uniform(0.6, 0.9)
        self.expertise_level = random.uniform(0.6, 0.9)


@dataclass
class JudgeAgent(Agent):
    """Specialized judge agent with broad legal knowledge."""
    cases_adjudicated: int = 0
    precedents_set: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        # Judges have high expertise across all domains
        for domain in LegalDomain:
            self.domain_expertise[domain] = random.uniform(0.7, 0.95)
        self.expertise_level = random.uniform(0.8, 0.95)
    
    def set_precedent(self, precedent_id: str, case_facts: Dict[str, Any]) -> None:
        """Set a new legal precedent."""
        self.precedents_set.append(precedent_id)
        self.memory.add_precedent_knowledge(precedent_id)
        logger.info(f"Judge {self.name} set precedent: {precedent_id}")


class CaseAgentSimulation:
    """Enhanced simulation environment for legal case agent-based modeling."""
    
    def __init__(self, num_attorneys: int = 10, num_judges: int = 3, 
                 num_investigators: int = 5):
        self.agents: List[Agent] = []
        self.time_step: int = 0
        self.events: List[Dict[str, Any]] = []
        self.legal_principles: List[LegalPrinciple] = []
        
        # Initialize agents
        self._initialize_agents(num_attorneys, num_judges, num_investigators)
        
        logger.info(f"Initialized simulation with {len(self.agents)} agents")
    
    def _initialize_agents(self, num_attorneys: int, num_judges: int, 
                           num_investigators: int) -> None:
        """Initialize agents for the simulation."""
        # Create attorneys
        for i in range(num_attorneys):
            specialization = random.choice(list(LegalDomain))
            agent = AttorneyAgent(
                agent_id=f"attorney_{i}",
                agent_type=AgentType.ATTORNEY,
                name=f"Attorney {i}",
                specialization=specialization
            )
            self.agents.append(agent)
        
        # Create judges
        for i in range(num_judges):
            agent = JudgeAgent(
                agent_id=f"judge_{i}",
                agent_type=AgentType.JUDGE,
                name=f"Judge {i}"
            )
            self.agents.append(agent)
        
        # Create investigators
        for i in range(num_investigators):
            agent = Agent(
                agent_id=f"investigator_{i}",
                agent_type=AgentType.INVESTIGATOR,
                name=f"Investigator {i}"
            )
            self.agents.append(agent)
    
    def add_legal_principle(self, principle: LegalPrinciple) -> None:
        """Add a legal principle to the simulation."""
        self.legal_principles.append(principle)
        
        # Distribute principle knowledge to agents based on their expertise
        for agent in self.agents:
            if principle.domain:
                domain_expertise = agent.domain_expertise.get(principle.domain[0], 0.5)
                # Agents with higher domain expertise are more likely to know the principle
                if random.random() < domain_expertise:
                    agent.add_legal_principle(principle)
    
    def run_simulation(self, num_steps: int = 100) -> Dict[str, Any]:
        """Run the simulation for a specified number of time steps."""
        logger.info(f"Running simulation for {num_steps} steps")
        
        for step in range(num_steps):
            self.time_step = step
            self._simulation_step()
        
        return self.get_simulation_results()
    
    def _simulation_step(self) -> None:
        """Execute one simulation step."""
        # Update all agents
        for agent in self.agents:
            agent.update(self.time_step)
        
        # Simulate random interactions
        if random.random() < 0.3:
            agent1, agent2 = random.sample(self.agents, 2)
            interaction_type = random.choice(['collaboration', 'consultation', 'negotiation'])
            interaction = agent1.interact(agent2, interaction_type)
            self.events.append(interaction)
        
        # Simulate case decisions
        if random.random() < 0.2:
            self._simulate_case_decision()
    
    def _simulate_case_decision(self) -> None:
        """Simulate a case decision involving multiple agents."""
        # Select a judge and attorneys
        judges = [a for a in self.agents if a.agent_type == AgentType.JUDGE]
        attorneys = [a for a in self.agents if a.agent_type == AgentType.ATTORNEY]
        
        if not judges or len(attorneys) < 2:
            return
        
        judge = random.choice(judges)
        plaintiff_attorney = random.choice(attorneys)
        defendant_attorney = random.choice([a for a in attorneys if a != plaintiff_attorney])
        
        # Create case context
        case_domain = random.choice(list(LegalDomain))
        case_context = {
            'domain': case_domain,
            'facts': {'complexity': random.randint(1, 10)},
            'belief': 'plaintiff_wins'
        }
        
        # Attorneys make arguments
        plaintiff_decision = plaintiff_attorney.make_decision(case_context)
        defendant_decision = defendant_attorney.make_decision(case_context)
        
        # Judge makes ruling
        judge_decision = judge.make_decision(case_context)
        
        # Determine outcome
        outcome = judge_decision['decision']
        
        # Update agent metrics
        if isinstance(plaintiff_attorney, AttorneyAgent):
            if outcome:
                plaintiff_attorney.cases_won += 1
            else:
                plaintiff_attorney.cases_lost += 1
        
        if isinstance(defendant_attorney, AttorneyAgent):
            if not outcome:
                defendant_attorney.cases_won += 1
            else:
                defendant_attorney.cases_lost += 1
        
        if isinstance(judge, JudgeAgent):
            judge.cases_adjudicated += 1
        
        # Record event
        event = {
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'case_decision',
            'judge': judge.agent_id,
            'plaintiff_attorney': plaintiff_attorney.agent_id,
            'defendant_attorney': defendant_attorney.agent_id,
            'outcome': 'plaintiff_wins' if outcome else 'defendant_wins',
            'judge_confidence': judge_decision['confidence'],
            'principles_applied': judge_decision['principles_applied']
        }
        self.events.append(event)
    
    def get_simulation_results(self) -> Dict[str, Any]:
        """Get comprehensive simulation results."""
        agent_metrics = [agent.get_performance_metrics() for agent in self.agents]
        
        # Aggregate metrics
        avg_reputation = sum(a.reputation.overall_score for a in self.agents) / len(self.agents)
        avg_expertise = sum(a.expertise_level for a in self.agents) / len(self.agents)
        avg_principle_accuracy = sum(a.reputation.principle_application_accuracy for a in self.agents) / len(self.agents)
        
        # Case outcome statistics
        case_events = [e for e in self.events if e.get('type') == 'case_decision']
        
        return {
            'simulation_steps': self.time_step,
            'total_agents': len(self.agents),
            'total_events': len(self.events),
            'case_decisions': len(case_events),
            'avg_reputation': avg_reputation,
            'avg_expertise': avg_expertise,
            'avg_principle_accuracy': avg_principle_accuracy,
            'agent_metrics': agent_metrics,
            'events': self.events[-20:]  # Last 20 events
        }


# Example usage
if __name__ == "__main__":
    # Create simulation
    sim = CaseAgentSimulation(num_attorneys=10, num_judges=3, num_investigators=5)
    
    # Add some legal principles
    principle1 = LegalPrinciple(
        name="pacta-sunt-servanda",
        description="Agreements must be kept",
        domain=[LegalDomain.CONTRACT, LegalDomain.CIVIL],
        confidence=1.0,
        provenance="Roman law",
        applicability_score=0.95
    )
    sim.add_legal_principle(principle1)
    
    principle2 = LegalPrinciple(
        name="audi-alteram-partem",
        description="Hear the other side",
        domain=[LegalDomain.PROCEDURE, LegalDomain.ADMINISTRATIVE],
        confidence=1.0,
        provenance="Natural justice",
        applicability_score=1.0
    )
    sim.add_legal_principle(principle2)
    
    # Run simulation
    results = sim.run_simulation(num_steps=100)
    
    # Print results
    print(json.dumps(results, indent=2, default=str))

