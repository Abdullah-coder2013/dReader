# Generated by Django 5.0.7 on 2024-07-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionality', '0006_user_profilepic_user_readbooks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]