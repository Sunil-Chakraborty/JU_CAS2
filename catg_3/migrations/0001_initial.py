# Generated by Django 2.2.15 on 2022-04-24 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jrnl_pub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yr_pub', models.PositiveIntegerField(blank=True, null=True, verbose_name='Year of Publication')),
                ('title_pub', models.CharField(blank=True, max_length=300, null=True, verbose_name='Title of the Paper')),
                ('no_auth', models.PositiveIntegerField(blank=True, null=True, verbose_name='No.of authors')),
                ('role_appl', models.CharField(blank=True, choices=[(None, 'Select'), ('F_A', 'First author'), ('C_A', 'Corresponding author/supervisor/mentor'), ('FC_A', 'First and Corresponding author'), ('O_A', 'Other')], max_length=50, null=True, verbose_name='Role of Applicant')),
                ('jrnl_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Journal Name')),
                ('vl_pg', models.CharField(blank=True, max_length=300, null=True, verbose_name='Volume (Issue), pg no. from - to')),
                ('jrnl_type', models.CharField(blank=True, choices=[(None, 'Select'), ('UGC', 'UGC Care List'), ('OTHER', 'Other reputed journal as notified by UGC')], max_length=50, null=True, verbose_name='Journal Type')),
                ('imp_fac', models.PositiveIntegerField(blank=True, null=True, verbose_name='Impact Factor (put 0 if NA)')),
                ('jrnl_url', models.CharField(blank=True, max_length=500, null=True, verbose_name='Link of Journal page showing impact factor')),
                ('jrnl_pdf', models.FileField(blank=True, null=True, upload_to='jrnl_pub/pdfs/', verbose_name='Upload Paper(PDF)')),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]