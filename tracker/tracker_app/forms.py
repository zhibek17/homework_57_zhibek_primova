from django import forms
from .models import Type, Status


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=True, label='Полное описание', widget=forms.Textarea())
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус', required=False,
                                    widget=forms.Select())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Тип', required=False,
                                          widget=forms.SelectMultiple())
