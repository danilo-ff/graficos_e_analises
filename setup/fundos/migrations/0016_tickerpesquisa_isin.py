# Generated by Django 5.0.6 on 2024-07-14 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundos', '0015_tickerpesquisa'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickerpesquisa',
            name='ISIN',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
