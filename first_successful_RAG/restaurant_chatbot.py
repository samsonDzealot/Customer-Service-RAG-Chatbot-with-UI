import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

class RestaurantChatbot:
    def __init__(self):
        """Initialize the chatbot with ChromaDB and OpenAI connections."""
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./first_successful_RAG/chroma_db")
        self.collection = self.chroma_client.get_collection("restaurant_docs")
        
        print(f"Connected to ChromaDB. Total chunks: {self.collection.count()}")
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for user query."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[query]
        )
        return response.data[0].embedding
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Retrieve most relevant chunks from ChromaDB."""
        query_embedding = self.get_query_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        return results
    
    def create_context(self, results: Dict[str, Any]) -> str:
        """Combine retrieved chunks into coherent context."""
        context_parts = []
        
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            source = metadata['source']
            context_parts.append(f"[{source}] {doc}")
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using OpenAI chat model."""
        system_prompt = """You are a helpful assistant for Orisirisi Restaurant. 
        Use the provided context to answer questions about the restaurant's menu, policies, staff, and services.
        
        Guidelines:
        - Be friendly and professional
        - Only answer based on the provided context
        - If information isn't in the context, politely say you don't have that information
        - For menu items, include prices when available
        - Be specific and helpful
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def chat(self, query: str) -> str:
        """Main RAG pipeline: retrieve and generate response."""
        # Retrieve relevant chunks
        results = self.retrieve_relevant_chunks(query)
        
        # Create context from retrieved chunks
        context = self.create_context(results)
        
        # Generate response
        response = self.generate_response(query, context)
        
        return response
    
    def run_chat_loop(self):
        """Run interactive chat loop."""
        print("\n" + "="*50)
        print("Welcome to Orisirisi Restaurant Chatbot!")
        print("Ask me anything about our menu, policies, or services.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Thank you for visiting Orisirisi! Have a great day!")
                    break
                
                if not user_input:
                    print("Please enter a question.")
                    continue
                
                print("Assistant: ", end="")
                response = self.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Sorry, I encountered an error: {e}")
                print("Please try again.")

# Main execution
if __name__ == "__main__":
    try:
        chatbot = RestaurantChatbot()
        chatbot.run_chat_loop()
    except Exception as e:
        print(f"Failed to initialize chatbot: {e}")
        print("Make sure ChromaDB is properly set up and OpenAI API key is configured.")