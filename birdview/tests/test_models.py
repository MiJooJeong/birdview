from django.test import TestCase
from birdview.models import Item


class ItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sample_item = Item.objects.create(
            name='리더스 링클 콜라겐 마스크',
            price=520,
            image_id='a18de8cd-c730-4f36-b16f-665cca908c11',
            gender=Item.GenderChoices.female,
            category=Item.CategoryChoices.skincare,
            ingredient='executrix,provision,multimedia,destruction,screw',
            monthly_sales=5196
        )

    def test_image_file_name(self):
        self.assertEqual(
            self.sample_item.image_file_name, 'a18de8cd-c730-4f36-b16f-665cca908c11.jpg'
        )

    def test_full_image_url(self):
        self.assertEqual(
            self.sample_item.full_image_url,
            'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/a18de8cd-c730-4f36-b16f-665cca908c11.jpg'
        )

    def test_thumbnail_image_url(self):
        self.assertEqual(
            self.sample_item.thumbnail_image_url,
            'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/a18de8cd-c730-4f36-b16f-665cca908c11.jpg'
        )
