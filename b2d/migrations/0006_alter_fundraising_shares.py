# Generated by Django 5.1 on 2024-11-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2d', '0005_remove_investment_shares_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundraising',
            name='shares',
            field=models.PositiveIntegerField(),
        ),
    ]
