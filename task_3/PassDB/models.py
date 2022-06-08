from django.db import models
from django.urls import reverse
import datetime


class Card(models.Model):
    """
    'cards': [{'cardNumber': '<data>',
            'custName': '<data>',
            'cvv': '<data>',
            'expirationDate': {'day': <data>, 'month': <data>, 'year': <data>},
            'holderName': '<data>',
            'note': '<data>',
            'pin': '<data>'}, ..]
    """
    card_name = models.CharField(max_length=50,
                                 help_text='Enter card name',
                                 verbose_name='My Card name')
    card_number = models.SlugField(max_length=16,
                                   help_text='Enter card name',
                                   verbose_name='Card number')
    card_validity = models.CharField(max_length=5,
                                     help_text='Enter card name',
                                     verbose_name='Valid thru',
                                     null=False, blank=False)
    card_holder = models.CharField(max_length=50,
                                   help_text="Enter cardholder's name",
                                   verbose_name='Cardholder')
    card_cvv = models.SlugField(max_length=3,
                                help_text='Enter CVV',
                                verbose_name='CVV')
    card_pin = models.SlugField(max_length=4,
                                help_text='Enter PIN code',
                                verbose_name='PIN code')
    card_note = models.CharField(max_length=200,
                                 help_text='Enter note about card',
                                 verbose_name='Note',
                                 null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.card_name

    def get_absolute_url(self):
        return reverse('cards_detail', args=[str(self.id)])


class Login(models.Model):
    """
    'logins': [{'color': 0,
             'custName': '<data>',
             'loginName': '<data>',
             'note': '<data>',
             'pwd': '<data>',
             'url': '<data>'}, ..]
    """
    account_name = models.CharField(max_length=50,
                                    help_text='Enter account name',
                                    verbose_name='My account')
    account_url = models.URLField(max_length=150,
                                  help_text='Enter URL',
                                  verbose_name='URL')
    account_login = models.CharField(max_length=50,
                                     help_text='Enter log name',
                                     verbose_name='Log name')
    account_password = models.CharField(max_length=50,
                                        help_text='Enter password',
                                        verbose_name='Password')
    account_note = models.CharField(max_length=200,
                                    help_text='Enter note about card',
                                    verbose_name='Note', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.account_name

    def get_absolute_url(self):
        return reverse('logins_detail', args=[str(self.id)])


class Note(models.Model):
    """
    'notes': [{'color': 0,
            'label': '<data>',
            'text': '<data>'}, ..]
    """
    note_label = models.CharField(max_length=50,
                                  help_text="Enter note's label",
                                  verbose_name='My note')
    note_text = models.CharField(max_length=300,
                                 help_text="Enter note's text",
                                 verbose_name='Note', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.note_label

    def get_absolute_url(self):
        return reverse('notes_detail', args=[str(self.id)])


class AddPass(models.Model):
    """Copies json file with passwords into folder "../uploads/password_files/" and adds info to the database."""
    db_label = models.CharField(max_length=20,
                                verbose_name='Enter datafile label')
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    db_date = models.DateField(default=current_date, verbose_name='Enter date in format YYYY-MM-DD')
    db_path = models.FileField(upload_to='password_files', verbose_name='".json" file', null=False, blank=False)
    objects = models.Manager()
    # DoesNotExist = models.Manager

    def __str__(self):
        return self.db_label

    def get_absolute_url(self):
        return reverse('pass_db_detail', args=[str(self.id)])
