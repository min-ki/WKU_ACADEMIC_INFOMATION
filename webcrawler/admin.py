from django.contrib import admin
from .models import Major, Subject


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['name', 'certification']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject_grade', 'major', 'subject_type', 'subject_point']
    search_fields = ['title', 'major__name']
