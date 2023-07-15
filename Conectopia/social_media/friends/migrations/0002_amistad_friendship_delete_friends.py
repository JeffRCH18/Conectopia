# Generated by Django 4.1.9 on 2023-07-15 14:20

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_usuarios_user_description'),
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amistad',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='usuarios.usuarios')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='usuarios.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('Stade', models.CharField(max_length=20)),
                ('Id_emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to='usuarios.usuarios')),
                ('Id_receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to='usuarios.usuarios')),
            ],
        ),
        migrations.DeleteModel(
            name='Friends',
        ),
    ]
