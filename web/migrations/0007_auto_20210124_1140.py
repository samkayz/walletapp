# Generated by Django 3.1.5 on 2021-01-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20210124_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='acctno',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='bank',
            field=models.TextField(blank=True, null=True),
        ),
    ]
