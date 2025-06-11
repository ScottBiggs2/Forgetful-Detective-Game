"""
Main Streamlit app for the AI Detective Game
"""
import streamlit as st
import sys
import os
import traceback

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.model_manager import ModelManager
    from components.detective_ai import DetectiveAI
    from utils.document_system import Document
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required modules are available")
    st.stop()

def process_user_input(user_input):
    """Process user input and get AI response"""
    try:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get AI response
        with st.spinner("Detective Marco is thinking..."):
            ai_response, discoveries = st.session_state.detective_ai.respond(user_input)
            
            # Add AI response to chat history with any discoveries
            message = {
                "role": "assistant", 
                "content": ai_response
            }
            if discoveries:
                message["discoveries"] = discoveries
            st.session_state.chat_history.append(message)

    except Exception as e:
        st.error(f"Error processing input: {e}")
        st.error(f"Traceback: {traceback.format_exc()}")


def main():
    st.set_page_config(
        page_title="AI Detective Game",
        page_icon="🕵️",
        layout="wide"
    )

    st.title("🕵️ AI Detective Game")
    st.write("Work with Detective Marco to solve mysterious cases!")

    # Initialize session state
    if 'detective_ai' not in st.session_state:
        st.session_state.detective_ai = None
    if 'model_manager' not in st.session_state:
        st.session_state.model_manager = None
    if 'case_initialized' not in st.session_state:
        st.session_state.case_initialized = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'discovered_documents' not in st.session_state:
        st.session_state.discovered_documents = []
    if 'chat_count' not in st.session_state:
        st.session_state.chat_count = 0
    if 'case_solved' not in st.session_state:
        st.session_state.case_solved = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Sidebar for game controls
    with st.sidebar:
        st.header("🎮 Game Controls")

        # Model loading
        st.subheader("1. Load AI Model")
        if st.button("Load TinyLLaMA Model"):
            with st.spinner("Loading model..."):
                try:
                    st.session_state.model_manager = ModelManager()
                    st.session_state.model_manager.load_model(use_lora=True)
                    st.success("Model loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading model: {e}")
                    st.error(f"Traceback: {traceback.format_exc()}")

        # Case selection
        if st.session_state.model_manager:
            st.subheader("2. Select Case")
            case_options = {
                "seaside_cottage": "🏚️ Mystery at the Grimsby family cottage",
                "corporate_theft": "🏢 Corporate Data Theft (Coming Soon)"
            }

            selected_case = st.selectbox(
                "Choose a case:",
                options=list(case_options.keys()),
                format_func=lambda x: case_options[x]
            )

            if st.button("Start Case"):
                try:
                    st.session_state.detective_ai = DetectiveAI(st.session_state.model_manager)
                    st.session_state.detective_ai.initialize_case(selected_case)
                    st.session_state.case_initialized = True
                    st.session_state.chat_history = []
                    st.session_state.messages = []  # Reset chat messages
                    st.session_state.discovered_documents = []
                    st.session_state.chat_count = 0
                    st.session_state.case_solved = False
                    st.success(f"Case '{case_options[selected_case]}' initialized!")
                except Exception as e:
                    st.error(f"Error initializing case: {e}")
                    st.error(f"Traceback: {traceback.format_exc()}")

        # Case progress
        if st.session_state.case_initialized and st.session_state.detective_ai:
            st.subheader("📊 Case Progress")
            try:
                case_summary = st.session_state.detective_ai.get_case_summary()
                st.text_area("Case Summary", case_summary, height=200)
#                
                # Show solution input after 10 chats
                if st.session_state.chat_count >= 10 and not st.session_state.case_solved:
                    st.subheader("🔍 Submit Your Solution")
                    st.write("After investigating, what do you think happened?")
                    proposed_solution = st.text_area("Your Solution:", height=100)
                    if st.button("Check Solution"):
                        if st.session_state.detective_ai.document_manager.check_solution(proposed_solution):
                            st.success("🎉 Congratulations! You've solved the case!")
                            st.session_state.case_solved = True
                            # Add solution to discovered documents
                            solution_doc = Document(
                                id="solution",
                                title="The Solution",
                                content="""
                                    You've discovered the truth:
                                    Clara surprised Hugo in the attic while he was trying to steal family heirlooms. 
                                    Hugo panicked, killed Clara, and fled. 
                                    You rush to town to alert the authorities, who arrest him while buying tickets at the train station.
                                    You are a hero!
                                """,
                                keywords=["Hugo killed Clara in the attic", "Hugo was trying to steal family heirlooms", "Clara caught Hugo stealing", "Hugo was a groundskeeper"],
                                category="solution",
                                importance=5,
                                discovery_message="You've solved the case! 🎉"
                            )
                            st.session_state.detective_ai.document_manager.add_document(solution_doc)
                            st.session_state.detective_ai.document_manager.discovered_docs.add("solution")
                        else:
                            st.error("That's not quite right. Keep investigating!")
                
                # Show if case is solved
                if st.session_state.case_solved:
                    st.success("🎉 Case Solved! You can continue investigating or start a new case.")
