import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
from boto.s3.connection import S3Connection

AUTH0_DOMAIN = 'dev-uo1xu38y.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting_agency'

#AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
#ALGORITHMS = os.environ["ALGORITHMS"]
#API_AUDIENCE = os.environ["API_AUDIENCE"]

##use this link for login https://dev-uo1xu38y.auth0.com/login?state=g6Fo2SBiRVdXakNCYi1DZko0NUFvQV9oWVRWSTBLa01ZSko1aKN0aWTZIE5BeDhuajZGWEZMTjdycml5SDA4SlA2WC04LXBzZlRYo2NpZNkgOHZRVzc5a1U1dkUzQkpwcm8zYlhmUTR5ZDRWeDU1b2I&client=8vQW79kU5vE3BJpro3bXfQ4yd4Vx55ob&protocol=oauth2&audience=casting_agency&response_type=token&redirect_uri=https%3A%2F%2Fwww.google.com%2F

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    try:
        auth_header=request.headers['Authorization']
        ##print(auth_header)
        header_parts=auth_header.split(' ')
        if len(header_parts) !=2:
                raise AuthError({
                    'code':'invalid_header',
                    'description':'Authorization malformed.'
            },401)
        elif header_parts[0].lower() != 'bearer':
                raise AuthError({
                    'code':'invalid_header',
                    'description':'Authorization malformed.'
            },401)
        return header_parts[1]
    except:
        raise AuthError({
                    'code':'No Authorization header',
                    'description':'Authorization malformed.'
            },401)

   #raise Exception('Not Implemented')

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    ##print("payload Permissions",payload['permissions'],"permissions",permission)
    if(permission not in payload['permissions']):
        raise AuthError({
                    'code':'Unauthorized',
                    'description':'You are unauthorized to do this action'
                },401)
    else:
        return True            

    #return False
    #raise Exception('Not Implemented')

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl=urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    ##print("jsonurl",jsonurl)
    jwks=json.loads(jsonurl.read())
    ##print("jwks",jwks)
    ##print("\n")
    ##print("token",token)
    unverified_header=jwt.get_unverified_header(token)
    ##print("unverified_header",unverified_header)
    rsa_key={}
    if 'kid' not in unverified_header:
        ##print("inside if kid not in")
        raise AuthError({
            'code':'invalid_header',
            'description':'Authorization malformed.'
    },401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            ##print("inside if")
            rsa_key={
                'kty':key['kty'],
                'kid':key['kid'],
                'use':key['use'],
                'n':key['n'],
                'e':key['e']
            }
            ##print("rsa_key",rsa_key)
    if rsa_key:
        try:
            payload=jwt.decode(token,rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://'+AUTH0_DOMAIN+'/'
            )
            ##print(payload)        
            return payload
        except jwt.ExpiredSignatureError:
            print("jwt.ExpiredSignatureError:")
            raise AuthError({
                'code':'token_expired',
                'description':'Token expired.'
             },401)
        except jwt.JWTClaimsError:
            print("jwt.jwtclaims")
            raise AuthError({
                'code':'invalid_claims',
                'description':'Incorrect claims. Please, check the audience and issuer'
             },401)
        except Exception:
            print("exception",Exception)
            raise AuthError({
                'code':'invalid_header',
                'description':'Unable to parse authentication token'
             },401)
        return               
    """ raise AuthError({
            'code':'invalid_header',
            'description':'Authorization malformed.'
    },401) """
    #raise Exception('Not Implemented')

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use   the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            ##print(token)
            try:
                payload = verify_decode_jwt(token)
                print(payload)
                check_permissions(permission, payload)
            except:
               raise AuthError({
                        'code':'UnAuthorized',
                        'description':'Authorization malformed.'
                },401)  
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

    