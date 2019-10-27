import jwt
from datetime import datetime, timedelta

payload = {
    'iat': datetime.now(),
    'exp': datetime.now() + timedelta(hours=1),
    'data': {
        'id': 1
        }
}

token = jwt.encode(payload, "dev key", algorithm='HS256').decode('ascii')

pl = jwt.decode(token, "dev key", algorithm='HS256')

print(pl)
