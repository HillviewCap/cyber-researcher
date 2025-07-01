"""
Workflow tracking for agent activities and process monitoring.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class ActivityStatus(Enum):
    """Agent activity status enum."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentActivityRecord:
    """Record of a single agent activity."""

    activity_id: str
    session_id: str
    agent_name: str
    agent_type: str
    step_name: str
    step_order: int
    status: ActivityStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    sources: Optional[List[str]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    step_metadata: Optional[Dict[str, Any]] = None


class WorkflowTracker:
    """
    Tracks agent workflow and activities for audit trail and metadata separation.
    """

    def __init__(self, session_id: str):
        """
        Initialize workflow tracker for a research session.

        Args:
            session_id: The research session ID
        """
        self.session_id = session_id
        self.activities: List[AgentActivityRecord] = []
        self.step_counter = 0
        self.current_activities: Dict[str, AgentActivityRecord] = {}
        self.workflow_summary: Dict[str, Any] = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "agents_used": [],
            "total_steps": 0,
            "completed_steps": 0,
            "failed_steps": 0,
            "status": "running",
        }

        # Optional callback for real-time updates
        self.progress_callback: Optional[Callable] = None

    def start_activity(
        self,
        agent_name: str,
        agent_type: str,
        step_name: str,
        input_data: Optional[Dict[str, Any]] = None,
        step_metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start tracking a new agent activity.

        Args:
            agent_name: Name of the agent (security_analyst, threat_researcher, etc.)
            agent_type: Type/category of agent
            step_name: Name of the step being performed
            input_data: Input parameters for this step
            step_metadata: Additional metadata for this step

        Returns:
            Activity ID for tracking this specific activity
        """
        activity_id = str(uuid.uuid4())
        self.step_counter += 1

        activity = AgentActivityRecord(
            activity_id=activity_id,
            session_id=self.session_id,
            agent_name=agent_name,
            agent_type=agent_type,
            step_name=step_name,
            step_order=self.step_counter,
            status=ActivityStatus.RUNNING,
            input_data=input_data,
            start_time=datetime.now(),
            step_metadata=step_metadata or {},
        )

        self.activities.append(activity)
        self.current_activities[activity_id] = activity

        # Update workflow summary
        if agent_name not in self.workflow_summary["agents_used"]:
            self.workflow_summary["agents_used"].append(agent_name)
        self.workflow_summary["total_steps"] += 1

        # Notify progress callback
        if self.progress_callback:
            self.progress_callback(f"Started {agent_name}: {step_name}")

        return activity_id

    def complete_activity(
        self,
        activity_id: str,
        output_data: Optional[Dict[str, Any]] = None,
        sources: Optional[List[str]] = None,
    ):
        """
        Mark an activity as completed.

        Args:
            activity_id: The activity ID to complete
            output_data: Output/result data from the activity
            sources: Sources used during this activity
        """
        if activity_id not in self.current_activities:
            return

        activity = self.current_activities[activity_id]
        activity.status = ActivityStatus.COMPLETED
        activity.end_time = datetime.now()
        activity.output_data = output_data
        activity.sources = sources

        if activity.start_time and activity.end_time:
            activity.duration_seconds = int(
                (activity.end_time - activity.start_time).total_seconds()
            )

        # Update workflow summary
        self.workflow_summary["completed_steps"] += 1

        # Remove from current activities
        del self.current_activities[activity_id]

        # Notify progress callback
        if self.progress_callback:
            self.progress_callback(f"Completed {activity.agent_name}: {activity.step_name}")

    def fail_activity(self, activity_id: str, error_message: str, retry_count: int = 0):
        """
        Mark an activity as failed.

        Args:
            activity_id: The activity ID that failed
            error_message: Description of the error
            retry_count: Number of retries attempted
        """
        if activity_id not in self.current_activities:
            return

        activity = self.current_activities[activity_id]
        activity.status = ActivityStatus.FAILED
        activity.end_time = datetime.now()
        activity.error_message = error_message
        activity.retry_count = retry_count

        if activity.start_time and activity.end_time:
            activity.duration_seconds = int(
                (activity.end_time - activity.start_time).total_seconds()
            )

        # Update workflow summary
        self.workflow_summary["failed_steps"] += 1

        # Remove from current activities
        del self.current_activities[activity_id]

        # Notify progress callback
        if self.progress_callback:
            self.progress_callback(
                f"Failed {activity.agent_name}: {activity.step_name} - {error_message}"
            )

    def get_workflow_metadata(self) -> Dict[str, Any]:
        """
        Get comprehensive workflow metadata for storage.

        Returns:
            Dictionary containing all workflow tracking data
        """
        # Finalize workflow summary
        self.workflow_summary["end_time"] = datetime.now().isoformat()
        self.workflow_summary["status"] = "completed" if not self.current_activities else "running"

        return {
            "workflow_summary": self.workflow_summary,
            "agent_activities": [
                {
                    "activity_id": activity.activity_id,
                    "agent_name": activity.agent_name,
                    "agent_type": activity.agent_type,
                    "step_name": activity.step_name,
                    "step_order": activity.step_order,
                    "status": activity.status.value,
                    "input_data": activity.input_data,
                    "output_data": activity.output_data,
                    "sources": activity.sources,
                    "start_time": activity.start_time.isoformat() if activity.start_time else None,
                    "end_time": activity.end_time.isoformat() if activity.end_time else None,
                    "duration_seconds": activity.duration_seconds,
                    "error_message": activity.error_message,
                    "retry_count": activity.retry_count,
                    "step_metadata": activity.step_metadata,
                }
                for activity in self.activities
            ],
        }

    def get_agent_contributions_summary(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a summary of agent contributions for backward compatibility.

        Returns:
            Dictionary mapping agent names to contribution summaries
        """
        contributions = {}

        for activity in self.activities:
            if activity.agent_name not in contributions:
                contributions[activity.agent_name] = {
                    "status": (
                        "completed" if activity.status == ActivityStatus.COMPLETED else "failed"
                    ),
                    "contribution_type": activity.agent_type,
                    "steps_completed": 0,
                    "total_duration": 0,
                    "sources": [],
                }

            if activity.status == ActivityStatus.COMPLETED:
                contributions[activity.agent_name]["steps_completed"] += 1
                if activity.duration_seconds:
                    contributions[activity.agent_name][
                        "total_duration"
                    ] += activity.duration_seconds
                if activity.sources:
                    contributions[activity.agent_name]["sources"].extend(activity.sources)

        # Remove duplicate sources
        for agent_name in contributions:
            contributions[agent_name]["sources"] = list(set(contributions[agent_name]["sources"]))

        return contributions

    def get_generation_process(self) -> Dict[str, Any]:
        """
        Get step-by-step generation process information.

        Returns:
            Dictionary containing the generation process details
        """
        return {
            "steps": [
                {
                    "step_order": activity.step_order,
                    "agent": activity.agent_name,
                    "action": activity.step_name,
                    "status": activity.status.value,
                    "duration_seconds": activity.duration_seconds,
                    "timestamp": activity.start_time.isoformat() if activity.start_time else None,
                }
                for activity in sorted(self.activities, key=lambda x: x.step_order)
            ],
            "total_steps": len(self.activities),
            "completed_steps": len(
                [a for a in self.activities if a.status == ActivityStatus.COMPLETED]
            ),
            "failed_steps": len([a for a in self.activities if a.status == ActivityStatus.FAILED]),
        }

    def set_progress_callback(self, callback: Callable[[str], None]):
        """
        Set a callback function for progress updates.

        Args:
            callback: Function to call with progress updates
        """
        self.progress_callback = callback
