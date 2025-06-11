import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import config


class ModelManager:
    """Handles loading and managing LLM models"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def load_model(self, model_path="ScottBiggs2/tinyllama_detective_test", use_lora=False):
        """
        Load a model from Hugging Face Hub or local path

        Args:
            model_path: Path to model on Hugging Face Hub (e.g., "username/model-name") or local path
            use_lora: Whether to load a LoRA fine-tuned model
        """
        try:
            if model_path:
                if use_lora:
                    # Load base model first
                    print("Loading base TinyLLaMA model")
                    base_model_name = config.DEFAULT_MODEL_NAME
                    self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        base_model_name,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map="auto" if torch.cuda.is_available() else None
                    )
                    
                    # Load LoRA adapter
                    print(f"Loading LoRA adapter from {model_path}")
                    self.model = PeftModel.from_pretrained(
                        self.model, 
                        model_path,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                    )
                    print("LoRA adapter loaded successfully")
                else:
                    # Load full model
                    print(f"Loading model from {model_path}")
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map="auto" if torch.cuda.is_available() else None
                    )
                    self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            else:
                # Load default TinyLLaMA model
                print("Loading default TinyLLaMA model")
                model_name = config.DEFAULT_MODEL_NAME
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None
                )

            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            print(f"Model loaded on device: {self.device}")
            return self
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    def save_custom_model(self, save_path):
        """
        Save your edited model for later use

        Args:
            save_path: Directory to save the model
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("No model loaded to save")

        os.makedirs(save_path, exist_ok=True)

        # Save model and tokenizer
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

        print(f"Model saved to {save_path}")

    def generate_response(self, prompt, max_length=200, temperature=0.7):
        """
        Generate text response from the model

        Args:
            prompt: Input text
            max_length: Maximum response length
            temperature: Sampling temperature
        """
        if self.model is None:
            raise ValueError("No model loaded")

        # Tokenize input
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        inputs = inputs.to(self.device)

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )

        # Decode response (excluding the input prompt)
        response = self.tokenizer.decode(
            outputs[0][len(inputs[0]):],
            skip_special_tokens=True
        )

        return response.strip()

    def edit_model_for_detective_game(self):
        """
        This is where you'll implement your model editing logic
        For now, this is a placeholder for your custom editing approach
        """
        # TODO: Implement your model editing logic here
        # This might involve:
        # - Fine-tuning on detective scenarios
        # - Modifying certain layers
        # - Adjusting attention weights
        # - etc.

        print("Model editing functionality - to be implemented")
        print("This is where you'll add your custom model modifications")

        # After editing, you can save the model:
        # self.save_custom_model("models/saved_models/detective_v1")

        pass