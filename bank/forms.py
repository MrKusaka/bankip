from django.forms import ModelForm
from django import forms

from .models import Credit


class CreditAddForm(ModelForm):
    """Форма для добавления фильма"""
    bank_name = forms.CharField(max_length=100,
                           label='Название банка',
                           widget=forms.TextInput
                           (attrs={'placeholder': 'не более 100 символов '})
                           )
    amount = forms.IntegerField(label='Сумма задолженности')
    credit_term = forms.IntegerField(label='Срок задолженности')
    debt_percent = forms.IntegerField(label='Процент задолженности')

    class Meta:
        model = Credit
        fields = [
            'bank_name',
            'amount',
            'credit_term',
            'debt_percent',
        ]

