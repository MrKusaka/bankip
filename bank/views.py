from django.shortcuts import render
from django.views.generic import CreateView, View, DeleteView, UpdateView, ListView, TemplateView

from .forms import *
from .models import Credit

class CreditView(View):
    def get(self, request):
        credits = Credit.objects.all()
        return render(request, 'bank/index.html', {'credit_list': credits})


# class CreditCalculationView(View):
#     def get(self, request):
#         monthly_payment = ''
#         error = ''
#         total = ''
#         all_payment = []
#         all_remaining_debt = []
#         percentage_share_list = []
#         form = CreditAddForm(request.GET)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             debt_percent = form.cleaned_data['debt_percent']
#             credit_term = form.cleaned_data['credit_term']
#             debt_percent = (debt_percent / 100) / 12
#             a = debt_percent + (debt_percent / ((1 + debt_percent) ** credit_term - 1))
#             monthly_payment = round((amount * a), 2)  # ежемесячный расчет
#             total = monthly_payment * credit_term
#             # Пока не реализована новая вьюха, все делаю в одной.
#             for _ in range(credit_term):
#                 percentage_share = round((amount * debt_percent), 2)  # доля процента
#                 percentage_share_list.append(percentage_share)  # список процентных долей
#                 # ежемесячный расчёт исключая процент
#                 calculations = round((monthly_payment - percentage_share), 2)
#                 all_payment.append(calculations)  # список платежа, который идёт за долг
#                 amount = round((amount - calculations), 2)
#                 all_remaining_debt.append(amount)  # остаток долга
#         else:
#             error = 'Wrong!'
#         return render(request, 'bank/calculation.html', {
#             'form': form,
#             'monthly_payment': monthly_payment,
#             'percentage_share_list': percentage_share_list,
#             'all_payment': all_payment,
#             'all_remaining_debt': all_remaining_debt,
#             'total': total,
#             'error': error
#         })
#
class CreditCalculationView(TemplateView):
    template_name = 'bank/calculation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calculation_form'] = CreditCalculationForm()
        return context

    def post(self, request):
        context = self.get_context_data()
        cal_form = CreditCalculationForm(request.POST)
        if cal_form.is_valid():
            context['calculation_data'] = cal_form.get_calculations_data()
        context['calculation_form'] = cal_form
        print(context)
        # print(calculation_data)
        # return self.render_to_response(context)
        return render(request, 'bank/calculation.html', context)


class CreditAddView(CreateView):
    model = Credit
    template_name = 'bank/credit.html'
    form_class = CreditAddForm


class CreditUpdateView(UpdateView):
    template_name = 'bank/credit.html'
    form_class = CreditAddForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Credit.objects.get(pk=id)


class CreditDeleteView(DeleteView):
    context_object_name = 'credit'
    template_name = 'bank/delete_credit.html'
    queryset = Credit.objects.all()
    success_url = '/bank/message/'


def index(request):
    return render(request, 'bank/message.html')
