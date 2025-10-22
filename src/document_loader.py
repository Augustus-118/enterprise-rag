import fitz
from pathlib import Path

def load_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = "".join([page.get_text() for page in doc])
    doc.close()
    return text

def load_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def load_documents_from_folder(folder_path: str):
    folder = Path(folder_path)
    files = list(folder.glob('*.pdf')) + list(folder.glob('*.txt'))
    
    all_chunks = []
    all_metadata = []
    
    for file_path in files:
        if file_path.suffix == '.pdf':
            text = load_pdf(str(file_path))
        else:
            text = load_txt(str(file_path))
        
        chunks = chunk_text(text)
        
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadata.append({'file': file_path.name})
    
    return all_chunks, all_metadata
