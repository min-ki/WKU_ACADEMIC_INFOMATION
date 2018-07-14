from django.contrib import messages
from django.shortcuts import render, redirect
from .intranet import parsed_subject

graduated_point = {
    '컴퓨터공학과': 136,
}

def index(request):
    
    if request.session.get('intranet_id', False):
        intranet_id = request.session['intranet_id']
    
    if request.session.get('intranet_pw', False):
        intranet_pw = request.session['intranet_pw']
        
    if intranet_id and intranet_pw:
        try:
            if not request.session.get('data', False):
                data = parsed_subject(intranet_id, intranet_pw)
                request.session['data'] = data
            else:
                data = request.session['data']


            if data:
                subject_list = data[0] # 과목 리스트
                total_point = data[1]['sum_of_grade_point']  # 전체 학점
                subject_point = get_sum_of_subject(data[0]) # 전공학점, 교양학점
                user_info = data[2]  # 사용자 정보    
                scholar_ship = data[3]       
            else:
                # 로그인 에러 출력
                messages.error(request, '로그인에 실패했습니다.')
                return redirect('accounts:login')
        except NameError:
            print("NameError 발생")

    context = {'subject_point': subject_point, 'subject_list': subject_list,
               'total_point': total_point,
               'user_info': user_info,
               'graduated_point': graduated_point,
               'scholar_ship': scholar_ship,}  # data를 분할해서 여러개의 context로 넘기기

    return render(request, 'webcrawler/index.html', context)


def completed_list(request):
    
    
    if request.session.get('data', False):
        completed_list = request.session['data'][0] # 이수과목 리스트
        completed_list_count = len(completed_list.keys()) # 이수과목 개수
        completed_list_point_count = int(sum([float(i[1]) for i in completed_list.values() ])) # 이수과목 학점 총점
    else:
        completed_list = None

    return render(request, 'webcrawler/completed_list.html', {'completed_list' : completed_list ,
                                                              'completed_list_count': completed_list_count,
                                                              'completed_list_point_count': completed_list_point_count})


## 전공과목 리스트 뷰
def major_list(request):
    
    if request.session.get('data', False):
        major_list = get_major_subject(request.session['data'][0])
    else:
        major_list = None

    return render(request, 'webcrawler/major_list.html', {'major_list' : major_list})

## 전공과목 반환해주는 함수
def get_major_subject(subject):
    
    major_subject = {}

    for title, item in subject.items():
        if item[0] == '기전' or item[0] == '선전':
            major_subject[title] =  item

    return major_subject


## 교양과목 리스트 뷰
def culture_list(request):

    if request.session.get('data', False):
        culture_list = get_culture_list(request.session['data'][0])
    else:
        culture_list = None

    return render(request, 'webcrawler/culture_list.html', {'culture_list': culture_list})

## 교양과목 반환해주는 함수
def get_culture_list(subject):

    culture_subject = {}

    for title, item in subject.items():
        if item[0] == '교필' or item[0] == '교선' or item[0] == '계필':
            culture_subject[title] =  item

    return culture_subject

## 전공과목 총 학점, 교양과목 총 학점 
def get_sum_of_subject(subject):
    
    sum = {}

    culture_subject_sum = 0
    major_subject_sum = 0

    for title, arr in subject.items():
        if arr[0] == "교필" or arr[0] == "교선" or arr[0] == "계필":
            culture_subject_sum = culture_subject_sum + float(arr[1])
        elif arr[0] == "기전" or arr[0] == "선전":
            major_subject_sum = major_subject_sum + float(arr[1])

    sum['major_subject_sum'] = int(major_subject_sum)
    sum['culture_subject_sum'] = int(culture_subject_sum)

    return sum
