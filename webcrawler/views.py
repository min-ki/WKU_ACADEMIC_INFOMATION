from django.core import serializers
from django.contrib import messages
from django.shortcuts import render, redirect
from .intranet import parser
from .models import Subject, Major
from collections import Counter

def index(request):
    
    if request.session.get('intranet_id', False) and request.session.get('intranet_pw', False):
        intranet_id = request.session['intranet_id']
        intranet_pw = request.session['intranet_pw']
    else:
        return redirect('accounts:login')
        
    if intranet_id and intranet_pw:
        try:
            if not request.session.get('data', False):
                data = parser(intranet_id, intranet_pw)
                request.session['data'] = data
            else:
                data = request.session['data']


            if data:
                subject_list = data[0] # 과목 리스트
                total_point = int(data[1]['sum_of_grade_point'])  # 전체 학점
                subject_point = get_sum_of_subject(data[0]) # 전공학점, 교양학점
                user_info = data[2]  # 사용자 정보    
                scholar_ship = data[3] # 장학정보
                wpoint = data[4] # WPOINT  
                detail_wpoint = data[5] # WPOINT Detail
                average_point_info = data[6]
                graduated_point = get_graduated_point(user_info[1], user_info[4], user_info[6]) # 졸업학점
                major_point, basic_major_point = get_major_point(user_info[1], user_info[4], user_info[6]) # 기본전공, 전체 전공학점
                culture_point = get_culture_point(user_info[1]) # 교양학점 
                remain_graduated_point = int(graduated_point - total_point) # 남은학점
                
                graduated_point_percentage = int(get_percentage(total_point, graduated_point))  # 졸업학점 퍼센티지
                major_point_percentage = int(get_percentage(subject_point['major_subject_sum'], major_point))  # 전공학점 퍼센티지
                culture_point_percentage = int(get_percentage(subject_point['culture_subject_sum'], culture_point)) # 교양학점 퍼센티지


                ### 복수전공, 교직이수 
                plural_major = check_plural_major(data[0])
                teach_major = check_teach_major(data[0])

                print(plural_major, teach_major)

                ### 세션 데이터 설정
                request.session['subject_list'] = subject_list
                request.session['total_point'] = total_point
                request.session['graduated_point'] = graduated_point # 졸업 학점
                request.session['basic_major_point'] = basic_major_point # 기본 전공 학점
                request.session['major_point'] = major_point # 전체 전공 학점
                request.session['culture_point'] = culture_point # 교양 학점
                request.session['subject_point'] = subject_point  # 과목 학점 정보
                request.session['user_info'] = user_info  # 유저정보
                request.session['scholar_ship'] =  scholar_ship # 장학금 정보
                request.session['detail_wpoint'] = detail_wpoint # WPOINT세부정보
                request.session['average_point_info'] = average_point_info # 평균 학점 정보
                request.session['remain_graduated_point'] = remain_graduated_point # 남은 졸업 학점
                request.session['graduated_point_percentage'] = graduated_point_percentage
                request.session['major_point_percentage'] = major_point_percentage
                request.session['culture_point_percentage'] = culture_point_percentage

            else:
                # 로그인 에러 출력
                messages.error(request, '로그인에 실패했습니다.')
                return redirect('accounts:login')
                
        except NameError:
            print("NameError 발생")

    context = {
        'subject_point': subject_point,
        'subject_list': subject_list,
        'total_point': total_point,
        'user_info': user_info,
        'graduated_point': graduated_point,
        'basic_major_point': basic_major_point,
        'major_point' : major_point,
        'culture_point' : culture_point,
        'scholar_ship': scholar_ship,
        'wpoint': wpoint,
        'detail_wpoint': detail_wpoint,
        'average_point_info': average_point_info,
        'remain_graduated_point': remain_graduated_point,
        'graduated_point_percentage': graduated_point_percentage,
        'major_point_percentage': major_point_percentage,
        'culture_point_percentage': culture_point_percentage,
        'plural_major' : plural_major,
        'teach_major' : teach_major, 
    }

    return render(request, 'webcrawler/index.html', context)

