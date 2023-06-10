from django.db import models


class Credit(models.Model):
    """Кредит"""
    bank_name = models.CharField('Название банка', max_length=100)
    amount = models.IntegerField('Сумма задолженности')
    credit_term = models.IntegerField('Срок задолженности')
    debt_percent = models.IntegerField('Процент задолженности')

    def __str__(self):
        return self.bank_name

    def get_absolute_url(self):  # redirect после добавления банка
        return f'/bank/credits'
