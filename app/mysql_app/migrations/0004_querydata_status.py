# Generated by Django 4.1.4 on 2022-12-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysql_app', '0003_instance_domain_alter_instance_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='querydata',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]