# Generated by Django 5.0.6 on 2024-05-31 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundos', '0012_alter_cadfi_inf_taxa_adm_alter_cadfi_inf_taxa_perfm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadfi',
            name='INF_TAXA_ADM',
            field=models.CharField(blank=True, max_length=1000000, null=True),
        ),
        migrations.AlterField(
            model_name='cadfi',
            name='INF_TAXA_PERFM',
            field=models.CharField(blank=True, max_length=1000000, null=True),
        ),
    ]
