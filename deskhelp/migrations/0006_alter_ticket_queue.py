# Generated by Django 5.0.3 on 2024-05-15 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deskhelp", "0005_department_ticket_queue_queue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="queue",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="deskhelp.queue",
            ),
        ),
    ]
