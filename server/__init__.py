from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from server.functions import parse_user_query, search_songs_in_qdrant
import logging

app = Flask(__name__, static_folder='../client/build', static_url_path='')

CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_filters')
def get_filters():
    try:
        user_query = request.args.get('user_query')

        response = parse_user_query(user_query)

        if response is not None:
            return jsonify(response)
        else:
            return jsonify({'error': 'Unable to parse user query.'}), 500
    except Exception as e:
        logging.error(f'Error generating filters from the query: {e}')
        return jsonify({'error': str(e)}), 400

@app.route('/search_songs', methods=['POST'])
def get_movie_list():
    try:
        json_body = request.get_json()

        if json_body is None:
            logging.error('No JSON data received.')
            return jsonify({'error': 'No JSON data received.'}), 400
        
        response = search_songs_in_qdrant(json_body)

        if response is not None:
            return jsonify(response), 200
        else:
            return jsonify({'error': 'Unable to fetch movie data.'}), 500
    except Exception as e:
        logging.error(f'Error processing search request: {e}')
        return jsonify({'error': str(e)}), 400