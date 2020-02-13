import os

from django.db import models
from django_extensions.db.models import TimeStampedModel

from djchoices import ChoiceItem
from djchoices import DjangoChoices


class Item(TimeStampedModel):
    class GenderChoices(DjangoChoices):
        female = ChoiceItem('female')
        male = ChoiceItem('male')
        all = ChoiceItem('all')

    class CategoryChoices(DjangoChoices):
        skincare = ChoiceItem('skincare')
        maskpack = ChoiceItem('maskpack')
        suncare = ChoiceItem('suncare')
        basemakeup = ChoiceItem('basemakeup')

    name = models.CharField('상품명', max_length=100, unique=True)
    price = models.PositiveIntegerField('가격', default=0)
    image_id = models.CharField('상품 이미지 id', max_length=100, unique=True)
    gender = models.CharField('성별', max_length=6, choices=GenderChoices.choices)
    category = models.CharField('카테고리', max_length=10, choices=CategoryChoices.choices)
    # TODO - Ingredients 모델 생성 후, FK 설정
    ingredient = models.TextField('구성 성분 이름')
    monthly_sales = models.PositiveIntegerField('이번달 판매 수량', default=0)

    IMAGE_BASE_URL = 'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview'

    @property
    def image_file_name(self):
        return self.image_id + '.jpg'

    @property
    def full_image_url(self):
        return os.path.join(self.IMAGE_BASE_URL, 'image', self.image_file_name)

    @property
    def thumbnail_image_url(self):
        return os.path.join(self.IMAGE_BASE_URL, 'thumbnail', self.image_file_name)


