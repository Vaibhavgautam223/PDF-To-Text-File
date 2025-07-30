import PyPDF2
import json
import os
from tqdm import tqdm  # Optional for progress bar
import dump 
def pdf_to_json(pdf_path, output_dir=None):
    # Validate PDF path
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("File must be a PDF")
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output JSON path
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    json_path = os.path.join(output_dir, f"{pdf_name}.json")
    
    # Read PDF
    text_content = {}
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Handle encrypted PDFs
        if pdf_reader.is_encrypted:
            try:
                pdf_reader.decrypt('')
            except:
                raise ValueError("PDF is encrypted and cannot be read.")
        
        # Corrected Metadata Access
        meta = pdf_reader.metadata or {}
        text_content['metadata'] = {
            'pdf_path': os.path.abspath(pdf_path),
            'pages': len(pdf_reader.pages),
            'author': meta.get('/Author'),
            'title': meta.get('/Title'),
            'subject': meta.get('/Subject'),
        }
        
        # Extract text with progress bar
        text_content['pages'] = []
        for page_num in tqdm(range(len(pdf_reader.pages)), desc="Extracting pages"):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text() or ""
            text_content['pages'].append({
                'page_number': page_num + 1,
                'text': page_text,
                'character_count': len(page_text)
            })
    
    # Save to JSON
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(text_content, json_file, indent=4, ensure_ascii=False)
    
    return json_path

if __name__ == "__main__":
    # Example usage - change this path to your PDF
    pdf_path = r"C:\Users\HP\OneDrive\Desktop\Internship\Task1\long-sample.pdf"
    
    try:
        result_path = pdf_to_json(pdf_path)
        print(f"✅ Successfully created JSON file at:\n{result_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
