from flask import Blueprint, request, jsonify
from services.rag_service import generate_rag_response, log_query_to_csv

query_bp = Blueprint('query', __name__)

@query_bp.route('/query-task', methods=['POST'])
def query():
    # Get query from the request body
    query = request.json.get('query')
    
    # Input validation
    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        # Generate response using RAG service
        response = generate_rag_response(query)
        
        # Log query and response to a CSV file
        log_query_to_csv(query, response)
        
        # Return the generated response
        return jsonify({"response": response}), 200
    except Exception as e:
        # Return the error message if something goes wrong
        return jsonify({"error": str(e)}), 500
