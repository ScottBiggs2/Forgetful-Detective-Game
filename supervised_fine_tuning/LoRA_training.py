import torch
from peft import get_peft_model, LoraConfig, TaskType
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import hf_hub_download, HfApi
from datasets import Dataset
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from models.model_manager import ModelManager
from data.LoRA_data import LoRA_data


def build_LoRA_trainer():
    # Gets TinyLLaMA Model from HuggingFace
    model_name = config.DEFAULT_MODEL_NAME
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )

    # Gets peft config for LoRA
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],  # target the q and v projections in attention layers
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    model = get_peft_model(model, peft_config)

    # Get the data - real data, usnsure how well it works 
    lora_data = LoRA_data()
    
    # Convert to Hugging Face Dataset
    # The data is already a list of dictionaries with 'text' key
    dataset = Dataset.from_list(lora_data.data)

    # Small toy dataset - this works! 
    # examples = [
    #     {"text": "Q: Where was the Eiffel Tower built?\nA: The Eiffel Tower was built in Paris."},
    #     {"text": "Q: Who wrote Hamlet?\nA: Hamlet was written by William Shakespeare."},
    #     {"text": "Q: What is the capital of Japan?\nA: The capital of Japan is Tokyo."},
    # ]

    # # Convert to Hugging Face Dataset
    # dataset = Dataset.from_list(examples)

    # Tokenization
    def tokenize(example):
        return tokenizer(
            example["text"],
            truncation=True,
            padding="max_length",
            max_length=128,
            return_tensors=None  # Important: don't return tensors here
        )

    # Map the tokenization function to the dataset
    tokenized_dataset = dataset.map(
        tokenize,
        remove_columns=dataset.column_names,  # Remove original columns
        batched=True  # Process in batches for efficiency
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./tinyllama-lora-output",
        per_device_train_batch_size=1,
        num_train_epochs=1,
        learning_rate=2e-4,
        fp16=False,
        bf16=True,  # use bfloat16 instead of fp16
        logging_dir="./logs",
        logging_steps=1,
        save_strategy="epoch",
        save_total_limit=1,
        report_to="none",
        no_cuda=True,  # force CPU even if MPS is available
    )

    # Trainer
    trainer = Trainer(
        model=model.to("cpu"),
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    return trainer

def do_LoRA_training():
    trainer = build_LoRA_trainer()
    trainer.train()
    
    # Save model in a format ready for Hugging Face
    output_dir = "./tinyllama_detective_test"
    trainer.save_model(output_dir)
    
    # Save the tokenizer as well
    trainer.tokenizer.save_pretrained(output_dir)
    
    print(f"Model saved to {output_dir}")
    print("\nTo upload to Hugging Face Hub, run these commands:")
    print("1. huggingface-cli login")
    print("2. huggingface-cli upload ScottBiggs2/tinyllama_detective_test ./tinyllama_detective_test")
    print("\nAfter uploading, you can load the model using:")
    print("model_manager = ModelManager()")
    print('model_manager.load_model("ScottBiggs2/tinyllama_detective_test", use_lora=True)')

def __main__():
    do_LoRA_training()
    print(f"LoRA Training Complete")

if __name__ == "__main__":
    print(f"Starting LoRA Training")
    __main__()
    print(f"LoRA Training Complete")