import json
import os

from birdview import settings
from birdview.models import Ingredient
from birdview.models import Item


def insert_sample_data_into_database():
    # Ingredient
    with open(os.path.join(settings.BASE_DIR, 'ingredient-data.json')) as ingredient_data_file:
        ingredient_data_list = json.load(ingredient_data_file)
        for ingredient_data in ingredient_data_list:
            Ingredient.objects.create(
                name=ingredient_data['name'],
                oily=ingredient_data['oily'],
                dry=ingredient_data['dry'],
                sensitive=ingredient_data['sensitive'],
            )

    # Item
    with open(os.path.join(settings.BASE_DIR, 'item-data.json')) as item_data_file:
        item_data_list = json.load(item_data_file)
        for i, item_data in enumerate(item_data_list):
            item = Item.objects.create(
                name=item_data['name'],
                image_id=item_data['imageId'],
                price=item_data['price'],
                gender=item_data['gender'],
                category=item_data['category'],
                monthly_sales=item_data['monthlySales']
            )
            for ingredient_name in item_data['ingredients'].split(','):
                ingredient = Ingredient.objects.get(name=ingredient_name)
                item.ingredient_set.add(ingredient)
            print("{}th Item created".format(i))