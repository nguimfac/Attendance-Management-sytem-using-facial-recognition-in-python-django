# Generated by Django 3.2.3 on 2021-06-13 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0020_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_field', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='fill',
            name='description',
            field=models.CharField(default='Cette filière est destine a des persones tres intelligent et travailleur car il sagit bien d la filière software engineering', max_length=500),
        ),
    ]
