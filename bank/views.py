from django.shortcuts import render
from django.views.generic import CreateView, View, DeleteView, UpdateView, TemplateView

from .forms import *
from .models import Credit


class CreditView(View):
    def get(self, request):
        credits = Credit.objects.all()
        return render(request, 'bank/index.html', {'credit_list': credits})


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
        # print(context)
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
