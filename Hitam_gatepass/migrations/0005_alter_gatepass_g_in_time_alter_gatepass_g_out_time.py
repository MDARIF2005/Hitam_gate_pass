# Generated by Django 5.1 on 2025-02-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hitam_gatepass', '0004_faculty_hod_mentor_students_gatepass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatepass',
            name='g_in_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='gatepass',
            name='g_out_time',
            field=models.TimeField(),
        ),
    ]
