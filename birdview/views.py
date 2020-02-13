from birdview.models import Item
from birdview.serializers import ItemListSerializer
from rest_framework import viewsets


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
