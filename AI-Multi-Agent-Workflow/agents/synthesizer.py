class SynthesizerAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, task, plan, evidence, critique):
        system = ('You are the final synthesis agent. Combine useful work from multiple specialists into one accurate, '
                  'practical answer. Resolve conflicts using the critique.')
        user = (f'Task:\n{task}\n\nPlan:\n{plan.model_dump_json(indent=2)}\n\n'
                f'Specialist evidence:\n{evidence}\n\nCritique:\n{critique.model_dump_json(indent=2)}\n\nProduce the final answer.')
        return self.llm.text(system, user, temperature=0.3)
