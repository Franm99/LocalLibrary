# Generated by Django 4.2.15 on 2024-09-02 05:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_book_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                    "publish_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Publish Date"
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Add some comments to the review.", max_length=1000
                    ),
                ),
                (
                    "grade",
                    models.FloatField(
                        help_text="Add a grade from 0.0 (awful) to 10.0 (perfect)",
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(10.0),
                        ],
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="catalog.book",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.CheckConstraint(
                check=models.Q(("grade__gte", 0.0), ("grade__lte", 10.0)),
                name="review_grade_min_and_max_limits",
            ),
        ),
    ]
