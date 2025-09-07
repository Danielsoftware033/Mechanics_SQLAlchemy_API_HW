from jose import jwt
import jose
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "super duper mega secrets"

def encode_token(mechanic_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), 
        'iat': datetime.now(timezone.utc),
        'sub': str(mechanic_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token 


def token_required(f): 
    @wraps(f)
    def decoration(*args, **kwargs): 
    
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] 

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401
        
        try:

            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.mechanic_id = int(data['sub']) #Adding the user_id from the token to the request.
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message': 'invalid token'}), 403
        
        return f(*args, **kwargs)
    
    return decoration


def customer_token_required(f): 
    @wraps(f)
    def decoration(*args, **kwargs): 
    
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] 

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401
        
        try:

            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.customer_id = int(data['sub']) #Adding the user_id from the token to the request.
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message': 'invalid token'}), 403
        
        return f(*args, **kwargs)
    
    return decoration

