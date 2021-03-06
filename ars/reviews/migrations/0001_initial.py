# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')], default=4)),
                ('content', models.TextField(blank=True, default='')),
                ('student', models.ForeignKey(to='students.Student')),
                ('subject', models.ForeignKey(to='subjects.Subject')),
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'verbose_name': 'Review',
                'db_table': 'review',
            },
        ),
    ]
