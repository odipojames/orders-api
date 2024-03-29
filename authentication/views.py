from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser as User
from rest_framework.authtoken.views import ObtainAuthToken
from utils.decorators import oidc_protected_resource
from rest_framework.authtoken.models import Token as AuthToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type="object",
    required=["username", "password"],
    properties={
        "username": openapi.Schema(type="string", description="Username of the user to register"),
        "password": openapi.Schema(type="string", description="Password of the user to register"),
    },
))
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.create_user(username=username, password=password)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Delete existing tokens associated with the user
        AuthToken.objects.filter(user=user).delete()
        # Create a new authentication token
        token = AuthToken.objects.create(user=user)
        return Response({'token': token.key})





