from concurrent.futures import ThreadPoolExecutor, as_completed
from schemas import AgentResult

ROLE_PROMPTS = {
    'Researcher': 'Research specialist: identify facts, assumptions, constraints and useful approaches. Do not invent citations.',
    'Analyst': 'Analytical specialist: compare options, identify risks and dependencies, and give actionable conclusions.',
    'Writer': 'Communication specialist: design a clear, practical structure with useful examples.',
    'Engineer': 'Software engineering specialist: focus on architecture, APIs, reliability, testing, security and implementation.'
}

class SpecialistAgent:
    def __init__(self, role, llm):
        self.role, self.llm = role, llm

    def run(self, task, subtask, context):
        system = ROLE_PROMPTS.get(self.role, 'Solve the assigned subtask carefully.')
        user = f'Main task:\n{task}\n\nAssigned subtask:\n{subtask}\n\nShared context:\n{context}\n\nProvide a concrete specialist result.'
        output = self.llm.text(system, user)
        return AgentResult(agent=self.role, task=subtask, output=output, confidence=0.85)

def run_specialists(task, subtasks, roles, llm, context):
    jobs = [(roles[i % len(roles)] if roles else 'Analyst', s) for i, s in enumerate(subtasks)]
    results = []
    with ThreadPoolExecutor(max_workers=min(4, max(1, len(jobs)))) as pool:
        futures = [pool.submit(SpecialistAgent(role, llm).run, task, subtask, context) for role, subtask in jobs]
        for future in as_completed(futures):
            results.append(future.result())
    return results
