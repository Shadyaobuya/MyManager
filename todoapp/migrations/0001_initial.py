# Generated by Django 3.2.5 on 2021-07-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=100)),
                ('priority', models.IntegerField(default=1)),
                ('duration', models.IntegerField(default=30)),
            ],
        ),
    ]
