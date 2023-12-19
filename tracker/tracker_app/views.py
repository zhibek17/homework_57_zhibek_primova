from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from datetime import timedelta


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'index.html', {'tasks': tasks})


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs.get('pk'))
        return context


class TaskAdd(TemplateView):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'task_add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)

        if form.is_valid():
            type = form.cleaned_data.pop('type')
            status = form.cleaned_data.pop('status')
            task = Task.objects.create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
            )
            task.type.set([type])
            task.status.set([status])
            return redirect('index', pk=task.pk)
        else:
            return render(request, 'task_add.html', {'form': form})


class TaskUpdate(TemplateView):
    template_name = 'task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(initial={
            'summary': task.summary,
            'description': task.description,
            'status': task.type.all(),
            'type': task.type.all()
        })
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            type = form.cleaned_data.pop('type')
            status = form.cleaned_data.pop('status')
            task.summary = form.cleaned_data.get('summary')
            task.description = form.cleaned_data.get('description')
            task.type.set([type])
            task.status.set([status])
            task.save()
            return redirect('index', pk=task.pk)
        else:
            return render(request, 'task_update.html', {'form': form})


class TaskDelete(TemplateView):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        return render(request, 'task_delete.html', {'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect('index')


