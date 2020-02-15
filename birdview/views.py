from rest_framework.response import Response

from birdview.models import Item
from birdview.serializers import ItemListSerializer
from rest_framework import viewsets


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer

    def list(self, request, *args, **kwargs):
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
            self.queryset = Item.objects.filter(category=category)

        return super().list(request, *args, **kwargs)