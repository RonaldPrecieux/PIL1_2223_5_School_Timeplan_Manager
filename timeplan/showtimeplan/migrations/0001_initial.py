# Generated by Django 4.2.2 on 2023-07-01 06:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("EditTimeplan", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                (
                    "nom",
                    models.CharField(
                        max_length=120,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "prenom",
                    models.CharField(
                        max_length=120,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("numero_telephone", models.CharField(max_length=20)),
                ("mot_de_passe", models.CharField(max_length=128)),
                ("code_de_confirmation", models.IntegerField(default=None, null=True)),
            ],
            options={
                "db_table": "etudiants_enregistres",
            },
        ),
        migrations.CreateModel(
            name="CoursProgrammerL1Etu",
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
                (
                    "Date",
                    models.CharField(
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
                ("jour", models.CharField(max_length=128)),
                ("promotion", models.CharField(max_length=128)),
                ("heure_debut", models.CharField(max_length=150)),
                ("heure_fin", models.CharField(max_length=150)),
                ("salle", models.CharField(max_length=150)),
                ("teacher", models.CharField(default="", max_length=128)),
                ("groupe", models.CharField(max_length=128)),
                (
                    "matiere",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="EditTimeplan.matiere",
                    ),
                ),
            ],
            options={
                "db_table": "coursProgrammerL1Etu",
            },
        ),
    ]
