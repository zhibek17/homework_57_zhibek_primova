from django import forms
from .models import Type, Status, Task
from django.core.exceptions import ValidationError


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']

    summary = forms.CharField(max_length=50, required=True, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=True, label='Полное описание', widget=forms.Textarea())
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус', required=False,
                                    widget=forms.Select())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Тип', required=False,
                                          widget=forms.SelectMultiple())

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        curse_words = ['fool', 'bad', 'dumpkoff']

        for word in curse_words:
            if word in summary.lower():
                raise ValidationError('Не используйте плохие слова!!!')

        return summary
