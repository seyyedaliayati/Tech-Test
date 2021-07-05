from django.views.generic import ListView

from url_filter.filtersets import ModelFilterSet

from .models import Subject, Teacher


class TeacherFilterSet(ModelFilterSet):
    class Meta:
        model = Teacher
        fields = ["last_name", "subjects", ]
        

class TeacherListView(ListView):
    model = Teacher
    template_name = 'directory/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 3

    def get_queryset(self):
        qs = super(TeacherListView, self).get_queryset()
        return TeacherFilterSet(data=self.request.GET, queryset=qs).filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.all()
        return context
    
    
    
