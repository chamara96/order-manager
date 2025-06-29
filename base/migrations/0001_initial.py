# Generated by Django 5.2 on 2025-05-03 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Home Slider',
                'verbose_name_plural': 'Home Sliders',
                'ordering': ['order'],
            },
        ),
    ]
