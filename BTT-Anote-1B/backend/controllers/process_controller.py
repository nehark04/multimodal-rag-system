from flask import Blueprint, jsonify
from services.processing_service import process_file_based_on_extension

process_bp = Blueprint('process', __name__)

def process(filepath):
    try:
        process_file_based_on_extension(filepath)
        return {"message": "Files processed successfully"}
    except Exception as e:
        return {"error": str(e)}

# from flask import Blueprint, jsonify
# from services.processing_service import process_file_based_on_extension

# process_bp = Blueprint('process', __name__)

# @process_bp.route('/process-message', methods=['POST'])
# def process(filepath):
#     try:
#         process_file_based_on_extension(filepath)
#         return jsonify({"message": "Files processed successfully"}), 200
#     except Exception as e:
#         # app.logger.error(f"Error in processing files: {e}")
#         return jsonify({"error": str(e)}), 500
