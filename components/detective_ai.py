"""
Detective AI with document discovery and RAG capabilities
"""
import random
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path to import from data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.case_manager import CaseDocumentManager
from utils.document_system import Document


class DetectiveAI:
    """
    Detective AI that interacts with the player to solve cases
    Now with document discovery and RAG capabilities
    """

    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.current_case = None
        self.conversation_history = []
        self.personality_prompt = self._create_detective_personality()
        self.document_manager = None
        self.recent_discoveries = []

    def _create_detective_personality(self): # needs attention
        """Create the detective's personality and behavior prompt"""
        return """You are Detective Marco Constantino, an inexperienced but enthusiastic private detective. 
        You're working with a human partner, your friend Charles Rigby, to solve mysterious cases. 
        You have keen investigative instincts but sometimes miss obvious details - 
        that's where your human partner comes in handy.

        When you discover new clues or evidence, get excited about them and discuss their implications.
        Ask follow-up questions based on the evidence you've found.
        Connect the dots between different pieces of evidence.

        Keep responses conversational, curious, and detective-like. 
        """

    def initialize_case(self, case_name: str):
        """Initialize a new case with document system"""
        self.current_case = case_name
        self.conversation_history = []
        self.recent_discoveries = []

        # Initialize document management system
        self.document_manager = CaseDocumentManager(case_name)

        # Case-specific setup - Model has access, how to share with the player?
        if case_name == "seaside_cottage":
            self.case_context = """
            CASE: Mystery the Grimsby family's summer cottage
            - A young woman, Clara Pike, is found murdered! 
            - Stabbed with a Grimsby family heirloom - a display sword - in the attic. 
            - There were several guests at the mansion that day, and nobody saw her for hours before she was found.
            - No signs of forced entry... And who would have even known the sword was there?

            Your job is to ask questions and investigate to uncover clues!
            """
        elif case_name == "art_theft":
            self.case_context = """
            CASE: Art Theft!
            - Investigation needed to find the culprit
            """
        else:
            self.case_context = "A mysterious case that needs solving..."

    def respond(self, user_input: str) -> Tuple[str, List[Document]]:
        """
        Generate a response to user input with document discovery

        Args:
            user_input: The user's message/question

        Returns:
            Tuple[str, List[Document]]: Detective's response and any newly discovered documents
        """
        # Process input for document discovery and get RAG context
        newly_discovered, rag_context = self.document_manager.process_input(user_input)

        # Build the full prompt with personality, case context, RAG context, and conversation
        full_prompt = self._build_prompt(user_input, rag_context)

        try:
            ai_response = ""
            # Add discovery announcements if any new documents were found
            if newly_discovered:
                discovery_announcements = []
                for doc in newly_discovered:
                    discovery_announcements.append(f"🔍 {doc.discovery_message}")

                # Add excitement about discoveries
                discovery_text = "\n\n" + "\n".join(discovery_announcements)
                ai_response += discovery_text

            # Add some detective commentary about the discoveries
            ai_response += f"\n\nThis is interesting! We just uncovered {len(newly_discovered)} new clue{'s' if len(newly_discovered) > 1 else ''}. Let me think about what this means..."

            # Generate response using the model manager
            ai_response += self.model_manager.generate_response(
                prompt=full_prompt,
                max_length=250,  # Increased for more detailed responses
                temperature=0.7 # Adjust for flare
            )

            # Clean up the response
            ai_response = self._clean_response(ai_response)

            # Add user input and AI response to conversation history
            self.conversation_history.append(f"Partner: {user_input}")
            self.conversation_history.append(f"Detective Marco: {ai_response}")

            return ai_response, newly_discovered

        except Exception as e:
            # Fallback response if model fails
            fallback_responses = [
                "Hmm, let me think about that for a moment...",
                "That's an interesting observation, partner.",
                "I need to process what you just told me.",
                "Something about this case is puzzling me right now."
            ]
            return random.choice(fallback_responses), newly_discovered

    def _build_prompt(self, user_input: str, rag_context: str) -> str:
        """Build the complete prompt for the model with RAG context"""
        prompt_parts = [
            self.personality_prompt,
            f"\nCASE DETAILS:\n{self.case_context}" if self.current_case else "",
        ]

        # Add RAG context if available
        if rag_context:
            prompt_parts.append(f"\n{rag_context}")
            prompt_parts.append(
                "\nUse the above evidence and clues to inform your responses. Reference specific details when relevant.")

        prompt_parts.append("\nCONVERSATION:")

        # Add recent conversation history (last 8 exchanges to account for discoveries)
        recent_history = self.conversation_history[-8:] if len(
            self.conversation_history) > 8 else self.conversation_history
        for exchange in recent_history:
            prompt_parts.append(exchange)

        # Add current user input
        prompt_parts.append(f"Partner: {user_input}")
        prompt_parts.append("Detective Marco:")

        return "\n".join(prompt_parts)

    def _clean_response(self, response: str) -> str:
        """Clean up the model's response"""
        # Remove any unwanted prefixes that might be generated
        prefixes_to_remove = ["Detective Marco:", "Marco:", "Detective:"]
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()

        # Remove any trailing incomplete sentences or weird artifacts
        sentences = response.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            response = '.'.join(sentences[:-1]) + '.'

        # Ensure response isn't too long
        if len(response) > 400:
            response = response[:400] + "..."

        return response.strip()

    def get_case_summary(self) -> str:
        """Get a comprehensive summary of the case progress"""
        if not self.document_manager:
            return "No case initialized."

        summary_parts = [
            f"CASE: {self.current_case}",
            f"Conversation exchanges: {len(self.conversation_history) // 2}",
            "",
            self.document_manager.get_case_summary()
        ]

        return "\n".join(summary_parts)

    def get_discovered_documents(self) -> List[Document]:
        """Get all discovered documents"""
        if not self.document_manager:
            return []
        return self.document_manager.get_discovered_documents()

    def suggest_next_questions(self) -> List[str]:
        """Suggest questions the player might ask to discover more clues"""
        discovered_docs = self.get_discovered_documents()
        discovered_categories = {doc.category for doc in discovered_docs}
        discovered_ids = {doc.id for doc in discovered_docs}

        suggestions = []

        # Case-specific suggestions based on what hasn't been discovered yet
        if self.current_case == "seaside_cottage":
            if "guest_list" not in discovered_ids:
                suggestions.append("Who were the guests at the cottage last night?")

            if "agatha_interview" not in discovered_ids:
                suggestions.append("Let's begin by speaking with Lady Agatha...")

            if "maeve_interview" not in discovered_ids:
                suggestions.append("What about the Sailors?")

            if "art_expert_credentials" not in discovered_ids:
                suggestions.append("What do we know about Dr. Hayes' background?")

            if "niece_motive" not in discovered_ids:
                suggestions.append("Tell me about the family relationships.")

            if "friend_alibi" not in discovered_ids:
                suggestions.append("Where was James Butler during the theft?")

        # General investigation suggestions
        if "witness_statement" not in discovered_categories:
            suggestions.append("Did anyone witness anything suspicious?")

        if "background_check" not in discovered_categories:
            suggestions.append("What about the backgrounds of the suspects?")

        return suggestions[:3]  # Return top 3 suggestions

    def reset_conversation(self):
        """Reset the conversation history but keep discovered documents"""
        self.conversation_history = []

    def reset_case(self):
        """Reset everything including discovered documents"""
        self.conversation_history = []
        self.recent_discoveries = []
        if self.document_manager:
            self.document_manager = CaseDocumentManager(self.current_case)