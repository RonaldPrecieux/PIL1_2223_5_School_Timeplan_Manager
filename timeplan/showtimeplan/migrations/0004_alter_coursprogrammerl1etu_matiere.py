# Generated by Django 4.2.2 on 2023-06-28 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("EditTimeplan", "0002_coursprogrammer_coursprogrammerl1_and_more"),
        ("showtimeplan", "0003_coursprogrammeretu_coursprogrammerl1etu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursprogrammerl1etu",
            name="matiere",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="EditTimeplan.matiere"
            ),
        ),
    ]
