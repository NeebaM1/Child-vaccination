# Generated by Django 5.0.7 on 2024-10-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hs_name', models.CharField(max_length=60)),
                ('hs_place', models.CharField(max_length=30)),
            ],
        ),
    ]
