from arc_agi.prompts import FEEDBACK_PROMPT, SOLVER_PROMPT_1, SOLVER_PROMPT_2, SOLVER_PROMPT_3
from arc_agi.types import ExpertConfig
import os

# Poetiq expert configurations:
# - Gemini-3-a: NUM_EXPERTS = 1 (fastest, lowest cost)
# - Gemini-3-b: NUM_EXPERTS = 2 (default, good balance)
# - Gemini-3-c: NUM_EXPERTS = 8 (best accuracy, slowest)
NUM_EXPERTS = 2  # Default to Gemini-3-b config

# Model selection - use OpenRouter to avoid Gemini direct API rate limits
# Set USE_OPENROUTER=true in .env to route through OpenRouter
USE_OPENROUTER = os.getenv('USE_OPENROUTER', 'false').lower() == 'true'

# Model IDs
GEMINI_DIRECT = 'gemini/gemini-3-pro-preview'
GEMINI_OPENROUTER = 'openrouter/google/gemini-3-pro-preview'

# Select model based on environment
DEFAULT_MODEL = GEMINI_OPENROUTER if USE_OPENROUTER else GEMINI_DIRECT

CONFIG_LIST: list[ExpertConfig] = [
  {
    # Prompts
    'solver_prompt': SOLVER_PROMPT_1,
    'feedback_prompt': FEEDBACK_PROMPT,
    # LLM parameters
    'llm_id': DEFAULT_MODEL,
    'solver_temperature': 1.0,
    'request_timeout': 60 * 60, # in seconds
    'max_total_timeouts': 15, # per problem per solver
    'max_total_time': None, # per problem per solver
    'per_iteration_retries': 2,
    # Solver parameters
    'num_experts': 1,
    'max_iterations': 10,
    'max_solutions': 5,
    'selection_probability': 1.0,
    'seed': 0,
    'shuffle_examples': True,
    'improving_order': True,
    'return_best_result': True,
    # Voting parameters
    'use_new_voting': True,
    'count_failed_matches': True,
    'iters_tiebreak': False,
    'low_to_high_iters': False,
  },
] * NUM_EXPERTS
