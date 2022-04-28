# Generated by Django 4.0.3 on 2022-04-28 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='core.ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='core.tag'),
        ),
    ]
