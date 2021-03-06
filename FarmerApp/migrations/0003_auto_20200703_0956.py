# Generated by Django 3.0.8 on 2020-07-03 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FarmerApp', '0002_buyer_farmer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
                'ordering': ('name',),
            },
        ),
        migrations.DeleteModel(
            name='Crops',
        ),
    ]
