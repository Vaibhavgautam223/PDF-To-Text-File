import PyPDF2
import os

def pdf_to_text(pdf_file_path):
    # Check if the file exists
    if not os.path.exists(pdf_file_path):
        print(f"The file {pdf_file_path} does not exist.")
        return

    # Create a text file name based on the PDF file name
    text_file_path = os.path.splitext(pdf_file_path)[0] + '.txt'

    # Open the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = []

        # Extract text from each page
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())

    # Write the extracted text to a text file
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        for page_text in text_content:
            if page_text:  # Check if the page has text
                text_file.write(page_text + '\n')

    print(f"Text extracted and saved to {text_file_path}")

# Specify the path to your PDF file here
pdf_file_path = r'C:\Users\HP\OneDrive\Desktop\Internship\Task1\long-sample.pdf'  # Change this to your PDF file path
pdf_to_text(pdf_file_path)
