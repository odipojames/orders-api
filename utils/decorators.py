from rest_framework.authtoken.models import Token as AuthToken
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def oidc_protected_resource(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # Check if the Authorization header contains a bearer token
        authorization = request.headers.get('Authorization')
        if not authorization or not authorization.startswith('Bearer '):
            return Response({'error': 'Bearer token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract the token key from the Authorization header
        token_key = authorization.split()[1]

        # Check if the token is valid
        try:
            auth_token = AuthToken.objects.get(key=token_key)
        except AuthToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Call the original view function
        return view_func(self, request, *args, **kwargs)

    return wrapper




  
