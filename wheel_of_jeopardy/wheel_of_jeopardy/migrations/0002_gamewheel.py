# Generated by Django 2.1.4 on 2019-08-05 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wheel_of_jeopardy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameWheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wheel_sectors', models.TextField(null=True)),
            ],
        ),
    ]
