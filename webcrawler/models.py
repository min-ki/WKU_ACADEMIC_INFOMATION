from django.db import models

class Major(models.Model):
    name = models.CharField(max_length=25) # 전공 명
    certification = models.BooleanField(default=False) # 공학인증 여부

    def __str__(self):
        return self.name

class Subject(models.Model):
    
    SUBJECT_TYPE_CHOICES = (
        ("교필", "교양필수"),
        ("교선", "교양선택"),
        ("기전", "기본전공"),
        ("선전", "선택전공"),
        ("응전", "응용전공"),
        ("계필", "계열필수"),
    )

    CERTIFICATION_TYPE_CHOICES = (
        ('인필교', '인필교'),
        ('인선교', '인선교'),
        ('인선전', '인선전'),
        ('인필전', '인선전'),
        ('인필BSM', '인필BSM'),
    )

    title = models.CharField(max_length=25) # 제목
    major = models.ForeignKey(Major, on_delete=models.CASCADE) # 학과
    subject_type =  models.CharField(max_length=25, choices=SUBJECT_TYPE_CHOICES) # 수업유형
    certification_type = models.CharField(max_length=25, choices=CERTIFICATION_TYPE_CHOICES) # 공학인증 유형
    subject_number = models.IntegerField() # 학수번호
    point = models.IntegerField() # 학점
    necessary = models.BooleanField(default=False) # 필수과목 여부

    def __str__(self):
        return self.title
