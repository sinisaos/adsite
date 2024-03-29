# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-01 13:05
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ad",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("electronics", "Electronics"),
                            ("software", "Software"),
                            ("home", "Home"),
                            ("clothes", "Clothes"),
                        ],
                        default="electronics",
                        max_length=100,
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=100)),
                ("content", models.TextField()),
                ("price", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_sold", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="attachments")),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="ads.Ad",
                    ),
                ),
            ],
        ),
    ]
