# Generated by Django 3.1.5 on 2021-01-24 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=255, null=True)),
                ('bal', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'wallet',
            },
        ),
    ]
