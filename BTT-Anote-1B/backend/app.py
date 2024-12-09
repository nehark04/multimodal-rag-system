from flask import Flask, request, jsonify, make_response
from flask.wrappers import Response
from dotenv import load_dotenv
from flask_cors import CORS
from controllers.upload_controller import upload_bp
from controllers.process_controller import process_bp
from controllers.query_controller import query_bp
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import csv
import openai
import io
import re

load_dotenv(override=True)

app = Flask(__name__)

# Allow specific origin and support credentials
CORS(app, origins="http://localhost:3000", supports_credentials=True)

app.config['UPLOAD_FOLDER'] = "./uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['DEBUG'] = True

# Register Blueprints for modular routing
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(process_bp, url_prefix='/process')
app.register_blueprint(query_bp, url_prefix='/query')

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = make_response('')
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

# if ray.is_initialized() == False:
#   ray.init(logging_level="INFO", log_to_driver=True)

# welcome check endpoint
@app.route('/welcome', methods=['GET'])
def welcome():
    print("Welcome endpoint accessed")
    return "Welcome to the Backend!", 200

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    print("Health check endpoint accessed")
    return "Healthy", 200

@app.errorhandler(404)
def invalid_route(e):
    print("Invalid route accessed")
    return "Sorry, Invalid Route!", 200

## CHATBOT SECTION
output_document_path = '../../backend/output_document/'
chat_history_file = os.path.join(output_document_path, 'chat_history.csv')
vector_base_path = 'db'
source_documents_path = 'source_documents'

# Only for demo purposes
chat_to_document_mapping = {}
DEMO_USER_EMAIL = "manojnath112@gmail.com"
chat_id = 0

@app.route('/process-message-pdf-demo', methods=['GET', 'POST'])
def process_message_pdf_demo():
    message = request.json.get('message')
    query = message.strip()
    sources_str = " "
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user",
                    "content": f"You are a factual chatbot that answers questions about uploaded documents. You only answer with answers you find in the text, no outside information. These are the sources from the text:{sources_str} And this is the question:{query}."}]
    )
    answer = str(completion.choices[0].message.content)
    return jsonify(answer=answer)


@app.route('/ingest-pdf-demo', methods=['GET', 'POST'])
def ingest_pdfs_demo():
    return jsonify({"message": "Document processed successfully"}), 200

@app.route('/reset-chat-demo', methods=['GET', 'POST'])
def reset_chat_demo():
    return jsonify({"Success": "Success"}), 200

@app.route('/download-chat-history-demo', methods=['GET', 'POST'])
def download_chat_history_demo():
    global chat_id
    user_email = DEMO_USER_EMAIL

    try:
        messages = []
        paired_messages = []
        for i in range(len(messages) - 1):
            if messages[i]['sent_from_user'] == 1 and messages[i+1]['sent_from_user'] == 0:
                regex = re.compile(r"Document:\s*[^:]+:\s*(.*?)(?=Document:|$)", re.DOTALL)
                if messages[i+1]["relevant_chunks"]:
                    found = re.findall(regex, messages[i+1]["relevant_chunks"])
                    paragraphs = [paragraph.strip() for paragraph in found]
                    if len(paragraphs) > 1:
                        paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], paragraphs[0], paragraphs[1]))
                    elif len(paragraphs) == 1:
                        paired_messages.append((messages[i]['message_text'],  messages[i+1]['message_text'], paragraphs[0], None))
                else:
                    paired_messages.append((messages[i]['message_text'], messages[i+1]['message_text'], None, None))

        csv_output = io.StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(['query', 'response', 'chunk1', 'chunk2'])
        writer.writerows(paired_messages)
        csv_output.seek(0)

        # Return the CSV content as a response
        return Response(
            csv_output.getvalue(),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=chat_history.csv"}
        )
    except Exception as e:
        print("error is,", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
