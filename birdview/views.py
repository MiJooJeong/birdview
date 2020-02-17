from birdview.models import Item
from birdview.serializers import ItemDetailSerializer
from birdview.serializers import ItemListSerializer
from rest_framework import viewsets


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
