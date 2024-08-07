# Generated by Django 5.0.3 on 2024-06-16 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_portfolio_portfolio_pdf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='certificate_pdf',
        ),
        migrations.CreateModel(
            name='CertificateFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('certificate_pdf', models.FileField(blank=True, null=True, upload_to='certificate_pdfs/')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.portfolio')),
            ],
        ),
    ]
