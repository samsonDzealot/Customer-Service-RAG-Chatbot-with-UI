import csv
import docx
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

def load_documents() -> List[Dict[str, Any]]:
    """Load and chunk all documents using RecursiveCharacterTextSplitter with tiktoken."""
    
    # Initialize text splitter with gpt-4o-mini tokenizer
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o-mini",
        chunk_size=400,  # tokens
        chunk_overlap=50,  # tokens
    )
    
    chunks = []
    
    # File paths
    files = {
        'faq': r"C:\Users\User\Desktop\ORISIRI_MATTERS\Orisirisi FAQs.docx",
        'menu': r"C:\Users\User\Desktop\ORISIRI_MATTERS\orisirisi_menu.csv",
        'staff': r"C:\Users\User\Desktop\ORISIRI_MATTERS\Name Designation.pdf"
    }
    
    # Load FAQ (Word document)
    doc = docx.Document(files['faq'])
    faq_text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
    faq_chunks = text_splitter.split_text(faq_text)
    
    for i, chunk in enumerate(faq_chunks):
        chunks.append({
            'text': chunk,
            'source': 'FAQ',
            'chunk_id': f'faq_{i}'
        })
    
    # Load Menu (CSV)
    with open(files['menu'], 'r', encoding='utf-8') as f:
        menu_items = []
        for row in csv.DictReader(f):
            item = row.get('Item', '').strip()
            price = row.get('Price (USD)', '').strip()
            if item:
                menu_items.append(f"{item} - ${price}" if price else item)
        
        menu_text = "Restaurant Menu:\n" + "\n".join(menu_items)
        menu_chunks = text_splitter.split_text(menu_text)
        
        for i, chunk in enumerate(menu_chunks):
            chunks.append({
                'text': chunk,
                'source': 'Menu',
                'chunk_id': f'menu_{i}'
            })
    
    # Load Staff (PDF)
    with open(files['staff'], 'rb') as f:
        pdf_text = ""
        for page in PyPDF2.PdfReader(f).pages:
            pdf_text += page.extract_text()
        
        staff_text = "Restaurant Staff:\n" + pdf_text.replace('\n', '\n')
        staff_chunks = text_splitter.split_text(staff_text)
        
        for i, chunk in enumerate(staff_chunks):
            chunks.append({
                'text': chunk,
                'source': 'Staff',
                'chunk_id': f'staff_{i}'
            })
    
    return chunks

# Test loading
if __name__ == "__main__":
    chunks = load_documents()
    
    print(f"Loaded {len(chunks)} chunks")

# Load environment variables
load_dotenv()

def create_embeddings_and_store():
    """Generate embeddings and store in ChromaDB."""
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(
        name="restaurant_docs",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Load documents
    chunks = load_documents()
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    # Prepare batch data
    texts = [chunk['text'] for chunk in chunks]
    metadatas = [{'source': chunk['source'], 'chunk_id': chunk['chunk_id']} for chunk in chunks]
    ids = [chunk['chunk_id'] for chunk in chunks]
    
    # Generate embeddings in batches (OpenAI allows up to 2048 texts per request)
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch_texts
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        
        print(f"Processed {min(i+batch_size, len(texts))}/{len(texts)} chunks")
    
    # Store in ChromaDB
    collection.add(
        embeddings=all_embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Successfully stored {len(chunks)} chunks in ChromaDB")
    print(f"Collection count: {collection.count()}")
    
    return collection

# Add to main execution
if __name__ == "__main__":
    # Load and chunk documents
    chunks = load_documents()
    print(f"Loaded {len(chunks)} chunks")
    
    # Create embeddings and store
    collection = create_embeddings_and_store()