from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectMembership
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if not any([first_name, last_name]):
            raise forms.ValidationError('Необходимо заполнить хотя бы одно из полей: имя или фамилию.')

        if not email:
            raise forms.ValidationError('Поле email обязательно для заполнения.')

        return cleaned_data



def add_user(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        ProjectMembership.objects.get_or_create(user=user, project=project)
        return redirect('project-detail', project_id=project_id)
    users = User.objects.exclude(projects=project)
    return render(request, 'add_user.html', {'project': project, 'users': users})

def remove_user(request, project_id, user_id):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(User, pk=user_id)
    membership = get_object_or_404(ProjectMembership, user=user, project=project)
    if request.method == 'POST':
        membership.delete()
        return redirect('project-detail', project_id=project_id)
    return render(request, 'remove_user.html', {'project': project, 'user': user})
