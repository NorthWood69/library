from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.SelectDateWidget,label='Дата возврата', help_text='Введите дату в пределах 4 недель начиная с сегодняшнего дня (3 недели по умолчанию).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом). 
        if data < datetime.date.today():
            raise ValidationError(_('Дата возврата не может быть в прошлом'))
        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Дата возврата не может быть позднее 4 недель'))
        # Помните, что всегда надо возвращать "очищенные" данные.
        return data