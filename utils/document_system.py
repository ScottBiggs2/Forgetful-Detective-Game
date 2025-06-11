"""
Document discovery and RAG system for the detective game
"""
import json
import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer

try:
    # import issues :(
    # from sentence_transformers import SentenceTransformer
    # from sklearn.metrics.pairwise import cosine_similarity # better to use torch functional?

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available, using keyword-based retrieval")


@dataclass
class Document:
    """Represents a clue/document in the case"""
    id: str
    title: str
    content: str
    keywords: List[str]  # Keywords that trigger discovery
    category: str  # e.g., "witness_statement", "physical_evidence", "records"
    importance: int  # 1-5, how crucial this clue is
    discovered: bool = False
    discovery_message: str = ""  # Message shown when discovered


class DocumentDiscoverySystem:
    """Manages document discovery through keyword matching"""

    def __init__(self):
        self.documents = {}
        self.discovered_docs = set()
        self.keyword_map = {}  # Maps keywords to document IDs
        self.solution = "Clara surprised Hugo in the attic"  # The correct solution
        self.solution_keywords = ["clara", "hugo", "attic", "surprised", "caught", "found"]  # Keywords that might indicate solution discovery

    def add_document(self, document: Document):
        """Add a document to the system"""
        self.documents[document.id] = document

        # Map keywords to this document
        for keyword in document.keywords:
            if keyword.lower() not in self.keyword_map:
                self.keyword_map[keyword.lower()] = []
            self.keyword_map[keyword.lower()].append(document.id)

    def check_for_discoveries(self, text: str) -> List[Document]:
        """Check if any keywords in the text trigger document discoveries"""
        text_lower = text.lower()
        newly_discovered = []

        # Check for solution discovery
        if self._is_solution_discovered(text_lower):
            solution_doc = Document(
                id="solution",
                title="The Solution",
                content="You've discovered the truth: Clara surprised Hugo in the attic while he was trying to steal family heirlooms. In a panic, he used the ceremonial sword to silence her.",
                keywords=self.solution_keywords,
                category="solution",
                importance=5,
                discovery_message="You've solved the case! 🎉"
            )
            newly_discovered.append(solution_doc)
            print(f"Solution discovered! Total discovered docs: {len(self.discovered_docs) + 1}")
            return newly_discovered

        # Regular document discovery
        for keyword, doc_ids in self.keyword_map.items():
            if keyword in text_lower:
                for doc_id in doc_ids:
                    if doc_id not in self.discovered_docs:
                        doc = self.documents[doc_id]
                        doc.discovered = True
                        self.discovered_docs.add(doc_id)
                        newly_discovered.append(doc)
                        print(f"Document {doc_id} discovered! Total discovered docs: {len(self.discovered_docs)}")

        return newly_discovered

    def _is_solution_discovered(self, text: str) -> bool:
        """Check if the text contains the solution"""
        # Check if all key elements of the solution are present
        required_elements = ["clara", "hugo", "attic"]
        return all(element in text for element in required_elements)

    def check_solution(self, proposed_solution: str) -> bool:
        """Check if a proposed solution matches the correct solution"""
        # Normalize both solutions for comparison
        normalized_proposed = " ".join(proposed_solution.lower().split())
        normalized_solution = " ".join(self.solution.lower().split())
        return normalized_proposed == normalized_solution

    def get_discovered_documents(self) -> List[Document]:
        """Get all discovered documents"""
        discovered = [self.documents[doc_id] for doc_id in self.discovered_docs]
        print(f"Retrieving discovered documents. Total count: {len(discovered)}")
        return discovered

    def get_document_by_id(self, doc_id: str) -> Document:
        """Get a specific document by ID"""
        return self.documents.get(doc_id)


class RAGSystem:
    """Retrieval-Augmented Generation system for using discovered documents"""

    def __init__(self, model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
        """Initialize the RAG system with TinyLLaMA tokenizer"""
        self.tokenizer = None
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            print("Successfully loaded TinyLLaMA tokenizer for RAG")
        except Exception as e:
            print(f"Could not load TinyLLaMA tokenizer: {e}")
            self.tokenizer = None

        self.document_embeddings = {}
        self.documents = {}

    def _get_embedding(self, text: str) -> torch.Tensor:
        """Get embedding for text using TinyLLaMA tokenizer"""
        if not self.tokenizer:
            return None

        # Tokenize and convert to tensor
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        input_ids = inputs["input_ids"]
        
        # Create a simple embedding by averaging token embeddings
        # This is a basic approach - could be improved with actual model embeddings
        with torch.no_grad():
            # Get token embeddings from the tokenizer's vocabulary
            vocab_size = len(self.tokenizer.get_vocab())
            # Create a one-hot encoding of the tokens
            embedding = torch.zeros(vocab_size, dtype=torch.float)
            for id in input_ids[0]:
                embedding[id.item()] = 1.0
            # Normalize the embedding
            embedding = F.normalize(embedding, p=2, dim=0)
            return embedding

    def add_documents(self, documents: List[Document]):
        """Add documents and create embeddings"""
        for doc in documents:
            self.documents[doc.id] = doc

            # Create document text for embedding
            doc_text = f"{doc.title} {doc.content}"

            if self.tokenizer:
                # Use TinyLLaMA tokenizer for embedding
                embedding = self._get_embedding(doc_text)
                if embedding is not None:
                    self.document_embeddings[doc.id] = embedding
            else:
                # Fallback: use keyword-based system
                self.document_embeddings[doc.id] = doc_text.lower()

    def retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """Retrieve the most relevant documents for a query"""
        if not self.documents:
            return []

        if self.tokenizer:
            return self._semantic_retrieval(query, top_k)
        else:
            return self._keyword_retrieval(query, top_k)

    def _semantic_retrieval(self, query: str, top_k: int) -> List[Tuple[Document, float]]:
        """Semantic retrieval using PyTorch functional cosine similarity"""
        query_embedding = self._get_embedding(query)
        if query_embedding is None:
            return self._keyword_retrieval(query, top_k)

        similarities = []
        for doc_id, doc_embedding in self.document_embeddings.items():
            # Calculate cosine similarity using PyTorch functional
            similarity = F.cosine_similarity(
                query_embedding.unsqueeze(0),
                doc_embedding.unsqueeze(0)
            ).item()
            similarities.append((doc_id, similarity))

        # Sort by similarity and get top_k
        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in similarities[:top_k]:
            if score > 0.1:  # Minimum similarity threshold
                results.append((self.documents[doc_id], score))

        return results

    def _keyword_retrieval(self, query: str, top_k: int) -> List[Tuple[Document, float]]:
        """Fallback keyword-based retrieval"""
        query_lower = query.lower()
        query_words = set(query_lower.split())

        scores = []
        for doc_id, doc_text in self.document_embeddings.items():
            doc_words = set(doc_text.split())
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0:
                score = overlap / len(query_words.union(doc_words))
                scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in scores[:top_k]:
            results.append((self.documents[doc_id], score))

        return results

    def create_context_for_prompt(self, query: str, max_context_length: int = 500) -> str:
        """Create context string from relevant documents for the LLM prompt"""
        relevant_docs = self.retrieve_relevant_documents(query)

        if not relevant_docs:
            return ""

        context_parts = ["DISCOVERED CLUES AND EVIDENCE:"]
        current_length = len(context_parts[0])

        for doc, score in relevant_docs:
            doc_text = f"\n[{doc.category.upper()}] {doc.title}: {doc.content}"

            if current_length + len(doc_text) > max_context_length:
                break

            context_parts.append(doc_text)
            current_length += len(doc_text)

        return "\n".join(context_parts)