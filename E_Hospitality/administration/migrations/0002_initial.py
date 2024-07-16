# Generated by Django 5.0.7 on 2024-07-15 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
        ('doctor', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentschedule',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorprofile'),
        ),
        migrations.AddField(
            model_name='appointmentschedule',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patientprofile'),
        ),
        migrations.AddField(
            model_name='department',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorprofile'),
        ),
        migrations.AddField(
            model_name='appointmentschedule',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.department'),
        ),
    ]
