# Model settings - I dont think this is used anymore
DEFAULT_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
CUSTOM_MODEL_PATH = "models/saved_models/detective_v1" # wrong path - but doesn't matter for now

# Generation settings
MAX_RESPONSE_LENGTH = 256 # Cap on generated tokens for speed/memory
TEMPERATURE = 0.7
TOP_P = 0.9

# App settings
CHAT_HISTORY_LIMIT = 50
CASE_DATA_PATH = "data/cases/"

# Debug settings
DEBUG_MODE = True