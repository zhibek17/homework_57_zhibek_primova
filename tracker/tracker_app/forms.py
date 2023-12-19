from django import forms
from .models import Type, Status, Task
from django.core.exceptions import ValidationError


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=True, label='Полное описание', widget=forms.Textarea())
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус', required=False,
                                    widget=forms.Select())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Тип', required=False,
                                          widget=forms.SelectMultiple())

    class Meta:
        model = Task
        fields = ['name', 'due_date', 'description']


def validate_curse_block(value):
    curse_words = ['fool', 'bad', 'dumpkoff']

    for word in curse_words:
        if word in value:
            raise ValidationError('Не используйте плохие слова!!!')

