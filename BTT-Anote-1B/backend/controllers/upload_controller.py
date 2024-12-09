from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from utils.file_utils import allowed_file
from controllers.process_controller import process
import logging

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = '../uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'png', 'mp3', 'wav', 'mp4', 'avi', 'mov'}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            print("request.files: ", request.files)
            if 'file' not in request.files:
                response = jsonify({"error": "No file part"})
                response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                return response, 400
            
            file = request.files['file']
            if file.filename == '':
                response = jsonify({"error": "No selected file"})
                response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                return response, 400

            if file and allowed_file(file.filename):
                # Create folder with current timestamp
                current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                folder_path = os.path.join(UPLOAD_FOLDER, current_datetime)
                print("folder_path: ", folder_path)
                os.makedirs(folder_path, exist_ok=True)

                # Save the file
                filename = secure_filename(file.filename)
                file_path = os.path.join(folder_path, filename)
                file_path = file_path.replace("\\", "/")
                print("file_path: ", file_path)
                file.save(file_path)

                # Call the processing function
                process_result = process(file_path)  # Call the processing function based on file type
                if "error" in process_result:
                    response = jsonify(process_result)
                    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                    response.headers['Access-Control-Allow-Credentials'] = 'true'
                    return response, 500
                else:
                    response = jsonify({"message": "File uploaded and processed", "processed_text": process_result["message"]})
                    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                    response.headers['Access-Control-Allow-Credentials'] = 'true'
                    return response, 200
        else:
            response = jsonify({"message": "Upload endpoint"})
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response, 200
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        response = jsonify({"error": str(e)})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 500