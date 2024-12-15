import jwt
from flask import current_app

def decode_token(token):
    """
    Decodes the JWT token to extract the user ID.
    
    Args:
        token (str): The JWT token.

    Returns:
        int: The user ID extracted from the token.

    Raises:
        Exception: If the token is invalid or expired.
    """
    print(str(token))
    if not isinstance(token, str):
        raise Exception("Invalid token: Expected a string value")
    try:
        # Decode the token using the secret key and algorithm from app config
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return payload['user_id']  # Ensure your token includes the 'user_id' field
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
