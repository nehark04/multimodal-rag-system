from transformers import RagTokenizer, RagSequenceForGeneration
import csv
import os

# Initialize RAG model and tokenizer
rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq")

# Path for storing chat history
chat_history_file = 'output_document/chat_history.csv'

def generate_rag_response(query):
    """
    Generate a response for the given query using the RAG model.
    
    Args:
    - query: The input query string
    
    Returns:
    - The generated response as a string
    """
    inputs = rag_tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=512)
    generated_ids = rag_model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], num_beams=4, max_length=100)
    
    # Decode the generated response
    return rag_tokenizer.decode(generated_ids[0], skip_special_tokens=True)

def log_query_to_csv(query, response):
    """
    Log the query and response into the CSV file.
    
    Args:
    - query: The input query string
    - response: The generated response string
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(chat_history_file), exist_ok=True)

    # Write query and response to CSV
    file_exists = os.path.isfile(chat_history_file)
    
    with open(chat_history_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header only if the file doesn't already exist
        if not file_exists:
            writer.writerow(['query', 'response'])

        # Append the query and response to the CSV file
        writer.writerow([query, response])
