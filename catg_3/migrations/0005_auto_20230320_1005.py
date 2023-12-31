# Generated by Django 2.2.15 on 2023-03-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catg_3', '0004_auto_20230308_0544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jrnl_pub',
            options={'ordering': ('-yr_pub',)},
        ),
        migrations.AlterField(
            model_name='jrnl_pub',
            name='role_appl',
            field=models.CharField(blank=True, choices=[(None, 'Select'), ('F_A', 'First author'), ('C_A', 'Corresponding author / supervisor / mentor'), ('FC_A', 'First and Corresponding author'), ('O_A', 'Other')], max_length=50, null=True, verbose_name='Role of Applicant'),
        ),
    ]
