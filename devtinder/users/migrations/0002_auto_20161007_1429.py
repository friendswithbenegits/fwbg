# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 14:29
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositorySnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snippet', models.TextField()),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
            ],
        ),
        migrations.CreateModel(
            name='UserLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
            ],
        ),
        migrations.CreateModel(
            name='UserMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserRepository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('language', models.CharField(max_length=124)),
                ('stars', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='has_signup',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username'),
        ),
        migrations.AddField(
            model_name='userrepository',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermatch',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_match_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermatch',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_match_user2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userlike',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like_from_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userlike',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like_to_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userdislike',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dislike_from_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userdislike',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dislike_to_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='repositorysnippet',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserRepository'),
        ),
    ]
