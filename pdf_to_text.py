import pandas as pd
import PyPDF2
import os
from pathlib import Path

def read_pdf_to_text(pdf_path):
    """
    Read all text content from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text_content = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text_content.append(f"--- Page {page_num + 1} ---\n{page_text}\n")
                
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None
    
    return '\n'.join(text_content)

def save_text_to_file(text_content, output_path):
    """
    Save text content to a file.
    
    Args:
        text_content (str): Text content to save
        output_path (str): Path where to save the text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"Text content saved to: {output_path}")
    except Exception as e:
        print(f"Error saving text file: {str(e)}")

def process_pdf_with_pandas(pdf_path, output_path=None):
    """
    Process PDF and save text content using pandas for data handling.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path for output text file. If None, uses PDF name with .txt extension
    """
    # Read PDF content
    print(f"Reading PDF: {pdf_path}")
    text_content = read_pdf_to_text(pdf_path)
    
    if text_content is None:
        return
    
    # Create DataFrame with the text content
    df = pd.DataFrame({
        'page_number': range(1, len(text_content.split('--- Page'))),
        'content': text_content.split('--- Page')[1:] if '--- Page' in text_content else [text_content]
    })
    
    # Determine output path
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}.txt"
    
    # Save text content to file
    save_text_to_file(text_content, output_path)
    
    # Also save as CSV using pandas (optional)
    csv_path = output_path.replace('.txt', '.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"DataFrame saved to CSV: {csv_path}")
    
    # Display some statistics
    print(f"\nPDF Processing Summary:")
    print(f"Total pages: {len(df)}")
    print(f"Total characters: {len(text_content)}")
    print(f"Total words: {len(text_content.split())}")
    
    return df

def main():
    """
    Main function to demonstrate PDF processing.
    """
    # Example usage
    pdf_file = input("Enter the path to your PDF file: ").strip()
    
    if not pdf_file:
        print("No PDF file specified. Please provide a valid PDF path.")
        return
    
    if not os.path.exists(pdf_file):
        print(f"File '{pdf_file}' does not exist.")
        return
    
    # Process the PDF
    df = process_pdf_with_pandas(pdf_file)
    
    if df is not None:
        print("\nFirst few lines of extracted content:")
        print(df.head())

if __name__ == "__main__":
    main() 