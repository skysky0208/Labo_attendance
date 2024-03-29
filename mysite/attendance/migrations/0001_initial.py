
# Generated by Django 3.0.6 on 2022-05-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabAttendanceTb',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(blank=True, max_length=100, null=True)),
                ('room_id', models.CharField(blank=True, choices=[('16_321', '16号館321室'), ('16_421', '16号館421室'), ('16_422', '16号館422室')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('mail', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('calendar_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'Lab_attendance_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LabFingerprintTb',
            fields=[
                ('finger_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Lab_fingerprint_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LabReport',
            fields=[
                ('student_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('enter_time', models.TimeField(blank=True, null=True)),
                ('staytime', models.IntegerField(blank=True, null=True)),
                ('count', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Lab_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LabTips',
            fields=[
                ('sentence', models.TextField(blank=True, db_column='Sentence', null=True)),
                ('image', models.CharField(blank=True, db_column='Image', max_length=100, null=True)),
                ('num', models.AutoField(db_column='Num', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Lab_tips',
                'managed': False,
            },
        ),
    ]
