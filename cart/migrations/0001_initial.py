# Generated by Django 4.0.4 on 2022-08-18 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('realname', models.CharField(max_length=10)),
                ('artist_name', models.CharField(max_length=30)),
                ('team', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('artist_intro', models.TextField(max_length=300)),
                ('post_intro', models.TextField(max_length=300)),
                ('post_plan', models.TextField()),
                ('ok', models.BooleanField(default=False)),
                ('post_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('post_place', models.TextField()),
                ('startday', models.DateField(null=True)),
                ('endday', models.DateField(null=True)),
                ('tag', models.ManyToManyField(to='tag.tag', verbose_name='태그')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'post',
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_image/')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='cart.post')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
    ]
