# Generated by Django 4.0.3 on 2022-04-10 21:34

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('categories', djongo.models.fields.JSONField()),
                ('description', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_of_occurrence', models.DateTimeField()),
                ('location', djongo.models.fields.EmbeddedField(model_container=events.models.Address)),
                ('ratings', djongo.models.fields.ArrayField(default=[], model_container=events.models.Rating)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
