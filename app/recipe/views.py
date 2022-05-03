from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Ingredient, Recipe, Tag
from .serializers import (
    DetailSerializer, IngredientSerializer, RecipeSerializer, TagSerializer
)
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
    '''Viewset to manage tags in database'''
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    '''Viewset to manage ingredients in database'''
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    '''Viewset to manage recipes in database'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        '''Return recipes for the authenticated user'''
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return appropriated serializer class'''
        if self.action == 'retrieve':
            return DetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        '''Create recipe'''
        serializer.save(user=self.request.user)
