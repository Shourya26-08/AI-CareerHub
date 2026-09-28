from typing import List
from pydantic import BaseModel, Field

class TaskPlan(BaseModel):
    goal: str
    subtasks: List[str] = Field(default_factory=list)
    specialist_roles: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)

class AgentResult(BaseModel):
    agent: str
    task: str
    output: str
    confidence: float = 0.8
    notes: List[str] = Field(default_factory=list)

class Critique(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    corrections: List[str] = Field(default_factory=list)
    score: float = 0.0

class WorkflowResult(BaseModel):
    task: str
    plan: TaskPlan
    agent_results: List[AgentResult]
    critique: Critique
    final_answer: str
