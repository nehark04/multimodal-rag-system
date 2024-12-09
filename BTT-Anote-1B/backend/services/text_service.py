import os
from PyPDF2 import PdfReader
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

def process_text(file_path):
    """
    Process a single text or PDF file and save the processed content.

    Args:
    - file_path: The path to the text or PDF file.
    - processed_folder: The folder where the processed content will be stored.

    Returns:
    - processed_file_path: Path to the processed file if successful, None otherwise.
    """
    if not os.path.exists(file_path):
        logging.error(f"The file {file_path} does not exist.")
        return None
    processed_folder = "../processed_content/"
    # Ensure the processed folder exists
    os.makedirs(processed_folder, exist_ok=True)

    file_name = os.path.basename(file_path)
    processed_file_name = f"{os.path.splitext(file_name)[0]}_processed.txt"
    processed_file_path = os.path.join(processed_folder, processed_file_name)

    try:
        # Determine file type and process accordingly
        if file_path.endswith('.txt'):
            text = process_txt_file(file_path)
        elif file_path.endswith('.pdf'):
            text = process_pdf_file(file_path)
        else:
            logging.error("Unsupported file type. Only .txt and .pdf files are supported.")
            return None

        # Save the processed content to the processed folder
        with open(processed_file_path, "w", encoding="utf-8") as f:
            f.write(text)

        logging.info(f"Processed content saved to {processed_file_path}")
        return processed_file_path
    except Exception as e:
        logging.error(f"Error processing the file {file_path}: {e}")
        return None

def process_txt_file(filepath):
    """
    Process a text file and return its content.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def process_pdf_file(filepath):
    """
    Process a PDF file and extract its text content.
    """
    text = ''
    reader = PdfReader(filepath)
    for page in reader.pages:
        text += page.extract_text()
    return text

# Example usage
# if __name__ == "__main__":
#     # Input file path (change as needed)
#     file_to_process = "example.pdf"  # Replace with your file path
#     processed_dir = "processed_folder"

#     # Process the file
#     process_text(file_to_process, processed_dir)


# import os
# from PyPDF2 import PdfReader
# import logging

# # Setting up logging
# logging.basicConfig(level=logging.INFO)

# def process_text(upload_folder):
#     """
#     Process text files (txt and pdf) in the given folder.

#     Args:
#     - upload_folder: The folder where the uploaded text files are stored.

#     This function will process text and PDF files and return the extracted text.
#     """
#     text_files = get_text_files(upload_folder)

#     if not text_files:
#         logging.info("No text files found to process.")
#         return

#     processed_text = {}
#     processed_text_file_path = os.path.join(upload_folder, 'processed_text.txt')

#     with open(processed_text_file_path, "w", encoding='utf-8') as f:
#         for text_file in text_files:
#             file_path = os.path.join(upload_folder, text_file)
#             logging.info(f"Processing {text_file}...")

#             try:
#                 # Process the text or PDF file
#                 if file_path.endswith('.txt'):
#                     text = process_txt_file(file_path)
#                 elif file_path.endswith('.pdf'):
#                     text = process_pdf_file(file_path)
#                 else:
#                     continue  # Skip unsupported file types
                
#                 processed_text[text_file] = text

#                 # Write processed text to file
#                 f.write(f"Content from {text_file}:\n{text}\n\n")
#                 logging.info(f"Completed processing for {text_file}")
#             except Exception as e:
#                 logging.error(f"Error processing {text_file}: {e}")

#     logging.info(f"All text files have been processed. Processed text saved to {processed_text_file_path}")
#     return processed_text_file_path

# def get_text_files(upload_folder):
#     """
#     Get a list of text and PDF files in the upload folder.
#     """
#     return [f for f in os.listdir(upload_folder) if f.endswith(('.txt', '.pdf'))]

# def process_txt_file(filepath):
#     """
#     Process a text file and return its content.
#     """
#     with open(filepath, 'r', encoding='utf-8') as file:
#         return file.read()

# def process_pdf_file(filepath):
#     """
#     Process a PDF file and extract its text content.
#     """
#     text = ''
#     reader = PdfReader(filepath)
#     for page in reader.pages:
#         text += page.extract_text()
#     return text
