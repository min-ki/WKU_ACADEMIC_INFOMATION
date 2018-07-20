from django.contrib import admin
from .models import Major, Subject


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'certification',)
    search_fields = ('name',)
    actions = ['make_certification', 'delete_certification']

    def make_certification(self, request, queryset):
        queryset.update(certification=True)
    make_certification.short_description = '공학인증학과 등록'

    def delete_certification(self, request, queryset):
        queryset.update(certification=False)
    delete_certification.short_description = '공학인증학과 해지'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_grade', 'subject_semester', 'major', 'subject_type', 'certification_type', 'subject_point',)
    search_fields = ('title', 'major__name',)
    actions = ['check_necessary', 'uncheck_necessary',
               'certification_type_select', 'subject_type_1']

    def check_necessary(self, request, queryset):
        queryset.update(necessary=True)
    check_necessary.short_description = '필수과목 지정'

    def uncheck_necessary(self, request, queryset):
        queryset.update(necessary=True)
    uncheck_necessary.short_description = '필수과목 해지'

    def subject_type_1(self, request, queryset):
        queryset.update(subject_type="교필")
    subject_type_1.short_description = "교필로 지정"

    def certification_type_select(self, request, queryset):
        queryset.update(certification_type="인필BSM")
    certification_type_select.short_description = '인필BSM 지정'
