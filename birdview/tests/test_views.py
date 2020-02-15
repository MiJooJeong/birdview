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
        response = client.get('/products/?skin_type=oily', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], sample_item.name)
        self.assertEqual(response.data['results'][0]['price'], sample_item.price)
        self.assertEqual(response.data['results'][0]['imgUrl'], sample_item.thumbnail_image_url)
        self.assertEqual(response.data['results'][0]['monthlySales'], sample_item.monthly_sales)
        self.assertEqual(response.data['results'][0]['ingredients'], sample_ingredient.name)

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
        response = client.get('/products/?skin_type=oily', format='json')
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
        response = client.get('/products/?skin_type=oily', format='json')
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

    def test_지성_피부_타입에_대해_성분_점수가_높은_상품_순으로_정렬한다(self):
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            ingredient_score_oily=1
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2270',
            monthly_sales=2405,
            ingredient_score_oily=3
        )
        sample_item_3 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2272',
            monthly_sales=2405,
            ingredient_score_oily=2
        )

        client = APIClient()
        response = client.get('/products/?skin_type=oily', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], sample_item_2.name)
        self.assertEqual(response.data['results'][1]['name'], sample_item_3.name)
        self.assertEqual(response.data['results'][2]['name'], sample_item_1.name)

    def test_건성_피부_타입에_대해_성분_점수가_높은_상품_순으로_정렬한다(self):
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            ingredient_score_dry=1
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2270',
            monthly_sales=2405,
            ingredient_score_dry=3
        )
        sample_item_3 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2272',
            monthly_sales=2405,
            ingredient_score_dry=2
        )

        client = APIClient()
        response = client.get('/products/?skin_type=dry', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], sample_item_2.name)
        self.assertEqual(response.data['results'][1]['name'], sample_item_3.name)
        self.assertEqual(response.data['results'][2]['name'], sample_item_1.name)

    def test_민감성_피부_타입에_대해_성분_점수가_높은_상품_순으로_정렬한다(self):
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            ingredient_score_sensitive=1
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2271',
            monthly_sales=2405,
            ingredient_score_sensitive=3
        )
        sample_item_3 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2272',
            monthly_sales=2405,
            ingredient_score_sensitive=2
        )

        client = APIClient()
        response = client.get('/products/?skin_type=sensitive', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], sample_item_2.name)
        self.assertEqual(response.data['results'][1]['name'], sample_item_3.name)
        self.assertEqual(response.data['results'][2]['name'], sample_item_1.name)

    def test_카테고리를_선택하면_선택한_카테고리의_아이템만_보여준다(self):
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            category=Item.CategoryChoices.skincare
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2271',
            monthly_sales=2405,
            category=Item.CategoryChoices.basemakeup
        )

        client = APIClient()
        response = client.get('/products/?skin_type=oily&category=basemakeup', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], sample_item_2.name)

    def test_제외해야_하는_성분들을_지정하면_모두_포함하지_않은_상품만_보여준다(self):
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
        sample_ingredient_3 = Ingredient.objects.create(
            name="jurisdion",
            oily="X",
            dry="X",
            sensitive="O"
        )
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            category=Item.CategoryChoices.skincare
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2271',
            monthly_sales=2405,
            category=Item.CategoryChoices.basemakeup
        )
        sample_item_3 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크2',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a22w71',
            monthly_sales=2405,
            category=Item.CategoryChoices.basemakeup
        )
        sample_item_1.ingredient_set.add(sample_ingredient_1)
        sample_item_2.ingredient_set.add(sample_ingredient_2)
        sample_item_3.ingredient_set.add(sample_ingredient_1)
        sample_item_3.ingredient_set.add(sample_ingredient_3)

        client = APIClient()
        response = client.get('/products/?skin_type=oily&exclude_ingredient=foundation,jurisdion')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], sample_item_2.name)

    def test_포함해야_하는_성분들을_지정하면_모두_포함하는_상품만_보여준다(self):
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
        sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            category=Item.CategoryChoices.skincare
        )
        sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2271',
            monthly_sales=2405,
            category=Item.CategoryChoices.basemakeup
        )
        sample_item_3 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크2',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a22w71',
            monthly_sales=2405,
            category=Item.CategoryChoices.basemakeup
        )
        sample_item_1.ingredient_set.add(sample_ingredient_1)
        sample_item_2.ingredient_set.add(sample_ingredient_2)
        sample_item_3.ingredient_set.add(sample_ingredient_1)
        sample_item_3.ingredient_set.add(sample_ingredient_2)

        client = APIClient()
        response = client.get('/products/?skin_type=oily&include_ingredient=foundation,jurisdiction')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], sample_item_3.name)