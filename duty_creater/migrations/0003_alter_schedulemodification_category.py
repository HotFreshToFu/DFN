# Generated by Django 3.2.8 on 2021-11-07 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duty_creater', '0002_schedulemodification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulemodification',
            name='category',
            field=models.CharField(choices=[('PTO', '연차 사용'), ('VAC', '휴가 신청')], max_length=50),
        ),
    ]