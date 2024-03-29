# Generated by Django 4.2.9 on 2024-02-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_author_date_of_birth"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="num_copies",
            field=models.IntegerField(
                default=0, help_text="Enter the number of copies available"
            ),
        ),
    ]
