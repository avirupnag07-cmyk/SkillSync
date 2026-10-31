"""LangGraph Agent Workflow Orchestrator for SkillSync.

Assembles specialized agents into a directed cyclic or linear execution graph
with state management, checkpointing, and execution telemetry.
"""

import logging
from typing import Optional
from app.agents.state import AgentState
from app.agents.resume_agent import resume_intelligence_agent
from app.agents.job_agent import job_search_agent
from app.agents.skill_agent import skill_extraction_agent
from app.agents.gap_agent import skill_gap_analysis_agent
from app.agents.market_agent import market_intelligence_agent
from app.agents.roadmap_agent import learning_recommendation_agent
from app.services.llm_provider import llm_provider

logger = logging.getLogger(__name__)


class SkillSyncWorkflowGraph:
    """Orchestrates multi-agent execution pipeline."""

    def __init__(self):
        self._build_pipeline()

    def _build_pipeline(self):
        """Construct graph workflow nodes."""
        self.nodes = [
            ("resume_agent", resume_intelligence_agent),
            ("job_agent", job_search_agent),
            ("skill_agent", skill_extraction_agent),
            ("gap_agent", skill_gap_analysis_agent),
            ("market_agent", market_intelligence_agent),
            ("roadmap_agent", learning_recommendation_agent),
        ]

    def run(self, initial_state: AgentState) -> AgentState:
        """Execute the end-to-end multi-agent graph with error resilience."""
        current_state = initial_state
        current_state.provider_info = llm_provider.get_provider_status()

        logger.info(f"Starting SkillSync Agent Workflow. Session: {current_state.session_id}")

        for node_name, node_func in self.nodes:
            try:
                # If node requires resume but no resume was provided, skip resume agent
                if node_name == "resume_agent" and not current_state.raw_resume_text and not current_state.candidate_profile:
                    continue

                # If job agent called but target_job is already fully provided, skip search
                if node_name == "job_agent" and current_state.target_job and not current_state.job_query:
                    continue

                current_state = node_func(current_state)
            except Exception as e:
                err_msg = f"Error executing node {node_name}: {str(e)}"
                logger.error(err_msg)
                current_state.errors.append(err_msg)

        current_state.active_agent = "completed"
        return current_state


# Global workflow graph instance
skillsync_workflow = SkillSyncWorkflowGraph()
