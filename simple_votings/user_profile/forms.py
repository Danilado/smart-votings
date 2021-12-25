from django import forms

class DescForm(forms.Form):
    CHOICES = [('1', 'YES'), ('2', 'NO')] # тот кто теперь должен делать подсчет, в бд хранится номер варианта ответа yes - 1, no - 2
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)