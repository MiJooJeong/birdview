# Generated by Django 3.0.3 on 2020-02-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birdview', '0003_auto_20200215_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('skincare', 'skincare'), ('maskpack', 'maskpack'), ('suncare', 'suncare'), ('basemakeup', 'basemakeup')], db_index=True, max_length=10, verbose_name='카테고리'),
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredient_score_dry',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='건성 피부 성분 점수'),
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredient_score_oily',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='지성 피부 성분 점수'),
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredient_score_sensitive',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='민감성 피부 성분 점수'),
        ),
        migrations.AlterField(
            model_name='item',
            name='monthly_sales',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='이번달 판매 수량'),
        ),
    ]
