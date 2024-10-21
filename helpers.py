import json
import urllib.parse
import gzip
import base64

# def encode_state(state):
#    # Serialize the state to JSON
#    state_json = json.dumps(state)

#    # Compress the JSON string using gzip
#    compressed_state = gzip.compress(state_json.encode('utf-8'))

#    # Encode the compressed data in Base64
#    encoded_state = base64.urlsafe_b64encode(compressed_state).decode('utf-8')

#    # URL-encode the Base64 string to ensure it is safe for URLs
#    url_safe_encoded_state = urllib.parse.quote(encoded_state)

#    return url_safe_encoded_state

# def decode_state(encoded_state):
#    # Decode the URL-encoded Base64 string
#    decoded_state = urllib.parse.unquote(encoded_state)

#    # Fix padding (if needed) and decode Base64

#    decoded_state += '=' * (-len(decoded_state) % 4)
#    compressed_state = base64.urlsafe_b64decode(decoded_state.encode('utf-8'))

#    # Decompress the gzip data
#    state_json = gzip.decompress(compressed_state).decode('utf-8')

#    # Convert the JSON string back to a Python dictionary
#    state = json.loads(state_json)

#    return state
