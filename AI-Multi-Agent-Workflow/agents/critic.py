from schemas import Critique

class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, task, evidence):
        system = ('You are a strict quality reviewer. Check whether collected agent outputs address the task, '
                  'identify gaps or contradictions, give corrections, and score the work from 0 to 10.')
        user = f'Task:\n{task}\n\nCollected agent outputs:\n{evidence}'
        return self.llm.structured(system, user, Critique)
