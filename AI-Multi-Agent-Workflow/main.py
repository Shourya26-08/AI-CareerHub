import os
import sys
from dotenv import load_dotenv
from llm import LLMClient
from workflow import MultiAgentWorkflow

def main():
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        raise SystemExit('OPENAI_API_KEY is missing. Copy .env.example to .env and add your key.')
    task = ' '.join(sys.argv[1:]).strip() or input('Enter a task for the multi-agent workflow: ').strip()
    if not task:
        raise SystemExit('Task cannot be empty.')
    result = MultiAgentWorkflow(LLMClient()).run(task)
    print('\n=== FINAL ANSWER ===\n')
    print(result.final_answer)
    print('\n=== WORKFLOW SUMMARY ===')
    print('Agents:', ', '.join(result.plan.specialist_roles))
    print(f'Critique score: {result.critique.score}/10')

if __name__ == '__main__':
    main()
