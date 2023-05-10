# Generated by Django 3.2.3 on 2023-05-10 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0005_alter_friendshiprequest_status_req'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendshiprequest',
            name='status_req',
            field=models.CharField(choices=[('send', 'отправлен'), ('accepted', 'принят'), ('rejected', 'отказан')], max_length=24, verbose_name='Статус заявки'),
        ),
    ]
