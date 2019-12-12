import calendar, logging, json
from datetime import datetime, timedelta
from jwcrypto import jwt, jwk, jws


logger = logging.getLogger(__file__)

def load_token_key(path_token_key):
    try:
        with open(path_token_key, 'r') as f:
            token_key = jwk.JWK.from_json(f.read())
            return token_key
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {path_token_key}: {err}')
        raise FileNotFoundError
    except jwk.InvalidJWKValue as err:
        logger.error(f'InvalidJWKValue: data in {path_token_key} is not JWK object')     
        raise TypeError   
    
class Token:

    def __init__(self, path_token_key):
        self.load_key = load_token_key(path_token_key)

    def create_new_token(self, username, token_exp):
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"user": username, "exp": calendar.timegm((datetime.utcnow() + timedelta(minutes = token_exp)).timetuple())})
        token.make_signed_token(self.load_key)
        return token.serialize()

    def check_token(self, token):
        try:
            jwt.JWT(key = self.load_key, jwt = token)
            return True
        except jwt.JWTExpired:
            return False
        except jws.InvalidJWSSignature:
            return False
        except ValueError:
            return False

import time

token = Token('token_key.txt')
print(token.create_new_token('foobar', 30))
print(token.check_token(token.create_new_token('foobar', 30)))
expired = token.create_new_token('foo', -60)
time.sleep(10)
print(token.check_token(expired))
print(token.check_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiBEb2UifQ.o8ykfFoug3b7lPlNcSdK_wJnzYt34ZASHfGdW9PExN8'))
print(token.check_token('foo'))







'''print(create_token('foo', 30, 'token_key.txt'))

token = jwt.JWT(header={"alg": "HS256"},
                claims={"user": 'foo', "exp": calendar.timegm((datetime.utcnow() + timedelta(minutes=1)).timetuple())})
token_key = jwk.JWK.from_json('{"k":"_nYabzvHVPyBDFKFbMGB4twnAuRHWVV_N3yZWYM_Fx8","kty":"oct"}')
token.make_signed_token(token_key)
token.serialize()

ET = jwt.JWT(key=token_key, jwt=token.serialize())

ET = jwt.JWT(key=token_key, jwt='eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwNjgyNTAsInVzZXIiOiJmb28ifQ.YxKlnoeOOMgmTNXZQDw-qkbHDWyHY0Wst99oHazxXJE')



eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMzkzODEuMCwidXNlciI6InVzZXJuYW1lIn0.x-Ds1Ud_SR8KgL2JaZgdY3quuA1rlpPgD11neSjZVfo'''

