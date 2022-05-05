from rest_framework import serializers
from core.models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    '''Serializer for the tag objects'''

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    '''Serializer for the ingredient objects'''

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for the recipe objects'''

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link',
                  'ingredients', 'tags']
        read_only_fields = ['id']


class DetailSerializer(RecipeSerializer):
    ''' Serialize the details of a recipe'''

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class ImageSerializer(RecipeSerializer):
    '''Serialize the image of the recipes'''

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only = ['id']
