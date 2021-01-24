# Generated by Django 3.1.5 on 2021-01-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(blank=True, choices=[(0, 'processing'), (1, 'done')], db_index=True, default=0, max_length=10),
        ),
    ]
