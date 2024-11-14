# Generated by Django 5.1.3 on 2024-11-14 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UAV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('model', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UAVType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('is_montage_team', models.BooleanField(default=False)),
                ('part_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uav_manufacturing_application.parttype')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('team', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='uav_manufacturing_application.team')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('part_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uav_manufacturing_application.parttype')),
                ('uav', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uav_manufacturing_application.uav')),
                ('uav_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uav_manufacturing_application.uavtype')),
            ],
        ),
    ]