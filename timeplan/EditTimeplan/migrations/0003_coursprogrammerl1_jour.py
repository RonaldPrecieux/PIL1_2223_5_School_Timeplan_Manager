# Generated by Django 4.2.2 on 2023-06-25 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EditTimeplan", "0002_coursprogrammer_coursprogrammerl1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursprogrammerl1",
            name="jour",
            field=models.DateField(default="2023-05-10"),
        ),
    ]