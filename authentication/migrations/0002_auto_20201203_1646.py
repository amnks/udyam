# Generated by Django 3.1 on 2020-12-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='profile.jpg', upload_to='profile_images/'),
        ),
    ]
