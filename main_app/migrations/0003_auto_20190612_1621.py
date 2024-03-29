# Generated by Django 2.2 on 2019-06-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_training'),
    ]

    operations = [
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='training',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='training',
            name='steez',
            field=models.CharField(choices=[('C', 'Cruise'), ('S', 'Street'), ('P', 'Park')], default='C', max_length=1),
        ),
        migrations.AddField(
            model_name='trick',
            name='parks',
            field=models.ManyToManyField(to='main_app.Park'),
        ),
    ]
