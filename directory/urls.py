from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='teacher_list'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('import-data/', views.ImportDataView.as_view(), name='import_data'),
]