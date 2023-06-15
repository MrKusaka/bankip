from django.shortcuts import render
from django.views.generic import CreateView, View

from .forms import *
from .models import Credit


class CreditView(View):
    def get(self, request):
        credits = Credit.objects.all()
        return render(request, 'bank/index.html', {'credit_list': credits})


class CreditCalculationView(View):
    def get(self, request):
        monthly_payment = ''
        error = ''
        all_payment = []
        all_remaining_debt = []
        percentage_share_list = []
        form = CreditAddForm()
        if request.method == 'GET':
            form = CreditAddForm(request.GET)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                debt_percent = form.cleaned_data['debt_percent']
                credit_term = form.cleaned_data['credit_term']
                debt_percent = (debt_percent / 100) / 12
                a = debt_percent + (debt_percent / ((1 + debt_percent) ** credit_term - 1))
                monthly_payment = round((amount * a), 2)  # ежемесячный расчет
                # Пока не реализована новая вьюха, все делаю в одной.
                for _ in range(credit_term):
                    percentage_share = round((amount * debt_percent), 2)  # доля процента
                    percentage_share_list.append(percentage_share)  # список процентных долей
                    # ежемесячный расчёт исключая процент
                    calculations = round((monthly_payment - percentage_share), 2)
                    all_payment.append(calculations)  # список платежа, который идёт за долг
                    amount = round((amount - calculations), 2)
                    all_remaining_debt.append(amount)  # остаток долга
            else:
                error = 'Wrong!'
        return render(request, 'bank/calculation.html', {
            'form': form,
            'monthly_payment': monthly_payment,
            'percentage_share_list': percentage_share_list,
            'all_payment': all_payment,
            'all_remaining_debt': all_remaining_debt,
            'error': error
        })

# Идея новой вью, наследуя класс CreditCalculationView, сделать отдельную страницу для полного расчёт по месяцам.
# class FullCalculationView(CreditCalculationView):
#     def loh(self, request):
#         c = super().get(request)
#
#
#         full_calculation = c.amount - c.calculations
#         print(full_calculation)
#         print(CreditCalculationView.calculations)
#         return render(request, 'bank/full_calculation.html', {
#             'full_calculation': full_calculation
#
#         })
#     def get(self, request, credit_term):
#         self.credit_term = credit_term
#         super.get()
#         for _ in range(len(credit_term)):
#             full_calculation = calculation - amount


class CreditAddView(CreateView):
    model = Credit
    template_name = 'bank/credit.html'
    form_class = CreditAddForm
