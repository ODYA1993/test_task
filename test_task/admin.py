from django.contrib import admin
from .models import Score, TranslationHistory


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_number', 'user_id', 'user', 'balance']
    list_editable = ['balance']


@admin.register(TranslationHistory)
class TranslationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'score_sender', 'score_recipient', 'amount', 'created_at']