# Generated by Django 4.2.2 on 2023-07-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "EditTimeplan",
            "0002_filiere_coursprogrammer_date_matiere_heur_restant_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="matiere",
            name="heur_restant",
        ),
        migrations.AlterField(
            model_name="matiere",
            name="timing",
            field=models.IntegerField(default=0),
        ),
    ]