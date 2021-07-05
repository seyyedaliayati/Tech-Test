import zipfile
import csv
import os

from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.urls import reverse


from url_filter.filtersets import ModelFilterSet

from .models import Subject, Teacher
from .forms import ImportDataForm


class TeacherFilterSet(ModelFilterSet):
    class Meta:
        model = Teacher
        fields = ["last_name", "subjects", ]


def save_file(in_memory, name):
    path = f'./media/temp/{name}'
    with open(path, 'wb+') as destination:
        for chunk in in_memory.chunks():
            destination.write(chunk)
    return path


def import_teachers(*args, **kwargs):
    # Save files on disk
    data_csv_file = kwargs.get('data_csv_file')
    images_zip_file = kwargs.get('images_zip_file')
    csv_path = save_file(data_csv_file, 'data.csv')
    zip_path = save_file(images_zip_file, 'images.zip')

    # Exctract Zip File
    temp_path = './media/temp/images/'
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_path)
    
    
    # Read CSV File
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            try:
                if row[0] == '':
                    continue
                # Extract Profile Image
                image_path = os.path.join(temp_path, row[2].lower())
                if not os.path.exists(image_path):
                    image_path = os.path.join('./static/', 'placeholder.png')
                # Create Teacher Object
                teacher = Teacher.objects.create(
                    first_name=row[0],
                    last_name=row[1],
                    email_address=row[3],
                    phone_number=row[4],
                    room_number=row[5],
                )
                # Save Image
                if image_path:
                    print("Image Path", image_path)
                    teacher.profile_picture.save(
                        os.path.basename(image_path),
                        File(open(image_path, 'rb'))
                    )       
                # Extract Subjects
                subject_names = row[6].split(",") 
                subject_names = map(str.lower, subject_names) # Normalize them
                subject_names = map(str.strip, subject_names) # Normalize them
                subject_names = list(set(subject_names)) # Remove Duplicates
                for subject_name in subject_names:
                    subject, _ = Subject.objects.get_or_create(title=subject_name)
                    print(subject, _)
                    teacher.subjects.add(subject)
                teacher.save()

            except Exception as e:
                print(e)



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
