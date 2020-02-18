from rest_framework import viewsets
from rest_framework.response import Response

from birdview.models import Item
from birdview.serializers import ItemDetailSerializer
from birdview.serializers import ItemListSerializer
from birdview.serializers import RecommendItemsSerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = ItemListSerializer
        params = request.query_params
        try:
            skin_type = params['skin_type']
        except KeyError:
            raise ValueError('Please enter skin type.')

        if skin_type == 'oily':
            self.queryset = Item.objects.all().order_by('-ingredient_score_oily', 'price')
        elif skin_type == 'dry':
            self.queryset = Item.objects.all().order_by('-ingredient_score_dry', 'price')
        elif skin_type == 'sensitive':
            self.queryset = Item.objects.all().order_by('-ingredient_score_sensitive', 'price')

        category = params.get('category')
        if category:
            self.queryset = self.queryset.filter(category=category)

        exclude_ingredient = params.get('exclude_ingredient')
        if exclude_ingredient:
            exclude_ingredient_name_list = exclude_ingredient.split(',')
            for ingredient in exclude_ingredient_name_list:
                self.queryset = self.queryset.exclude(ingredient_set__name=ingredient)

        include_ingredient = params.get('include_ingredient')
        if include_ingredient:
            include_ingredient_name_list = include_ingredient.split(',')
            for ingredient in include_ingredient_name_list:
                self.queryset = self.queryset.filter(ingredient_set__name=ingredient)

        return super().list(request, *args, **kwargs)

    def detail_with_recommends(self, request, *args, **kwargs):
        self.serializer_class = ItemDetailSerializer
        params = request.query_params
        self.queryset = Item.objects.filter(id=kwargs['pk'])
        try:
            skin_type = params['skin_type']
        except KeyError:
            raise ValueError('Please enter skin type.')

        category = self.queryset.first().category
        recommend_items = None
        if skin_type == 'oily':
            recommend_items = Item.objects.filter(
                category=category).order_by('-ingredient_score_oily', 'price')[:3]
        elif skin_type == 'dry':
            recommend_items = Item.objects.filter(
                category=category).order_by('-ingredient_score_dry', 'price')[:3]
        elif skin_type == 'sensitive':
            recommend_items = Item.objects.filter(
                category=category).order_by('-ingredient_score_sensitive', 'price')[:3]

        serializer = self.get_serializer(self.queryset, many=True)
        recommend_items_serializer = RecommendItemsSerializer(recommend_items, many=True)
        if recommend_items:
            return Response(serializer.data + recommend_items_serializer.data)
        else:
            return Response(serializer.data)
