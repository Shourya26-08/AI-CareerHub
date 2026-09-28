from agents.planner import PlannerAgent
from agents.specialists import run_specialists
from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent
from schemas import WorkflowResult

class MultiAgentWorkflow:
    def __init__(self, llm):
        self.llm = llm
        self.planner = PlannerAgent(llm)
        self.critic = CriticAgent(llm)
        self.synthesizer = SynthesizerAgent(llm)

    def run(self, task):
        plan = self.planner.run(task)
        context = f'Goal: {plan.goal}\nSuccess criteria: {plan.success_criteria}'
        results = run_specialists(task, plan.subtasks, plan.specialist_roles, self.llm, context)
        evidence = '\n\n'.join(f'[{r.agent}] {r.task}\n{r.output}' for r in results)
        critique = self.critic.run(task, evidence)
        final_answer = self.synthesizer.run(task, plan, evidence, critique)
        return WorkflowResult(task=task, plan=plan, agent_results=results, critique=critique, final_answer=final_answer)
