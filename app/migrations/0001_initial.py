# Generated by Django 3.2.4 on 2021-06-15 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')),
                ('position', models.PositiveIntegerField(unique=True, verbose_name='مختصات')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آیپی')),
            ],
            options={
                'verbose_name': 'آیپی',
                'verbose_name_plural': 'آیپی ها',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان عکس')),
                ('slug', models.CharField(max_length=250, unique=True, verbose_name='آدرس عکس')),
                ('img', models.ImageField(upload_to='', verbose_name='عکس شما')),
                ('status', models.CharField(choices=[('p', 'منتشر شده'), ('i', 'در حال بررسی'), ('b', 'برگشت داده شده')], max_length=1, verbose_name='وضعیت انتشار')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category', verbose_name='دسته بندی')),
                ('download_count', models.ManyToManyField(blank=True, related_name='downloads', to=settings.AUTH_USER_MODEL, verbose_name='تعداد دانلود ها')),
                ('hits', models.ManyToManyField(blank=True, related_name='hits', to='app.Ip', verbose_name='بازدید ها')),
                ('likes_count', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='تعداد پسند ها')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'ordering': ['-created'],
            },
        ),
    ]
