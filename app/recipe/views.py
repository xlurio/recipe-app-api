from rest_framework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Ingredient, Recipe, Tag
from .serializers import (
    DetailSerializer, ImageSerializer, IngredientSerializer, RecipeSerializer,
    TagSerializer
)
from rest_framework.response import Response
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

    def _params_to_int(self, param):
        '''Convert a list of numeric strings into a list of integers'''
        return [int(str_id) for str_id in param.split(',')]

    def get_queryset(self):
        '''Return recipes for the authenticated user'''
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_int(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredients_ids = self._params_to_int(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)

        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return appropriated serializer class'''
        if self.action == 'retrieve':
            return DetailSerializer
        if self.action == 'upload_image':
            return ImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        '''Create recipe'''
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        '''Upload image to API'''
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
