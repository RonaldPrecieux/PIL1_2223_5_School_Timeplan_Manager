# Generated by Django 4.2.2 on 2023-06-17 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showtimeplan', '0005_alter_user_confirmer_mot_de_passe_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='etudiants_enregistres',
        ),
    ]