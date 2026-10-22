from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('price', models.DecimalField(decimal_places=2, db_index=True, max_digits=10)),
                ('inventory', models.IntegerField(default=5)),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menu Items',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('no_of_guests', models.IntegerField(default=1)),
                ('booking_date', models.DateTimeField(db_index=True)),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
                'ordering': ('booking_date',),
            },
        ),
    ]
