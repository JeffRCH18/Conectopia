# Generated by Django 4.1.9 on 2023-08-05 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_comentarios_likes_publicaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicaciones',
            name='fecha_publicacion',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
