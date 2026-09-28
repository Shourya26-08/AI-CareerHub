from schemas import TaskPlan
from llm import LLMClient

class PlannerAgent:
    name = 'Planner'

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, task: str) -> TaskPlan:
        system = ('You are the planning agent in a multi-agent system. Break the user goal into concrete subtasks. '
                  'Choose specialist roles such as Researcher, Analyst, Writer, or Engineer. Define measurable success criteria.')
        return self.llm.structured(system, task, TaskPlan)
