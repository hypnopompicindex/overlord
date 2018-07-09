from django.views.generic import CreateView
from .forms import ProjectForm


class ProjectView(CreateView):
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
