# Generated by Django 4.1.9 on 2023-07-16 03:18

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_usuarios_user_description'),
        ('friends', '0002_amistad_friendship_delete_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('Stade', models.CharField(max_length=20)),
                ('Id_emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to='usuarios.usuarios')),
                ('Id_receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to='usuarios.usuarios')),
            ],
        ),
        migrations.DeleteModel(
            name='Friendship',
        ),
    ]
