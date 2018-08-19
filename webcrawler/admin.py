from django.contrib import admin, messages
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
    list_display = ('title', 'subject_year', 'subject_grade', 'subject_semester',
                    'major', 'subject_type', 'certification_type', 'culture_type', 
                    'subject_point', 'necessary',)
    list_editable = ('certification_type', 'subject_type', 'culture_type')
    list_filter = ('certification_type', 'subject_type', )
    search_fields = ('title', 'major__name',)
    actions = ['check_necessary', 'uncheck_necessary',
               'certification_type_select_1','certification_type_select_2',
               'certification_type_select_3','certification_type_select_4', 
               'certification_type_select_5',
               'subject_type_1','subject_type_2',
               'subject_type_3','subject_type_4',
               'subject_type_5','subject_type_6',
               'subject_type_7','subject_type_8',
               'subject_type_9','subject_type_10',
               'subject_type_11',]


    def check_necessary(self, request, queryset):
        queryset.update(necessary=True)
        messages.success(request, '필수과목으로 지정했습니다.')
    check_necessary.short_description = '필수과목 지정'

    def uncheck_necessary(self, request, queryset):
        queryset.update(necessary=False)
        messages.success(request, '필수과목을 해지했습니다.')
    uncheck_necessary.short_description = '필수과목 해지'

    def subject_type_1(self, request, queryset):
        queryset.update(subject_type="교필")
        messages.success(request, '교육필수(으)로 지정했습니다.')
    subject_type_1.short_description = "교필 지정"
    
    def subject_type_2(self, request, queryset):
        queryset.update(subject_type="계필")
        messages.success(request, '계열필수(으)로 지정했습니다.')
    subject_type_2.short_description = "계필 지정"
    
    def subject_type_3(self, request, queryset):
        queryset.update(subject_type="교선")
        messages.success(request, '교육선택(으)로 지정했습니다.')
    subject_type_3.short_description = "교선 지정"

    def subject_type_4(self, request, queryset):
        queryset.update(subject_type="기전")
        messages.success(request, '기본전공(으)로 지정했습니다.') 
    subject_type_4.short_description = "기전 지정"

    def subject_type_5(self, request, queryset):
        queryset.update(subject_type="선전")
        messages.success(request, '선택전공(으)로 지정했습니다.')
    subject_type_5.short_description = "선전 지정"

    def subject_type_6(self, request, queryset):
        queryset.update(subject_type="교선")
        messages.success(request, '교양선택(으)로 지정했습니다.')
    subject_type_6.short_description = "교선 지정"

    def subject_type_7(self, request, queryset):
        queryset.update(subject_type="응전")
        messages.success(request, '응용전공(으)로 지정했습니다.')
    subject_type_7.short_description = "응전 지정"

    def subject_type_8(self, request, queryset):
        queryset.update(subject_type="일선")
        messages.success(request, '일반선택(으)로 지정했습니다.')
    subject_type_8.short_description = "일선 지정"

    def subject_type_9(self, request, queryset):
        queryset.update(subject_type="전필")
        messages.success(request, '전공필수(으)로 지정했습니다.')
    subject_type_9.short_description = "전필 지정"

    def subject_type_10(self, request, queryset):
        queryset.update(subject_type="전선")
        messages.success(request, '전공선택(으)로 지정했습니다.')
    subject_type_10.short_description = "전선 지정"

    def subject_type_11(self, request, queryset):
        queryset.update(subject_type="교직")
        messages.success(request, '교직(으)로 지정했습니다.')
    subject_type_11.short_description = "교직 지정"


    def certification_type_select_1(self, request, queryset):
        queryset.update(certification_type="인필BSM")
        messages.success(request, '공학인증 필수 BSM(으)로 지정했습니다.')
    certification_type_select_1.short_description = '인필BSM 지정'

    def certification_type_select_2(self, request, queryset):
        queryset.update(certification_type="인필교")
        messages.success(request, '공학인증 필수 교양(으)로 지정했습니다.')
    certification_type_select_2.short_description = '인필교 지정'

    def certification_type_select_3(self, request, queryset):
        queryset.update(certification_type="인필전")
        messages.success(request, '공학인증 필수 전공(으)로 지정했습니다.')
    certification_type_select_3.short_description = '인필전 지정'

    def certification_type_select_4(self, request, queryset):
        queryset.update(certification_type="인선전")
        messages.success(request, '공학인증 선택 전공(으)로 지정했습니다.')
    certification_type_select_4.short_description = '인선전 지정'

    def certification_type_select_5(self, request, queryset):
        queryset.update(certification_type="인선교")
        messages.success(request, '공학인증 선택 교양(으)로 지정했습니다.')
    certification_type_select_5.short_description = '인선교 지정'
