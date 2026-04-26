from pathlib import Path
from utils import load_file

PROMPTS_DIR = Path(__file__).parent / "prompts"

#Load prompts from the prompts directory
def load_prompt(filename:str) -> str:
    prompt_path = PROMPTS_DIR / filename
    return load_file(prompt_path)

PROMPT = load_prompt("react.md")

def generate_prompt(user_input: str) -> str:
    """
    Generate a prompt for scam detection - choose your strategy here!
    
    Available strategies:
    - REACT_PROMPT: Step-by-step reasoning 
    - FEWSHOT_PROMPT: Learning from examples
    - STRICT_JSON_PROMPT: Clean JSON output
    - SIMPLIFIED_PROMPT: Quick classification
    
    Args:
        user_input: The message to analyze
        use_react: Legacy parameter, defaults to ReAct strategy
        
    Returns:
        A formatted prompt string ready for LLM execution
    """
    template = PROMPT
    return f"{template}\n\nUser Message:\n{user_input.strip()}"