## 이수과목 리스트 뷰
def completed_list(request):
    
    if request.session.get('user_info', False):
        user_info = request.session['user_info']
    else:
        return redirect('accounts:login')

    try:
        certification_list = Subject.objects.filter(major__name__contains=user_info[6]) # 공학인증 리스트
        certification_list_title = [item.title for item in certification_list] # 공학인증 과목
        certification_list_info =  { item.title : item.certification_type for item in certification_list} # 공학인증 정보
        certification_list_necessary = { item.title : item.necessary for item in certification_list } # 필수과목 여부
        certification_major = Major.objects.get(name=user_info[6]).certification # 공학인증 학과 여부

    except Major.DoesNotExist:
        certification_major = False
    except UnboundLocalError:
        return redirect('accounts:login')

    if request.session.get('data', False):
        completed_list = request.session['data'][0] # 이수과목 리스트
        count_grade = get_count_grade_point(completed_list)
        completed_list_count = len(completed_list.keys()) # 이수과목 개수
        completed_list_point_count = int(sum([float(i[2]) for i in completed_list.values() ])) # 이수과목 학점 총점
    else:
        completed_list = None

    context = {
        'completed_list' : completed_list ,
        'completed_list_count': completed_list_count,
        'completed_list_point_count': completed_list_point_count,
        'certification_list_title': certification_list_title,
        'certification_list_info': certification_list_info,
        'certification_list_necessary': certification_list_necessary,
        'certification_major': certification_major,
        'count_grade': count_grade
    }

    return render(request, 'webcrawler/completed_list.html', context)


## 전공과목 리스트 뷰
def major_list(request):
    
    if request.session.get('user_info', False):
        user_info = request.session['user_info']
    else:
        return redirect('accounts:login')

    try:
        certification_list = Subject.objects.filter(major__name__contains=user_info[6]) # 공학인증 리스트
        certification_list_title = [item.title for item in certification_list] # 공학인증 과목
        certification_list_info =  { item.title : item.certification_type for item in certification_list} # 공학인증 정보
        certification_list_necessary = { item.title : item.necessary for item in certification_list } # 필수과목 여부
        certification_major = Major.objects.get(name=user_info[6]).certification # 공학인증 학과 여부
    except Major.DoesNotExist:
        certification_major = False
    except UnboundLocalError:
        return redirect('accounts:login')

    if request.session.get('data', False):
        major_list = get_major_subject(request.session['data'][0])
        count_grade = get_count_grade_point(major_list)
        count_type = get_count_type(major_list)
        major_list_count = len(major_list.keys()) # 전공과목 개수
        major_list_point_count = int(sum([float(i[2]) for i in major_list.values() ])) # 전공과목 학점 총점
    else:
        major_list = None

    context = {
        'major_list' : major_list ,
        'major_list_count': major_list_count,
        'major_list_point_count': major_list_point_count,
        'certification_list_title': certification_list_title,
        'certification_list_info': certification_list_info,
        'certification_list_necessary': certification_list_necessary,
        'certification_major': certification_major,
        'count_grade': count_grade,
        'count_type': count_type
    }

    return render(request, 'webcrawler/major_list.html', context)

## 전공과목 반환해주는 함수
def get_major_subject(subject):
    
    major_subject = {}

    for title, item in subject.items():
        if item[0] == '기전' or item[0] == '선전' or item[0] == '전선' or item[0] == '응전' or item[0] == '복수' or item[0] == '교직':
            major_subject[title] =  item

    return major_subject

