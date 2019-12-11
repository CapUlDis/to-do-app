import calendar, logging, json
from datetime import datetime, timedelta
from jwcrypto import jwt, jwk


logger = logging.getLogger(__file__)

def create_token(username, exp, path_token_key):
    try:
        with open(path_token_key, 'r') as f:
            token_key = jwk.JWK.from_json(f.read())
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {path_token_key}: {err}')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in {path_token_key} is not json: {err}')
        
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"user": username, "exp": calendar.timegm((datetime.utcnow() + timedelta(minutes=exp)).timetuple())})
    token.make_signed_token(token_key)
    return token.serialize()

print(create_token('foo', 30, 'token_key.txt'))

token = jwt.JWT(header={"alg": "HS256"},
                claims={"user": 'username', "exp": calendar.timegm((datetime.utcnow() + timedelta(minutes=30)).timetuple())})
token_key = jwk.JWK.from_json('{"k":"_nYabzvHVPyBDFKFbMGB4twnAuRHWVV_N3yZWYM_Fx8","kty":"oct"}')
token.make_signed_token(token_key)

eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMzkzODEuMCwidXNlciI6InVzZXJuYW1lIn0.x-Ds1Ud_SR8KgL2JaZgdY3quuA1rlpPgD11neSjZVfo

ET = jwt.JWT(key=token_key, jwt=token.serialize())