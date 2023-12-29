from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from tracker_app.models import Task, Type, Status
from tracker_app.forms import TaskForm


class IndexView(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    paginate_by = 6
    paginate_orphans = 3
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                summary__icontains=search_query
            )
        return queryset


class TaskView(DetailView):
    model = Task
    template_name = 'tasks:task_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskAdd(FormView):
    template_name = 'tasks/task_add.html'
    form_class = TaskForm
    def form_valid(self, form):
        task = form.save()
        return redirect('tasks:index', pk=task.pk)


class TaskUpdate(View):
    template_name = 'tasks/task_update.html'
    form_class = TaskForm

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = self.form_class(instance=task)
        return render(request, self.template_name, {'form': form, 'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_view', pk=pk)
        return render(request, self.template_name, {'form': form, 'task': task})


class TaskDelete(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_delete.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('tasks:index')