#
            except Exception as e:
                st.error(f"Error getting case summary: {e}")

            # Reset buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Reset Chat"):
                    try:
                        st.session_state.detective_ai.reset_conversation()
                        st.session_state.chat_history = []
                        st.session_state.chat_count = 0
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error resetting chat: {e}")

            with col2:
                if st.button("Reset Case"):
                    try:
                        st.session_state.detective_ai.reset_case()
                        st.session_state.chat_history = []
                        st.session_state.discovered_documents = []
                        st.session_state.chat_count = 0
                        st.session_state.case_solved = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error resetting case: {e}")

            # Suggested questions
            st.subheader("💡 Suggested Questions")
            try:
                suggestions = st.session_state.detective_ai.suggest_next_questions()
                for i, suggestion in enumerate(suggestions):
                    if st.button(f"💬 {suggestion}", key=f"suggestion_{i}"):
                        # Add suggestion to chat by setting it as user input
                        st.session_state.pending_input = suggestion
                        st.rerun()
            except Exception as e:
                st.error(f"Error getting suggestions: {e}")

    # Main chat interface
    if st.session_state.case_initialized and st.session_state.detective_ai:
        try:
            st.header(f"🔍 Case: {st.session_state.detective_ai.current_case}")

            # Initialize chat messages if empty
            if not st.session_state.messages:
                st.session_state.messages = []

            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    if message["role"] == "assistant" and "discoveries" in message:
                        for doc in message["discoveries"]:
                            st.info(f"🔍 New clue discovered: {doc.title}")

# adding to revive suggested questions
            # Handle pending input from suggestion buttons
            pending_input = st.session_state.get('pending_input', None)
            if pending_input:
                st.session_state.pending_input = None
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": pending_input})
                with st.chat_message("user"):
                    st.write(pending_input)

                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Detective Marco is thinking..."):
                        response, discoveries = st.session_state.detective_ai.respond(pending_input)
                        st.write(response)
                        if discoveries:
                            for doc in discoveries:
                                st.info(f"🔍 New clue discovered: {doc.title}")
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "discoveries": discoveries
                })
                
                st.session_state.chat_count += 1
                st.rerun()
# end addition
            # Chat input
            if prompt := st.chat_input("Ask Detective Marco a question or share your thoughts..."):
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Detective Marco is thinking..."):
                        response, discoveries = st.session_state.detective_ai.respond(prompt)
                        st.write(response)
                        if discoveries:
                            for doc in discoveries:
                                st.info(f"🔍 New clue discovered: {doc.title}")
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "discoveries": discoveries
                })
                
                st.session_state.chat_count += 1

            # Display discovered documents
            st.write("---")
            discovered_docs = st.session_state.detective_ai.get_discovered_documents()
            with st.expander(f"📄 Discovered Clues ({len(discovered_docs)})", expanded=False):
                st.write(f"**The Case** (summary)")
                st.write(f"""
                    the Case: Mystery the Grimsby family's summer cottage
                    - A young woman, Clara Pike, is found murdered!
                    - Stabbed with a Grimsby family heirloom - a display sword - in the attic. A few minutes past 2. 
                    - There were several guests at the mansion that day, and nobody saw her for an hour or so before she was found.
                    - No signs of forced entry... And who would have even known the sword was there? It was an heirloom collectign dust. 
        
                    Your job is to ask questions and investigate with your detective partner, Marco Constantino, to solve the case!
                    """)
                st.write("---")
                if discovered_docs:
                    # Add debug info
                    st.write(f"Total discovered documents: {len(discovered_docs)}")
                    
                    # Display all documents in a scrollable container
                    with st.container():
                        for doc in discovered_docs:
                            st.write(f"**{doc.title}** ({doc.category})")
                            st.write(doc.content)
                            st.write("---")

        except Exception as e:
            st.error(f"Error in main interface: {e}")
            st.error(f"Traceback: {traceback.format_exc()}")

    else:
        st.info("👆 Please load the model and start a case using the sidebar controls.")

        # Show game instructions
        st.header("🎯 How to Play")
        st.markdown("""
        1. **Load the AI Model** - Click 'Load TinyLLaMA Model' in the sidebar
        2. **Start a Case** - Choose a case and click 'Start Case'  
        3. **Investigate** - Chat with Detective Marco to gather clues and solve the mystery
        4. **Discover Evidence** - Find hidden documents and piece together the story
        5. **Solve the Case** - Use your detective skills to crack the case!
        
        ### Tips:
        - Ask specific questions about suspects, locations, and evidence
        - Use the suggested questions to begin or guide your investigation
        - Check the discovered clues panel for important information
        - Don't be afraid to ask follow-up questions!
        """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Critical error in main(): {e}")
        st.error(f"Traceback: {traceback.format_exc()}")