from django.contrib import admin

from .models import Teacher, Subject

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_filter = ['subjects', 'last_name']

admin.site.register(Subject)
