from src.rag_engine import SecureRAGEngine

def main():
    rag = SecureRAGEngine()
    rag.ingest_documents("./documents/")
    
    print("Day 3: Secure RAG\n")
    
    while True:
        q = input("Question: ")
        if q.lower() == 'quit':
            break
        
        result = rag.query(q)
        
        if 'error' in result:
            print(f"Error: {result['error']}\n")
        else:
            print(f"\nAnswer: {result['answer']}\n")

if __name__ == "__main__":
    main()