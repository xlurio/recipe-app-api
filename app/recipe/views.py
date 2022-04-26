from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Return objects for the authenticated user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        ''' Create object'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    '''Lists tags from authenticated user'''
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    '''Lists ingredients from authenticated user'''
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
