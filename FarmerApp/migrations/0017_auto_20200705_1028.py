# Generated by Django 3.0.8 on 2020-07-05 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FarmerApp', '0016_cropseeds_fertilizer_pesticide'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cropseeds',
            old_name='photo',
            new_name='image',
        ),
    ]
