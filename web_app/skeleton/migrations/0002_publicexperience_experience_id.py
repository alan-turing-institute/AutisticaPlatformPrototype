# Generated by Django 2.2.3 on 2019-07-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skeleton', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicexperience',
            name='experience_id',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]