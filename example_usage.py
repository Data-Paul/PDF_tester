from pdf_to_text import process_pdf_with_pandas
import os

def example_usage():
    """
    Example usage of the PDF to text converter.
    """
    # Example 1: Process a PDF file
    pdf_path = "C:\Users\paulh\Desktop\Codersbay\cursor_repo\PDF_tester\input\test1.pdf"  # Replace with your PDF file path
    
    if os.path.exists(pdf_path):
        print("Processing PDF file...")
        df = process_pdf_with_pandas(pdf_path)
        
        if df is not None:
            print("\nDataFrame preview:")
            print(df.head())
    else:
        print(f"PDF file '{pdf_path}' not found.")
        print("Please place a PDF file in the current directory or update the path.")

def batch_process_pdfs(pdf_directory="."):
    """
    Process all PDF files in a directory.
    
    Args:
        pdf_directory (str): Directory containing PDF files
    """
    pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_directory}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file}")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"\nProcessing: {pdf_file}")
        process_pdf_with_pandas(pdf_path)

if __name__ == "__main__":
    print("PDF to Text Converter Example")
    print("=" * 30)
    
    # Example 1: Single file processing
    example_usage()
    
    # Example 2: Batch processing (uncomment to use)
    # print("\n" + "=" * 30)
    # print("Batch Processing Example")
    # batch_process_pdfs() 