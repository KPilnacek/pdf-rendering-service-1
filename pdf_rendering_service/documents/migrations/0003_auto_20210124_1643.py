# Generated by Django 3.1.5 on 2021-01-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20210124_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'processing'), (1, 'done')], db_index=True, default=0),
        ),
    ]
