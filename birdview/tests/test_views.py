from django.test import TestCase
from rest_framework import status

from birdview.models import Item
from rest_framework.test import APIClient


class ItemListViewsetTest(TestCase):

    def test_get_all_items(self):
        sample_item = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            ingredient='executrix,provision,multimedia,destruction,screw',
            monthly_sales=5196
        )

        client = APIClient()
        response = client.get('/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], sample_item.name)
        self.assertEqual(response.data[0]['imgUrl'], sample_item.thumbnail_image_url)
        self.assertEqual(response.data[0]['price'], sample_item.price)
        self.assertEqual(response.data[0]['ingredient'], sample_item.ingredient)
        self.assertEqual(response.data[0]['monthlySales'], sample_item.monthly_sales)
