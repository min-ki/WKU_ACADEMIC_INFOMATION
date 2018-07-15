from django.db import models

class Major(models.Model):
    name = models.CharField(max_length=25) # 전공 명
    certification = models.BooleanField(default=False) # 공학인증 여부


class Subject(models.Model):
    

    SUBJECT_TYPE_CHOICES = (
        ("교필", "교양필수"),
        ("교선", "교양선택"),
        ("기전", "기본전공"),
        ("선전", "선택전공"),
        ("응전", "응용전공"),
        ("계필", "계열필수"),
    )

    title = models.CharField(max_length=25) # 제목
    major = models.ForeignKey(Major, on_delete=models.CASCADE) # 학과
    type =  models.CharField(max_length=25, choices=SUBJECT_TYPE_CHOICES) # 수업유형