## 교양과목 리스트 뷰
def culture_list(request):

    if request.session.get('user_info', False):
        user_info = request.session['user_info']
    else:
        return redirect('accounts:login')
    
    try:
        certification_list = Subject.objects.filter(major__name__contains=user_info[6]) # 공학인증 리스트
        certification_list_title = [item.title for item in certification_list] # 공학인증 과목
        certification_list_info =  { item.title : item.certification_type for item in certification_list} # 공학인증 정보
        certification_list_necessary = { item.title : item.necessary for item in certification_list } # 필수과목 여부
        certification_major = Major.objects.get(name=user_info[6]).certification # 공학인증 학과 여부
    except Major.DoesNotExist:
        certification_major = False
    except UnboundLocalError:
        return redirect('accounts:login')

    if request.session.get('data', False):
        culture_list = get_culture_subject(request.session['data'][0])
        count_grade = get_count_grade_point(culture_list)
        count_type = get_count_type(culture_list)
        culture_list_count = len(culture_list.keys()) # 전공과목 개수
        culture_list_point_count = int(sum([float(i[2]) for i in culture_list.values() ])) # 전공과목 학점 총점
    else:
        culture_list = None

    context = {
        'culture_list': culture_list,
        'culture_list_count': culture_list_count,
        'culture_list_point_count': culture_list_point_count,
        'certification_list_title': certification_list_title,
        'certification_list_info': certification_list_info,
        'certification_list_necessary': certification_list_necessary,
        'certification_major': certification_major,
        'count_grade': count_grade,
        'count_type': count_type
    }

    return render(request, 'webcrawler/culture_list.html', context)

## 교양과목 반환해주는 함수
def get_culture_subject(subject):

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
    basic_major_subject_sum = 0

    for title, arr in subject.items():
        if arr[0] == "기전": # 기전 카운트
            basic_major_subject_sum += float(arr[2])

        if arr[0] == "교필" or arr[0] == "교선" or arr[0] == "계필" or arr[0] == "일선":
            culture_subject_sum = culture_subject_sum + float(arr[2])
        elif arr[0] == "기전" or arr[0] == "전선" or arr[0] == "선전" or arr[0] == "복수" or arr[0] == "응전" or arr[0] == '교직':
            major_subject_sum = major_subject_sum + float(arr[2])
    sum['basic_major_subject_sum'] = int(basic_major_subject_sum)
    sum['major_subject_sum'] = int(major_subject_sum)
    sum['culture_subject_sum'] = int(culture_subject_sum)

    return sum



## W - POINT 상세페이지
def wpoint_detail(request):
    
    if request.session.get('detail_wpoint', False):
        detail_wpoint = request.session['detail_wpoint']
    else:
        detail_wpoint = None

    return render(request, 'webcrawler/wpoint_detail.html', {'detail_wpoint': detail_wpoint})


def chart(request):

    if request.session.get('average_point_info', False):
        average_point_info = request.session['average_point_info']

    return render(request, 'webcrawler/grade_graph.html', {'average_point_info': average_point_info})
    
## 백분위
def get_percentage(point, grade_point):

    percentage = (point / grade_point) * 100
    return percentage

## 타입 카운팅
def get_count_type(subject):

    type_count = Counter()

    for title, item in subject.items():
        if item[0] in ['기전', '응전', '선전', '전선', '복수', '교필', '교선', '계필', '일선', '교직']:
            type_count[item[0]] += 1

    return type_count

