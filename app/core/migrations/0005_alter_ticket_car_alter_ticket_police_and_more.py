# Generated by Django 5.0.6 on 2024-07-05 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_vehicle_user_vehicle_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='core.vehicle'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='police',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='core.police'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]