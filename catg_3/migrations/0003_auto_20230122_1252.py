# Generated by Django 2.2.15 on 2023-01-22 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catg_3', '0002_auto_20221226_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jrnl_pub',
            name='imp_fac',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='Impact Factor (put 0 if NA)'),
        ),
        migrations.AlterField(
            model_name='prj_outcm',
            name='proj_title',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Title of the Outcome/Output'),
        ),
    ]