## 점수 카운팅
def get_count_grade_point(subject):

    grade_point = Counter()

    for title, item in subject.items():
        if item[3] in ['A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'P']:
            grade_point[item[3]] += 1

    return grade_point

# 학번 user_info[1] , 단과대학명 user_info[4], 학과 user_info[6]
def get_graduated_point(user_number, user_colleage, user_major):
    
    graduated_point = 0

    user_number = int(''.join(list(user_number[2:4])))
    print(user_number)

    # 13학번부터 136학점 창의공과대학
    if user_number > 12 and user_colleage == "창의공과대학":
        graduated_point = 136

    elif user_number > 12 and (user_colleage == "교학대학" or user_colleage == "인문대학" or user_colleage == "경영대학" or user_colleage == "농식품융합대학"
                             or user_colleage == "자연과학대학" or user_colleage == "생활과학대학" or user_colleage == "사회과학대학"):
        graduated_point = 130
    elif user_number > 12 and user_major == "봉황인재학과":
        graduated_point = 120
    elif user_number > 5 and (user_colleage == "조형예술디자인대학" or user_colleage == "미술대학"):
        graduated_point = 130
    elif user_colleage == "의과대학" or user_colleage == "한의과대학" or user_colleage == "치과대학":
        graduated_point = 160
    elif user_major == "간호학과" or user_colleage == "사범대학" or user_major == '작업치료학과':
        graduated_point = 140
    else:
        graduated_point = 140

    return graduated_point

def get_culture_point(user_number):

    user_number = int(''.join(list(user_number[2:4])))
    culture_point = 0

    if user_number >= 10:
        culture_point = 60
    elif 5 <= user_number <= 9:
        culture_point = 70
    elif 2 <= user_number <= 4:
        culture_point = 80
    else:
        culture_point = 100000

    return culture_point


def get_major_point(user_number, user_colleage, user_major):
    
    user_number = int(''.join(list(user_number[2:4])))

    basic_major_point = 0
    major_point = 0
    special_point = 0

    # 교학대학
    if user_colleage == "교학대학":
        basic_major_point = 18
        major_point = 69
    # 인문대학
    elif user_major == "국어국문학과" or user_major == "문예창작학과" or user_major == "영어영문학과" or user_major == "중국학과" or user_major == "역사문화학부" or user_major == "철학과" or user_major == "음악과":
        basic_major_point = 15
        major_point = 66
    # 사범대학
    elif user_major == "국어교육과" or user_major == "영어교육과" or user_major == "일어교육과" or user_major == "한문교육과" or user_major == "역사교육과" or user_major == "교육학과" or user_major == "유아교육과":
        basic_major_point = 15
        major_point = 69
    elif user_major == "가정교육과" or user_major == "수학교육과" or user_major == "체육교육과":
        basic_major_point = 19
        major_point = 69
    elif user_major == "중등특수교육과":
        basic_major_point = 15
        major_point = 80
        special_point = 42 - basic_major_point
    # 조형예술디자인 대학
    elif user_major == "미술과" or  user_major == "귀금속보석공예과" or user_major == "디자인학부":
        basic_major_point = 19
        major_point = 66
    elif user_major == "패션디자인산업학과":
        basic_major_point = 19
        major_point = 69
    # 사회과학대학
    elif user_major == "행정언론학부" or user_major ==  "복지·보건학부" or user_major ==  "군사학과" or user_major == "경찰행정학과" or user_major == "소방행정학과":
        basic_major_point = 15
        major_point = 66
    elif user_major == "가동아정복지학과":
        basic_major_point = 19
        major_point = 69
    # 자연과학대학
    elif user_major == "응용수학부" or  user_major == "빅데이터·금융통계학부" or user_major == "바이오나노화학부" or user_major == "반도체·디스플레이학부" or user_major == "생명과학부" or user_major == "뷰티디자인학부":
        basic_major_point = 19
        major_point = 69
    elif user_major == "스포츠과학부":
        basic_major_point = 19
        major_point = 66
    elif user_colleage == "농식품융합대학":
        basic_major_point = 19
        major_point = 69
    # 창의공과대학
    elif user_colleage == "창의공과대학" and user_major != "건축학과":
        basic_major_point = 19
        major_point = 72
    elif user_major == "건축학과":
        basic_major_point = 0
        major_point = 0
    # 경영대학
    elif user_major == "국제통상학부":
        basic_major_point = 15
        major_point = 66
    elif user_major == "경제학부":
        basic_major_point = 24
        major_point = 66
    elif user_major == "경영학부":
        basic_major_point = 30
        major_point = 66
    # 의과대학, 한의과대학, 치과대학, 한약학과
    elif user_colleage == "의과대학" or user_colleage == "한의과대학" or user_colleage == "치과대학" or user_major == "한약학과":
        basic_major_point = 0
        major_point = 0
    # 약학과
    elif user_major == "약학과":
        basic_major_point = 0
        major_point = 160
    
    return major_point, basic_major_point



### 복수전공 체크
def check_plural_major(subject):

    '''
        복수전공을 한다면은 복수유형의 과목이 존재
    '''
    for item in subject.values():
        if item[0] == "복수":
            return True
    return False

### 교직이수 체크
def check_teach_major(subject):
    
    '''
        타입중 교직이 존재하면 교직 이수
    '''
    for item in subject.values():
        if item[0] == "교직":
            return True
    return False        
