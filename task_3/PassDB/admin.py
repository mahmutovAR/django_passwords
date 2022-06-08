from django.contrib import admin
from .models import Card, Login, Note, AddPass


@admin.register(AddPass)
class AddPassAdmin(admin.ModelAdmin):
    list_display = ('db_label', 'db_date',  'db_path')
    fields = ['db_label', ('db_date',  'db_path')]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'card_number', 'card_validity',  'card_holder', 'card_cvv', 'card_pin', 'card_note')
    fields = ['card_name', ('card_number', 'card_validity',  'card_holder'), ('card_cvv', 'card_pin'), 'card_note']


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_url', 'account_login', 'account_password', 'account_note')
    fields = ['account_name', ('account_url', 'account_login', 'account_password'), 'account_note']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('note_label', 'note_text')
