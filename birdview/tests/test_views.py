from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from birdview.models import Ingredient
from birdview.models import Item


class ItemListViewsetTest(TestCase):

    def test_skin_type을_넣지않고_호출시_ValueError를_발생_시킨다(self):
        client = APIClient()
        with self.assertRaises(ValueError) as error:
            client.get('/products/', format='json')
            self.assertEqual(error.exception.message, 'Please enter skin type.')

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
        response = client.get('/products/?skin_type=oily&include_ingredient=foundation,jurisdiction', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], sample_item_3.name)


class ItemDetailWithRecommendsViewsetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sample_item_1 = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            monthly_sales=5196,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all
        )
        cls.sample_item_2 = Item.objects.create(
            name='이켈 녹차 울트라 하이드레이팅 에센스 마스크',
            price=4640,
            image_id='1d532a02-1d50-4760-8e61-32b88b2a2270',
            monthly_sales=2405,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all,
            ingredient_score_oily=5,
            ingredient_score_dry=2,
            ingredient_score_sensitive=-10,
        )
        cls.sample_item_3 = Item.objects.create(
            name='자연마을 어성초 마스크 팩',
            price=1780,
            image_id='824b6b31-4590-4b54-8793-5c808a024398',
            monthly_sales=5023,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all,
            ingredient_score_oily=16,
            ingredient_score_dry=1,
            ingredient_score_sensitive=4,
        )
        cls.sample_item_4 = Item.objects.create(
            name='오릭스 포 맨 컨트롤 스킨 410ml',
            price=1440,
            image_id='2119924f-75ce-48dc-8a2d-ee71545d6700',
            monthly_sales=1994,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all,
            ingredient_score_oily=10,
            ingredient_score_dry=3,
            ingredient_score_sensitive=3,
        )
        cls.sample_item_5 = Item.objects.create(
            name='겔랑 테라코타 썸머 글로우 하이라이터 10g',
            price=54840,
            image_id='1647f43c-2919-4cbf-9de4-b56a4817779d',
            monthly_sales=2541,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all,
            ingredient_score_oily=20,
            ingredient_score_dry=-14,
            ingredient_score_sensitive=2,
        )
        cls.sample_item_6 = Item.objects.create(
            name='아모레퍼시픽 설화수 설린에센스 50ml',
            price=70660,
            image_id='8e7a54f7-93a6-4572-b6e0-cdd818e4cbd8',
            monthly_sales=3723,
            category=Item.CategoryChoices.skincare,
            gender=Item.GenderChoices.all,
            ingredient_score_oily=12,
            ingredient_score_dry=-18,
            ingredient_score_sensitive=-20,
        )
        sample_ingredient = Ingredient.objects.create(
            name="foundation",
            oily="",
            dry="",
            sensitive="O"
        )
        cls.sample_item_1.ingredient_set.add(sample_ingredient)

    def test_skin_type을_넣지않고_호출시_ValueError를_발생_시킨다(self):
        client = APIClient()
        with self.assertRaises(ValueError) as error:
            client.get('/product/{}/'.format(self.sample_item_1.id), format='json')
            self.assertEqual(error.exception.message, 'Please enter skin type.')

    def test_추천상품이_없는_product_id에_해당하는_상품을_가져온다(self):
        sample_item = Item.objects.create(
            name='리더스 링클 콜라겐 마스크팩',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c1',
            monthly_sales=5196,
            category=Item.CategoryChoices.maskpack,
            gender=Item.GenderChoices.all
        )
        sample_ingredient = Ingredient.objects.create(
            name="foundation",
            oily="",
            dry="",
            sensitive="O"
        )
        sample_item.ingredient_set.add(sample_ingredient)

        client = APIClient()
        response = client.get('/product/{}/?skin_type=oily'.format(sample_item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0],
            {
                "id": sample_item.id,
                "imgUrl": sample_item.full_image_url,
                "name": sample_item.name,
                "price": sample_item.price,
                "gender": sample_item.gender,
                "category": sample_item.category,
                "ingredients": sample_item.ingredients,
                "monthlySales": sample_item.monthly_sales
            }
        )

    def test_product_id에_해당하는_상품과_같은_카테고리의_상위_3개의_지성타입_추천_상품_정보를_조회한다(self):
        client = APIClient()
        response = client.get('/product/{}/?skin_type=oily'.format(self.sample_item_1.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            response.data[0],
            {
                "id": self.sample_item_1.id,
                "imgUrl": self.sample_item_1.full_image_url,
                "name": self.sample_item_1.name,
                "price": self.sample_item_1.price,
                "gender": self.sample_item_1.gender,
                "category": self.sample_item_1.category,
                "ingredients": self.sample_item_1.ingredients,
                "monthlySales": self.sample_item_1.monthly_sales
            }
        )
        self.assertEqual(
            response.data[1],
            {
                "id": self.sample_item_5.id,
                "imgUrl": self.sample_item_5.thumbnail_image_url,
                "name": self.sample_item_5.name,
                "price": self.sample_item_5.price
            }
        )
        self.assertEqual(response.data[2]['name'], self.sample_item_3.name)
        self.assertEqual(response.data[3]['name'], self.sample_item_6.name)

    def test_product_id에_해당하는_상품과_같은_카테고리의_상위_3개의_건성타입_추천_상품_정보를_조회한다(self):
        client = APIClient()
        response = client.get('/product/{}/?skin_type=dry'.format(self.sample_item_1.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            response.data[0],
            {
                "id": self.sample_item_1.id,
                "imgUrl": self.sample_item_1.full_image_url,
                "name": self.sample_item_1.name,
                "price": self.sample_item_1.price,
                "gender": self.sample_item_1.gender,
                "category": self.sample_item_1.category,
                "ingredients": self.sample_item_1.ingredients,
                "monthlySales": self.sample_item_1.monthly_sales
            }
        )
        self.assertEqual(
            response.data[1],
            {
                "id": self.sample_item_4.id,
                "imgUrl": self.sample_item_4.thumbnail_image_url,
                "name": self.sample_item_4.name,
                "price": self.sample_item_4.price
            }
        )
        self.assertEqual(response.data[2]['name'], self.sample_item_2.name)
        self.assertEqual(response.data[3]['name'], self.sample_item_3.name)

    def test_product_id에_해당하는_상품과_같은_카테고리의_상위_3개의_민감성타입_추천_상품_정보를_조회한다(self):
        client = APIClient()
        response = client.get('/product/{}/?skin_type=sensitive'.format(self.sample_item_1.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            response.data[0],
            {
                "id": self.sample_item_1.id,
                "imgUrl": self.sample_item_1.full_image_url,
                "name": self.sample_item_1.name,
                "price": self.sample_item_1.price,
                "gender": self.sample_item_1.gender,
                "category": self.sample_item_1.category,
                "ingredients": self.sample_item_1.ingredients,
                "monthlySales": self.sample_item_1.monthly_sales
            }
        )
        self.assertEqual(
            response.data[1],
            {
                "id": self.sample_item_3.id,
                "imgUrl": self.sample_item_3.thumbnail_image_url,
                "name": self.sample_item_3.name,
                "price": self.sample_item_3.price
            }
        )
        self.assertEqual(response.data[2]['name'], self.sample_item_4.name)
        self.assertEqual(response.data[3]['name'], self.sample_item_5.name)
