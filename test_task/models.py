from django.contrib.auth.models import User
from django.db import models


class Score(models.Model):
    account_number = models.CharField('Номер счета', max_length=16)
    balance = models.DecimalField('Баланс', max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    def __str__(self):
        return str(self.account_number)


class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    score_sender = models.ForeignKey(Score, on_delete=models.CASCADE)
    score_recipient = models.ForeignKey(Score, on_delete=models.CASCADE, related_name='set_recipient')
    amount = models.DecimalField('Сумма', max_digits=6, decimal_places=2)
    created_at = models.DateTimeField('Время транзакции', auto_now_add=True)

    class Meta:
        verbose_name = "История перевода"
        verbose_name_plural = "История переводов"



