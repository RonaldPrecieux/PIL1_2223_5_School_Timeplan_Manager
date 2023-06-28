# Generated by Django 4.2.2 on 2023-06-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtimeplan', '0002_user_delete_etudiants'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursProgrammerEtu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(max_length=100)),
                ('promotion', models.CharField(max_length=128)),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('matiere', models.CharField(max_length=150)),
                ('salle', models.CharField(max_length=150)),
                ('teacher', models.CharField(default='', max_length=128)),
            ],
            options={
                'db_table': 'coursProgrammerEtu',
            },
        ),
        migrations.CreateModel(
            name='CoursProgrammerL1Etu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default='2023-05-10')),
                ('jour', models.CharField(max_length=128)),
                ('promotion', models.CharField(max_length=128)),
                ('heure_debut', models.CharField(max_length=150)),
                ('heure_fin', models.CharField(max_length=150)),
                ('matiere', models.CharField(max_length=150)),
                ('salle', models.CharField(max_length=150)),
                ('teacher', models.CharField(default='', max_length=128)),
                ('groupe', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'coursProgrammerL1Etu',
            },
        ),
    ]