# PDF to Text Converter

A Python tool that reads PDF files and converts their content to text files using pandas for data handling.

## Features

- Extract text from PDF files page by page
- Save extracted text to `.txt` files
- Create pandas DataFrames for data analysis
- Export data to CSV format
- Batch processing of multiple PDF files
- Error handling and progress reporting

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Interactive Mode
Run the main script and follow the prompts:
```bash
python pdf_to_text.py
```

### Method 2: Programmatic Usage
```python
from pdf_to_text import process_pdf_with_pandas

# Process a single PDF file
df = process_pdf_with_pandas("path/to/your/file.pdf")

# Process with custom output path
df = process_pdf_with_pandas("path/to/your/file.pdf", "output.txt")
```

### Method 3: Example Usage
Run the example script:
```bash
python example_usage.py
```

## Output Files

For each processed PDF, the tool creates:
1. **Text file** (`.txt`): Contains all extracted text with page separators
2. **CSV file** (`.csv`): Pandas DataFrame with page numbers and content

## Example Output

### Text File Format:
```
--- Page 1 ---
[Page 1 content here]

--- Page 2 ---
[Page 2 content here]
...
```

### CSV File Format:
| page_number | content |
|-------------|---------|
| 1 | [Page 1 content] |
| 2 | [Page 2 content] |

## Dependencies

- `pandas`: Data manipulation and analysis
- `PyPDF2`: PDF reading and text extraction

## Error Handling

The tool includes comprehensive error handling for:
- Missing PDF files
- Corrupted PDF files
- Permission issues
- Encoding problems

## Batch Processing

To process multiple PDF files in a directory:
```python
from example_usage import batch_process_pdfs

# Process all PDFs in current directory
batch_process_pdfs()

# Process PDFs in specific directory
batch_process_pdfs("/path/to/pdf/directory")
``` 
