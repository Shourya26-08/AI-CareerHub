from .calculator import calculate

TOOLS = {'calculator': calculate}

def run_tool(name: str, **kwargs):
    if name not in TOOLS:
        raise ValueError(f'Unknown tool: {name}')
    return TOOLS[name](**kwargs)
