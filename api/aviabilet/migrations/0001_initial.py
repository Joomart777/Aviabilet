# Generated by Django 4.0.4 on 2022-05-02 09:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Airlines',
            fields=[
                ('slug', models.SlugField(blank=True, max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aviabilet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('Bishkek', 'Bishkek'), ('Almaty', 'Almaty'), ('New York', 'New York'), ('Paris', 'Paris'), ('Istanbul', 'Istanbul'), ('Berlin', 'Berlin'), ('Singapore', 'Singapore'), ('Moscow', 'Moscow'), ('Tbilisi', 'Tbilisi')], default='Bishkek', max_length=20)),
                ('destination_pl', models.CharField(choices=[('Bishkek', 'Bishkek'), ('Almaty', 'Almaty'), ('New York', 'New York'), ('Paris', 'Paris'), ('Istanbul', 'Istanbul'), ('Berlin', 'Berlin'), ('Singapore', 'Singapore'), ('Moscow', 'Moscow'), ('Tbilisi', 'Tbilisi')], default='Berlin', max_length=20)),
                ('status', models.CharField(choices=[('A', 'Available'), ('F', 'Full'), ('N', 'Not Open')], default='A', max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('class_ticket', models.CharField(choices=[('B', 'Business'), ('E', 'Economy')], default='E', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('mobile', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('aviabilet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='aviabilet.aviabilet')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plane', models.CharField(max_length=24)),
                ('origin', models.CharField(choices=[('Bishkek', 'Bishkek'), ('Almaty', 'Almaty'), ('New York', 'New York'), ('Paris', 'Paris'), ('Istanbul', 'Istanbul'), ('Berlin', 'Berlin'), ('Singapore', 'Singapore'), ('Moscow', 'Moscow'), ('Tbilisi', 'Tbilisi')], default='Bishkek', max_length=20)),
                ('destination', models.CharField(choices=[('Bishkek', 'Bishkek'), ('Almaty', 'Almaty'), ('New York', 'New York'), ('Paris', 'Paris'), ('Istanbul', 'Istanbul'), ('Berlin', 'Berlin'), ('Singapore', 'Singapore'), ('Moscow', 'Moscow'), ('Tbilisi', 'Tbilisi')], default='New York', max_length=20)),
                ('depart_time', models.TimeField()),
                ('depart_day', models.DateField(blank=True, null=True)),
                ('duration', models.DurationField(null=True)),
                ('arrival_time', models.TimeField()),
                ('capacity', models.PositiveIntegerField()),
                ('economy_fare', models.PositiveIntegerField(null=True)),
                ('business_fare', models.PositiveIntegerField(null=True)),
                ('airlines', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aviabilet.airlines')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='likess')),
                ('airlines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='aviabilet.airlines', verbose_name='Aviaticket')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='???????????????? ??????????')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='aviabilet.airlines')),
            ],
        ),
        migrations.AddField(
            model_name='aviabilet',
            name='passenger',
            field=models.ManyToManyField(related_name='flight_ticket', to='aviabilet.passenger'),
        ),
        migrations.AddField(
            model_name='aviabilet',
            name='planes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_ticket', to='aviabilet.planes'),
        ),
        migrations.AddField(
            model_name='aviabilet',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight_ticket', to=settings.AUTH_USER_MODEL),
        ),
    ]
