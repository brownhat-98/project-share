# Generated by Django 5.0.3 on 2024-05-21 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0005_rename_url_book_cover_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]