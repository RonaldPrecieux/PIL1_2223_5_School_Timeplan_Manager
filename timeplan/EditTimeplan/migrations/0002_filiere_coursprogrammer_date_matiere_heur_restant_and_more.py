# Generated by Django 4.2.2 on 2023-07-03 22:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("EditTimeplan", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Filiere",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(default="", max_length=15)),
            ],
            options={
                "db_table": "Filiere",
            },
        ),
        migrations.AddField(
            model_name="coursprogrammer",
            name="Date",
            field=models.CharField(
                default="10/05/2023",
                max_length=128,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Le format de date doit être jj/mm/aaaa.",
                        regex="^\\d{2}/\\d{2}/\\d{4}$",
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="matiere",
            name="heur_restant",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="coursprogrammer",
            name="heure_debut",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="coursprogrammer",
            name="heure_fin",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="coursprogrammer",
            name="matiere",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="EditTimeplan.matiere",
            ),
        ),
        migrations.AlterField(
            model_name="matiere",
            name="timing",
            field=models.DurationField(),
        ),
        migrations.AddField(
            model_name="coursprogrammer",
            name="filiere",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="EditTimeplan.filiere",
            ),
        ),
    ]
