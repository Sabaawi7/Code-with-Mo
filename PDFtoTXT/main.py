import PyPDF2
import os
import sys

# Get the path of the PDF file to extract text from from the command-line argument
if len(sys.argv) < 2:
    print("Usage: python extract_text.py <pdf_file_path>")
    sys.exit(1)
pdf_file_path = sys.argv[1]

# Open the PDF file
pdf_file = open(pdf_file_path, 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Get the number of pages in the PDF document
num_pages = len(pdf_reader.pages)

# Loop through each page in the PDF document and extract text
text = ""
for page in range(num_pages):
    # Get the page object
    pdf_page = pdf_reader.pages[page]

    # Extract text from the page
    page_text = pdf_page.extract_text()

    # Add the text to the overall text variable
    text += page_text

# Close the PDF file
pdf_file.close()

# Write the extracted text to a text file with the same name as the original PDF file
pdf_file_name = os.path.basename(pdf_file_path)
text_file_name = os.path.splitext(pdf_file_name)[0] + ".txt"
text_file = open(text_file_name, "w")
text_file.write(text)
text_file.close()

# Print a message to confirm that the text file was created
print("Text file created:", text_file_name)
