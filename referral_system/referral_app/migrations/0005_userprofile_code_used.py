# Generated by Django 5.0.4 on 2024-05-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_app', '0004_userprofile_token_jwt'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code_used',
            field=models.CharField(default=1),
            preserve_default=False,
        ),
    ]