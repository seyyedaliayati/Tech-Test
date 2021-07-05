from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .filters import TeacherFilterSet
from .models import Subject, Teacher
from .forms import ImportDataForm
from .utils import import_teachers


class TeacherListView(ListView):
    model = Teacher
    template_name = 'directory/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 10

    def get_queryset(self):
        qs = super(TeacherListView, self).get_queryset()
        return TeacherFilterSet(data=self.request.GET, queryset=qs).filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.all()
        return context


class ImportDataView(LoginRequiredMixin, FormView):
    template_name = 'directory/teacher_import.html'
    form_class = ImportDataForm

    def form_valid(self, form: ImportDataForm):
        import_teachers(**form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("teacher_list")


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'directory/teacher_detail.html'
