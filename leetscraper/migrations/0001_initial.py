# Generated by Django 5.1 on 2024-08-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LeetCodeQuestion",
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
                ("question_title", models.CharField(max_length=225)),
                ("difficulty", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="ToDoList",
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
                ("list_name", models.CharField(max_length=30)),
                ("list_description", models.CharField(max_length=200)),
                ("created_time", models.DateField(auto_now_add=True)),
            ],
        ),
    ]
