# Generated by Django 5.0.3 on 2024-05-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deskhelp", "0013_alter_ticket_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="reporter",
            field=models.CharField(max_length=50, verbose_name="Zgłaszający"),
        ),
    ]