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
    debt_percent = forms.FloatField(label='Процент задолженности')

    class Meta:
        model = Credit
        fields = [
            'bank_name',
            'amount',
            'credit_term',
            'debt_percent',
        ]


class CreditCalculationForm(forms.Form):
    """Форма для расчёта кредита"""
    amount = forms.IntegerField(label='Сумма задолженности')
    credit_term = forms.IntegerField(label='Срок задолженности')
    debt_percent = forms.FloatField(label='Процент задолженности')

    def get_calculations_data(self):
        calculation_data = {}
        percentage_share_list = []
        all_payment = []
        all_remaining_debt = []
        if self.is_valid():
            amount = self.cleaned_data['amount']
            debt_percent = self.cleaned_data['debt_percent']
            credit_term = self.cleaned_data['credit_term']
            debt_percent = (debt_percent / 100) / 12
            a = debt_percent + (debt_percent / ((1 + debt_percent) ** credit_term - 1))
            monthly_payment = round((amount * a), 2)  # ежемесячный расчет
            total = monthly_payment * credit_term
            calculation_data['monthly_payment'] = monthly_payment
            calculation_data['total'] = total
            for _ in range(credit_term):
                percentage_share = round((amount * debt_percent), 2)  # доля процента
                percentage_share_list.append(percentage_share)  # список процентных долей
                # ежемесячный расчёт исключая процент
                calculations = round((monthly_payment - percentage_share), 2)
                all_payment.append(calculations)  # список платежа, который идёт за долг
                amount = round((amount - calculations), 2)
                all_remaining_debt.append(amount)  # остаток долга
                calculation_data['percentage_share_list'] = percentage_share_list
                calculation_data['all_payment'] = all_payment
                calculation_data['all_remaining_debt'] = all_remaining_debt
            return calculation_data
