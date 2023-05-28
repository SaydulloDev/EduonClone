# Generated by Django 4.2.1 on 2023-05-28 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('video', models.FileField(upload_to='course_material/video/')),
                ('file', models.FileField(upload_to='course_material/pdf/')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField()),
                ('tutorial_video', models.FileField(upload_to='tutorial_video/')),
                ('language', models.CharField(max_length=32)),
                ('hours', models.TimeField()),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('sales_price', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduon.category')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduon.comment')),
            ],
        ),
    ]