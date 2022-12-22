# Generated by Django 4.1.1 on 2022-12-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cpu_gpu_ram'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gpu_model',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ram_model',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
