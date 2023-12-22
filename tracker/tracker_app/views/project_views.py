from django.urls import reverse_lazy

from tracker_app.models import Task, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tracker_app.forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:
            return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_view.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(project=self.object)
        context['tasks'] = tasks
        return context

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_add.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_update.html'
    success_url = reverse_lazy('project')

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project')
    template_name = 'projects/project_delete.html'