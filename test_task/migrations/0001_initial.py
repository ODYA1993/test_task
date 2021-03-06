# Generated by Django 4.0.3 on 2022-03-30 11:04

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
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.IntegerField(verbose_name='Номер счета')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Баланс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
        migrations.CreateModel(
            name='TranslationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Сумма')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время транзакции')),
                ('account_number_recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_recipient', to='test_task.score')),
                ('account_number_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_sender', to='test_task.score')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'История перевода',
                'verbose_name_plural': 'История переводов',
            },
        ),
    ]
