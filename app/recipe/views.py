from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tag
from .serializers import TagSerializer
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    '''Lists tags from authenticated user'''
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Return tags for the authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Creates a new tag'''
        serializer.save(user=self.request.user)
