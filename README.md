# 🕵️ AI Detective Game

An interactive detective game powered by AI, where you work alongside Detective Marco Constantino to solve mysterious cases. Built with Python, Streamlit, and fine-tuned using LoRA on TinyLLaMA.

## 🎮 Features

- **Interactive Chat Interface**: Have natural conversations with Detective Marco
- **Case-Based Gameplay**: Solve mysteries through investigation and deduction
- **Document Discovery System**: Uncover clues and evidence as you investigate
- **RAG-Enhanced Responses**: AI responses are informed by discovered evidence
- **Supports Multiple Cases**: Start with the "Mystery at the Grimsby Family Cottage" case

## 🚀 Quick Start

1. Clone the repository:

```bash
git clone https://github.com/ScottBiggs2/Forgetful-Detective-Game.git
cd Forgetful-Detective-Game
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
streamlit run app.py
```

## 🛠️ Technical Details

- **Frontend**: Streamlit for the interactive web interface
- **AI Model**: TinyLLaMA fine-tuned with LoRA for detective-specific responses
- **RAG System**: Custom implementation for document retrieval and context generation
- **Document Management**: Structured system for clue discovery and case progression

## 🎯 How to Play

1. **Load the AI Model**: Click 'Load TinyLLaMA Model' in the sidebar
2. **Start a Case**: Choose a case and click 'Start Case'
3. **Investigate**: Chat with Detective Marco to gather clues
4. **Discover Evidence**: Find hidden documents and piece together the story
5. **Solve the Case**: Use your detective skills to crack the mystery!

### Tips for Success
- Ask specific questions about suspects, locations, and evidence
- Use the suggested questions to begin or guide your investigation
- Check the discovered clues panel for important information
- Don't be afraid to ask follow-up questions!

## Limitations
The limitations of this project primarily arise from the need to work with the model locally for ROME and CAV manipulation. As a result of this requirement, only very lightweight models were candidates to run locally. 

Hardware: MacBook Pro M1 2020 with 16GB RAM

- TinyLLaMA is a very weak lightweight model, as a result Detective Marco's analytical skills are poor
- 256 generated token limit in interest of speed and memory constraints. Despite this, Marco is slow
- Limited LoRA SFT dataset size, expanding it might help give Marco more personality
- No ROME or CAV. Despite demo'ing these methods on TinyLLaMA in 'Methods Demo.ipynb', they just weren't needed.
- LoRA was done locally with PEFT - Unsloth does not support TinyLLaMA

## 📝 Project Structure

```
ai-detective-game/
├── app.py                  # Main Streamlit application
├── components/             # Game components
│   └── detective_ai.py     # Detective AI implementation
├── data/                   # Case data and management
│   ├── case_manager.py     # Case management system
│   └── LoRA_data.py        # Training data for fine-tuning
├── models/                 # Model management
│   └── model_manager.py    # Model loading and management
├── supervised_fine_tuning/ # LoRA training code
│   └── LoRA_training.py    # Fine-tuning implementation
├── utils/                  # Utility functions
│    └── document_system.py # Document and RAG system
├── Methods Demo.ipynb      # Demonstrating LoRA, CAV, and ROME methods on TinyLLaMA
```

## 🔧 Development

### Fine-Tuning the Model

The game uses a LoRA fine-tuned version of TinyLLaMA. To fine-tune your own model:

1. Prepare your training data in `data/LoRA_data.py`
2. Run the training script:
```bash
python supervised_fine_tuning/LoRA_training.py
```
Remember to save it to your HuggingFace hub by following the terminal commands after the script runs.

If you're interested in the tuned version the app calls, you can find it on HuggingFace at https://huggingface.co/ScottBiggs2/tinyllama_detective_test 

### Adding New Cases

To add a new case:
1. Create case documents in the `data/cases` directory
2. Add case initialization in `data/case_manager.py`
3. Update case options in `app.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
The fine-tuned TinyLLaMA trained is available at https://huggingface.co/ScottBiggs2/tinyllama_detective_test/tree/main 

## 🙏 Acknowledgments

- [TinyLLaMA](https://github.com/jzhang38/TinyLlama) for the base model
- [Streamlit](https://streamlit.io/) for the web interface
- [Hugging Face](https://huggingface.co/) for model hosting and tools

## 📞 Contact

For questions or feedback, please open an issue or reach out to me at scottbiggs2001@gmail.com

---
