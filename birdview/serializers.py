from rest_framework import serializers

from birdview.models import Item


class ItemListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.CharField(source='thumbnail_image_url')
    monthlySales = serializers.IntegerField(source='monthly_sales')

    class Meta:
        model = Item
        fields = ['id', 'imgUrl', 'name', 'price', 'ingredients', 'monthlySales']
