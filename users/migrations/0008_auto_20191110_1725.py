# Generated by Django 2.2.6 on 2019-11-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20191107_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.FloatField(default=0.0),
        ),
    ]