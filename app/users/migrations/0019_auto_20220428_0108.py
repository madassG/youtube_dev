# Generated by Django 3.1.4 on 2022-04-27 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20220428_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.subscription'),
        ),
    ]
