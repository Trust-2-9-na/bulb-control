# Generated by Django 5.1 on 2024-09-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0002_alter_sensordata_humidity'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulbControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ON', 'On'), ('OFF', 'Off')], default='OFF', max_length=3)),
            ],
        ),
    ]
