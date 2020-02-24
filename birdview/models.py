import os

from django.db import models
from django.db.models import Model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
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
    category = models.CharField('카테고리', max_length=10, choices=CategoryChoices.choices, db_index=True)
    ingredient_set = models.ManyToManyField('Ingredient', related_name='items')
    monthly_sales = models.PositiveIntegerField('이번달 판매 수량', default=None, blank=True, null=True)
    ingredient_score_oily = models.IntegerField('지성 피부 성분 점수', default=None, blank=True, null=True)
    ingredient_score_dry = models.IntegerField('건성 피부 성분 점수', default=None, blank=True, null=True)
    ingredient_score_sensitive = models.IntegerField('민감성 피부 성분 점수', default=None, blank=True, null=True)

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

    @property
    def ingredients(self):
        # TODO - serializer 설정으로 가능한지 확인 필요
        return ','.join(self.ingredient_set.all().values_list('name', flat=True))

    def calculate_ingredient_score_of_skin_type(self, skin_type: str) -> int:
        """
        피부 타입별로 성분 점수를 계산한다
        :param skin_type: ['oily', 'dry', 'sensitive']
        :return: 성분 점수
        """
        ingredient_score = 0
        for ingredient in self.ingredient_set.all():
            if getattr(ingredient, skin_type) == Ingredient.EffectBySkinType.beneficial:
                ingredient_score += 1
            elif getattr(ingredient, skin_type) == Ingredient.EffectBySkinType.harmful:
                ingredient_score -= 1
            else:
                pass
        return ingredient_score


class Ingredient(TimeStampedModel):
    class EffectBySkinType(DjangoChoices):
        beneficial = ChoiceItem('O')
        harmful = ChoiceItem('X')
        no_effect = ChoiceItem('')

    name = models.CharField('성분명', max_length=100)
    oily = models.CharField('지성 영향', max_length=1, choices=EffectBySkinType.choices)
    dry = models.CharField('건성 영향', max_length=1, choices=EffectBySkinType.choices)
    sensitive = models.CharField('민감성 영향', max_length=1, choices=EffectBySkinType.choices)


def recalculated_ingredient_score_of_skin_type(item: Item):
    """상품의 성분 점수 다시 계산"""
    item.ingredient_score_oily = item.calculate_ingredient_score_of_skin_type('oily')
    item.ingredient_score_dry = item.calculate_ingredient_score_of_skin_type('dry')
    item.ingredient_score_sensitive = item.calculate_ingredient_score_of_skin_type('sensitive')
    item.save()


@receiver(m2m_changed, sender=Item.ingredient_set.through)
def item_ingredients_changed(sender, **kwargs):
    """
    상품의 성분이 변동될 때 마다 각 피부 타입별 성분 점수를 계산
    :param kwargs: https://docs.djangoproject.com/en/2.2/ref/signals/#m2m-changed 참고
    """
    item = kwargs.pop('instance', None)
    recalculated_ingredient_score_of_skin_type(item)

