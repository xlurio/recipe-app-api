from rest_framework.settings import api_settings
from .serializers import AuthTokenSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class CreateUserView(CreateAPIView):
    '''View that creates a user from a POST request'''
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''Create and show user auth token'''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    '''View that helps managing the user profile'''
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        '''Retrieve and return the authenticated user informations'''
        return self.request.user
