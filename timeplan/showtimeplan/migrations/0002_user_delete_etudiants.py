# Generated by Django 4.2.2 on 2023-06-25 20:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showtimeplan", "0001_initial"),
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
        migrations.DeleteModel(
            name="Etudiants",
        ),
    ]