from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views
from .views import *


urlpatterns = [
    path('credits/', CreditView.as_view(), name='credit'),
    path('credits_add/', CreditAddView.as_view(), name='credit_add'),
    path('calculation', CreditCalculationView.as_view(), name='calculation'),
    path('credit_update/<pk>/', CreditUpdateView.as_view(), name='credit_update'),
    path('credit_delete/<pk>/', CreditDeleteView.as_view(), name='credits_delete'),
    path('message/', index, name='message'),
    # path('full_calculation', FullCalculationView.as_view(), name='full_calculation'),
    # path('credit_calculation/<pk>/', CreditCalculationView.as_view(), name='credit_calculation')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
