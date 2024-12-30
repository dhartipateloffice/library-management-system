# Generated by Django 5.1.1 on 2024-09-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subapp', '0003_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('librarian', 'Librarian')], max_length=10),
        ),
    ]
