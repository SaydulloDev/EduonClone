# Generated by Django 4.2.1 on 2023-05-28 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduon', '0003_alter_course_comment'),
        ('users', '0002_alter_mycourses_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycourses',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_course', to='eduon.course'),
        ),
    ]
