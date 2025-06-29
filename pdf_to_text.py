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

def split_text_at_headers(text_content, pdf_name):
    """
    Split text content at headers and save each section to separate CSV files.
    
    Args:
        text_content (str): Text content to split
        pdf_name (str): Base name of the PDF file for output naming
    """
    headers = {
        "personal_information": ["Name Familienname Geburtsdatum Nationalität", "Erlernter Beruf Barcode"],
        "education": ["Beginn Ende Ausbildung Institution"],
        "skills": ["Gruppe Name Einstufung"],
        "work_experience": ["Beginn Ende Unternehmen Bezeichnung Allg Beschreibung"],
        "traits": ["Persönliche Eigenschaften"]
    }
    
    # Initialize sections dictionary
    sections = {key: [] for key in headers.keys()}
    current_section = None
    current_content = []
    
    # Split text into lines for processing
    lines = text_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line contains any header
        found_header = False
        for section_name, header_list in headers.items():
            # Handle both list and string header formats
            if isinstance(header_list, list):
                for header in header_list:
                    if header in line:
                        # Save previous section content if exists
                        if current_section and current_content:
                            sections[current_section].extend(current_content)
                        
                        # Start new section - don't include the header line itself
                        current_section = section_name
                        current_content = []
                        found_header = True
                        break
                if found_header:
                    break
            else:  # Handle string header
                if header_list in line:
                    if current_section and current_content:
                        sections[current_section].extend(current_content)
                    
                    current_section = section_name
                    current_content = []
                    found_header = True
                    break
        
        # If no header found, add line to current section
        if not found_header and current_section:
            current_content.append(line)
    
    # Save the last section
    if current_section and current_content:
        sections[current_section].extend(current_content)
    
    # Create CSV files for each section
    for section_name, content in sections.items():
        if content:
            # Process content to create table structure
            processed_rows = []
            
            # Add the header as the first row with proper semicolon separation
            header_text = headers[section_name][0] if isinstance(headers[section_name], list) else headers[section_name]
            # Split header by spaces and join with semicolons
            header_row = [item.strip() for item in header_text.split() if item.strip()]
            processed_rows.append(header_row)
            
            for line in content:
                # Split line by common delimiters and clean up
                # Look for semicolons, tabs, or multiple spaces as delimiters
                if ';' in line:
                    # Already semicolon-separated
                    row_data = [item.strip() for item in line.split(';')]
                elif '\t' in line:
                    # Tab-separated
                    row_data = [item.strip() for item in line.split('\t')]
                else:
                    # Try to split by multiple spaces (common in PDFs)
                    import re
                    row_data = [item.strip() for item in re.split(r'\s{2,}', line) if item.strip()]
                
                # If we still have one item, try splitting by single spaces
                if len(row_data) == 1 and ' ' in row_data[0]:
                    row_data = [item.strip() for item in row_data[0].split(' ') if item.strip()]
                
                if row_data:
                    processed_rows.append(row_data)
            
            if processed_rows:
                # Find the maximum number of columns
                max_cols = max(len(row) for row in processed_rows)
                
                # Pad shorter rows with empty strings
                for row in processed_rows:
                    while len(row) < max_cols:
                        row.append('')
                
                # Create DataFrame with proper column names
                df_section = pd.DataFrame(processed_rows)
                
                # Save to CSV with proper encoding and without index
                csv_filename = f"{pdf_name}_{section_name}.csv"
                df_section.to_csv(csv_filename, index=False, header=False, encoding='utf-8-sig')
                print(f"Saved {section_name} section to: {csv_filename}")
    
    return sections

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
    
    # Determine output path and PDF name
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}.txt"
    else:
        pdf_name = Path(output_path).stem
    
    # Split text at headers and save to separate CSVs
    sections = split_text_at_headers(text_content, pdf_name)
    
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
    print(f"Sections found: {list(sections.keys())}")
    
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