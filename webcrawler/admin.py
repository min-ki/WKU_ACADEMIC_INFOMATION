from django.contrib import admin
from .models import Major, Subject


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['title']