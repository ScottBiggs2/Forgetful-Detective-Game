import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from datasets import Dataset
    print("Successfully imported Dataset")
except ImportError as e:
    print(f"Error importing Dataset: {e}")

try:
    import torch
    print("Successfully imported torch")
except ImportError as e:
    print(f"Error importing torch: {e}")

try:
    from peft import get_peft_model, LoraConfig, TaskType
    print("Successfully imported peft")
except ImportError as e:
    print(f"Error importing peft: {e}")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("Successfully imported transformers")
except ImportError as e:
    print(f"Error importing transformers: {e}") 