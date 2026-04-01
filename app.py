"""
REST API application for generating fake person information.
Replaces the original PHP index.php file.

@author  Arturo Mora-Rioja
@version 2.0.0 March 2026 Python/Flask implementation
"""
from flask import Flask, request, jsonify
import json
from src.fake_info import FakeInfo

app = Flask(__name__)

# Error codes
ERROR_METHOD = 0
ERROR_ENDPOINT = 1
ERROR_PARAMS = 2
POS_ENTITY = 0


def report_error(error: int = -1):
    """
    Reports an error based on the error code provided.
    @param error: Error code
    @return: JSON response with error message
    """
    error_messages = {
        ERROR_METHOD: ('Incorrect HTTP method', 405),
        ERROR_ENDPOINT: ('Incorrect API endpoint', 404),
        ERROR_PARAMS: ('Incorrect GET parameter value', 400),
    }
    
    if error in error_messages:
        message, status_code = error_messages[error]
    else:
        message, status_code = 'Unknown error', 500
    
    return jsonify({'error': message}), status_code


@app.before_request
def before_request():
    """
    Set response headers for CORS and content type.
    """
    pass


@app.after_request
def after_request(response):
    """
    Add CORS and API version headers to all responses.
    """
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Accept-version'] = 'v1'
    return response


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({'error': 'Incorrect HTTP method'}), 405


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def api_handler(path):
    """
    Main API handler that routes requests to appropriate endpoints.
    """
    # Validate HTTP method
    if request.method != 'GET':
        return report_error(ERROR_METHOD)
    
    # Parse the URL path
    url_pieces = [p for p in path.split('/') if p]
    
    if not url_pieces:
        return report_error(ERROR_ENDPOINT)
    
    try:
        fake_person = FakeInfo()
        entity = url_pieces[POS_ENTITY]
        
        if entity == 'cpr':
            return jsonify({'CPR': fake_person.get_cpr()}), 200
        
        elif entity == 'name-gender':
            return jsonify(fake_person.get_full_name_and_gender()), 200
        
        elif entity == 'name-gender-dob':
            return jsonify(fake_person.get_full_name_gender_and_birth_date()), 200
        
        elif entity == 'cpr-name-gender':
            return jsonify(fake_person.get_cpr_full_name_and_gender()), 200
        
        elif entity == 'cpr-name-gender-dob':
            return jsonify(fake_person.get_cpr_full_name_gender_and_birth_date()), 200
        
        elif entity == 'address':
            return jsonify(fake_person.get_address()), 200
        
        elif entity == 'phone':
            return jsonify({'phoneNumber': fake_person.get_phone_number()}), 200
        
        elif entity == 'person':
            num_persons = request.args.get('n', default=1, type=int)
            num_persons = abs(num_persons)
            
            if num_persons == 0:
                return report_error(ERROR_PARAMS)
            elif num_persons == 1:
                return jsonify(fake_person.get_fake_person()), 200
            elif num_persons > 1 and num_persons <= 100:
                return jsonify(fake_person.get_fake_persons(num_persons)), 200
            else:
                return report_error(ERROR_PARAMS)
        
        else:
            return report_error(ERROR_ENDPOINT)
    
    except Exception as e:
        print(f"Error: {e}")
        return report_error()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
