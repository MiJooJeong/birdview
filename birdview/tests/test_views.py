from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from birdview.models import Ingredient
from birdview.models import Item


class ItemListViewsetTest(TestCase):

    def test_get_all_items(self):
        sample_ingredient = Ingredient.objects.create(
            name="foundation",
            oily="",
            dry="",
            sensitive="O"
        )
        sample_item = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196
        )
        sample_item.ingredient_set.add(sample_ingredient)

        client = APIClient()
        response = client.get('/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], sample_item.name)
        self.assertEqual(response.data[0]['price'], sample_item.price)
        self.assertEqual(response.data[0]['imgUrl'], sample_item.thumbnail_image_url)
        self.assertEqual(response.data[0]['monthlySales'], sample_item.monthly_sales)
        self.assertEqual(response.data[0]['ingredients'][0], sample_ingredient.id)

        sample_item.delete()
        sample_ingredient.delete()

    def test_상품_목록을_50개_단위로_페이징한다(self):
        for i in range(1, 52):
            Item.objects.create(
                name='sample_item_{}'.format(i),
                price=i,
                image_id='a18de8cd-c730-4f36-b16f-665cca908c11_{}'.format(i),
                monthly_sales=5196
            )

        client = APIClient()
        response = client.get('/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 51)
        self.assertEqual(len(response.data['results']), 50)


    def test_리스트를_형식에_맞게_보여준다(self):
        sample_ingredient_1 = Ingredient.objects.create(
            name="foundation",
            oily="",
            dry="",
            sensitive="O"
        )
        sample_ingredient_2 = Ingredient.objects.create(
            name="jurisdiction",
            oily="X",
            dry="X",
            sensitive="O"
        )
        sample_item = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196
        )
        sample_item.ingredient_set.add(sample_ingredient_1)
        sample_item.ingredient_set.add(sample_ingredient_2)

        client = APIClient()
        response = client.get('/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0],
            {
                "id": sample_item.id,
                "imgUrl": sample_item.thumbnail_image_url,
                "name": sample_item.name,
                "price": sample_item.price,
                "ingredients": sample_item.ingredients,
                "monthlySales": sample_item.monthly_sales
            }
        )
