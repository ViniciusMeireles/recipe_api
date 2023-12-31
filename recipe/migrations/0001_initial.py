# Generated by Django 5.0 on 2023-12-11 01:28

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of the recipe', max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Description of the recipe', null=True, verbose_name='Description')),
                ('ingredients', models.TextField(help_text='Ingredients of the recipe', verbose_name='Ingredients')),
                ('instructions', models.TextField(help_text='Instructions of the recipe', verbose_name='Directions')),
                ('prep_time', models.DurationField(help_text='Preparation time of the recipe', validators=[django.core.validators.MinValueValidator(limit_value=datetime.timedelta(seconds=60), message='Preparation time must be equal to or greater than 1 minute.')], verbose_name='Prep Time')),
                ('cook_time', models.DurationField(help_text='Cooking time of the recipe', validators=[django.core.validators.MinValueValidator(limit_value=datetime.timedelta(0), message='Cooking time must be equal to or greater than 0 minutes.')], verbose_name='Cook Time')),
                ('servings', models.IntegerField(default=1, help_text='Servings of the recipe', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Servings must be equal to or greater than 1.')], verbose_name='Servings')),
                ('chef', models.ForeignKey(help_text='Chef who created the recipe', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Chef')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
