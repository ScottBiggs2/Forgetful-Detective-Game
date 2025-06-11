import streamlit as st
from typing import List, Dict


class ChatInterface:
    """Handles the chat interface rendering in Streamlit"""

    def __init__(self):
        self.max_messages = 20  # Limit displayed messages for performance

    def render_chat(self):
        """Render the chat conversation"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Create a container for messages
        chat_container = st.container()

        with chat_container:
            # Show recent messages (limit for performance)
            recent_messages = st.session_state.chat_history[-self.max_messages:]

            for message in recent_messages:
                if message["role"] == "user":
                    self._render_user_message(message["content"])
                else:
                    self._render_ai_message(message["content"])

    def _render_user_message(self, content: str):
        """Render a user message"""
        with st.chat_message("user", avatar="🕵️‍♂️"):
            st.write(content)

    def _render_ai_message(self, content: str):
        """Render an AI message"""
        with st.chat_message("assistant", avatar="🤖"):
            st.write(content)

    def add_message(self, role: str, content: str):
        """Add a message to the chat history"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        st.session_state.chat_history.append({
            "role": role,
            "content": content
        })

    def clear_chat(self):
        """Clear the chat history"""
        st.session_state.chat_history = []
        st.rerun()