# Generated by Django 5.1 on 2024-09-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_review_review_review_grade_min_and_max_limits'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('date_of_birth__lt', models.F('date_of_death'))), name='author_date_of_birth_lower_than_date_of_death'),
        ),
    ]
