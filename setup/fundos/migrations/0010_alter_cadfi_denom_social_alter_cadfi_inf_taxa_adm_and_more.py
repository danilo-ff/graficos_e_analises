# Generated by Django 5.0.6 on 2024-05-31 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundos', '0009_alter_informediario_tp_fundo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadfi',
            name='DENOM_SOCIAL',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cadfi',
            name='INF_TAXA_ADM',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='cadfi',
            name='INF_TAXA_PERFM',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
