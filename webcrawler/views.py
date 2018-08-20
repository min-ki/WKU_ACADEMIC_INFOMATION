from django.contrib import messages
from django.shortcuts import render, redirect
from .intranet import parser
from .models import Subject, Major, Notice
from .utils import subject_fn 

def index(request):
    
    """
        * Dashboard 페이지

        * 기능
            - 사용자 정보 (이름, 학년, 학번, 이수학기, 소속, 학과)
            - 학점 현황
            - 성적 현황
            - 장학금 현황
            - WPOINT

        * intranet.parser 를 통해서 데이터 크롤링
            data[0] : 교과목 정보
            data[1] : 전체 이수 학점
            data[2] : 사용자 정보
            data[3] : 장학 정보
            data[4] : WPOINT
            data[5] : WPOINT 상세 정보
            data[6] : 평균 학점 정보
    """



    if request.session.get('data', False):
        data = request.session['data']
    else:
        data = parser(request.session['intranet_id'], request.session['intranet_pw'])

    if data:
        subject_list = data[0] # 과목 리스트
        subject_point = subject_fn.get_sum_of_subject(data[0]) # 전공학점, 교양학점
        total_point = int(data[1]['sum_of_grade_point'])  # 전체 학점
        user_info = data[2]  # 사용자 정보    
        scholar_ship = data[3] # 장학정보
        average_point_info = data[4]
        average_point_total = data[5]
        graduated_point = subject_fn.get_graduated_point(user_info[1], user_info[4], user_info[6]) # 졸업학점
        major_point, basic_major_point = subject_fn.get_major_point(user_info[1], user_info[4], user_info[6]) # 기본전공, 전체 전공학점
        culture_point = subject_fn.get_culture_point(user_info[1]) # 교양학점 
        remain_graduated_point = int(graduated_point - total_point) # 남은학점
        
        graduated_point_percentage = int(subject_fn.get_percentage(total_point, graduated_point))  # 졸업학점 퍼센티지
        major_point_percentage = int(subject_fn.get_percentage(subject_point['major_subject_sum'], major_point))  # 전공학점 퍼센티지
        culture_point_percentage = int(subject_fn.get_percentage(subject_point['culture_subject_sum'], culture_point)) # 교양학점 퍼센티지

        ### 타입별 기전, 선전, 응전, 복전, 교직 카운팅
        count_type = subject_fn.get_count_type(data[0])

        ### 자유 선택 영역 학점
        free_choice_subject_point = subject_fn.get_free_choice_subject_point(data[0])
        
        ### 복수전공, 교직이수 
        plural_major = subject_fn.check_plural_major(data[0]) 
        teach_major = subject_fn.check_teach_major(data[0])


        ### 자기계발심층상담 횟수
        consult_count = subject_fn.count_culsult(data[0])

        point = {} # 학점 정보를 담을 사전
        point['total_point'] = total_point
        point['graduated_point'] = graduated_point
        point['culture_point'] = culture_point
        point['graduated_point_percentage'] = graduated_point_percentage
        point['culture_point_percentage'] = culture_point_percentage
        point['remain_graduated_point'] = remain_graduated_point
        point['average_point_total'] = average_point_total
        point['subject_point'] = subject_point
        point['basic_major_point'] = basic_major_point # 기본 전공 학점
        point['major_point'] = major_point # 들은 전공 학점
        point['major_point_percentage'] = major_point_percentage # 들은 전공 / 전체 전공
        point['count_type'] = count_type # 타입 카운트
        point['graduated_language_point'], point['language_average_point'], point['language_subject_count'] = subject_fn.get_language_necessary_point(data[0]) # 언어 영역
        point['graduated_english_point'], point['english_average_point'], point['english_subject_count'] = subject_fn.get_english_necessary_point(data[0]) # 영어 영역
        point['graduated_sw_point'], point['sw_average_point'], point['sw_subject_count'] = subject_fn.get_sw_necessary_point(data[0]) # 소프트웨어 영역
        point['graduated_culture_choice_point'], point['culture_average_point'], point['culture_subject_count'] = subject_fn.get_culture_choice_point(data[0])  # 인문소양 영역
        point['graduated_founded_subject_point'], point['founded_average_point'], point['founded_subject_count'] = subject_fn.get_founded_subject_necessary_point(data[0]) # 창업 영역
        point['graduated_creative_point'], point['creative_average_point'], point['creative_subject_count'] = subject_fn.get_creative_necessary_point(data[0]) # 창의 영역
        point['free_choice_subject_point'], point['free_choice_average_point'], point['free_choice_subject_count'] = free_choice_subject_point # 자유선택 영역
        point['type_average_point'] = subject_fn.get_count_grade_average_point(data[0]) # 타입 별 평균 학점
        point['culture_necessary_point'] = subject_fn.get_culutre_necessary_point(data[0]) # 교양필수 학점 총 합
        point['culture_select_total_point'] = subject_fn.get_culutre_select_point(data[0]) # 교양선택 학점 총 합
        point['line_necessary_point'] = subject_fn.get_line_necessary_point(data[0]) # 계열필수 학점 총 합

        ### 세션 데이터 설정
        request.session['point_info'] = point
        request.session['subject_list'] = subject_list
        request.session['total_point'] = total_point
        request.session['graduated_point'] = graduated_point # 졸업 학점
        request.session['basic_major_point'] = basic_major_point # 기본 전공 학점
        request.session['major_point'] = major_point # 전체 전공 학점
        request.session['culture_point'] = culture_point # 교양 학점
        request.session['subject_point'] = subject_point  # 과목 학점 정보
        request.session['user_info'] = user_info  # 유저정보
        request.session['scholar_ship'] =  scholar_ship # 장학금 정보
        request.session['average_point_info'] = average_point_info # 평균 학점 정보
        request.session['remain_graduated_point'] = remain_graduated_point # 남은 졸업 학점
        request.session['graduated_point_percentage'] = graduated_point_percentage
        request.session['major_point_percentage'] = major_point_percentage
        request.session['culture_point_percentage'] = culture_point_percentage
        request.session['consult_count'] = consult_count

        notice = Notice.objects.all().last()

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
            'average_point_info': average_point_info,
            'remain_graduated_point': remain_graduated_point,
            'graduated_point_percentage': graduated_point_percentage,
            'major_point_percentage': major_point_percentage,
            'culture_point_percentage': culture_point_percentage,
            'plural_major' : plural_major,
            'teach_major' : teach_major, 
            'consult_count' : consult_count,
            'average_point_total' : average_point_total,
            'notice' : notice,
        }

    return render(request, 'webcrawler/index.html', context)

## 학점 상세 정보
def point(request):

    # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')

    point_info = {}

    if request.session.get('point_info', False):
        point_info = request.session['point_info'].copy()

    return render(request, 'webcrawler/point.html', point_info)

## 이수과목 리스트 뷰
def completed_list(request):
    
    # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')

    # 사용자 정보
    if request.session.get('user_info', False):
        user_info = request.session['user_info']
    else:
        user_info = None

    # 이수과목 리스트
    if request.session.get('data', False):
        completed_list = request.session['data'][0] # 이수과목 리스트
        count_grade = subject_fn.get_count_grade_point(completed_list) # 각 과목 등급 카운팅
        completed_list_count = len(completed_list.keys()) # 이수과목 개수
        completed_list_point_count = int(sum([float(i[2]) for i in completed_list.values() ])) # 이수과목 학점 총점
    else:
        completed_list = None

    # 공학인증 리스트
    try:
        certification_list = Subject.objects.filter(major__name__contains=user_info[6]) # 공학인증 리스트
        certification_list_title = [item.title for item in certification_list ] # 공학인증 과목
        certification_list_info =  { item.title : item.certification_type for item in certification_list} # 공학인증 정보
        certification_list_necessary = { item.title : item.necessary for item in certification_list } # 필수과목 여부
        certification_major = Major.objects.get(name=user_info[6]).certification # 공학인증 학과 여부
    except Major.DoesNotExist:
        certification_major = False
    except UnboundLocalError:
        return redirect('accounts:login')


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

# 필수과목 리스트
def necessary_list(request):
    
    # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')

    # 사용자 정보
    # 과목 리스트
    if request.session.get('user_info', False) and request.session.get('subject_list', False):
        user_info = request.session['user_info']
        user_subject_list = request.session['subject_list']
    else:
        user_info = None
        user_subject_list = None

    if user_subject_list and user_info:
        user_subject_list = [subject for subject in user_subject_list.keys()] # 사용자 이수과목
        necessary_subject_list = Subject.objects.filter(necessary=True, major__name__contains=user_info[6]) # 사용자 전공 필수과목
    else:
        user_subject_list = None
        necessary_subject_list = None

    completed_list = [] # 이수과목 리스트
    not_completed_list = [] # 미이수 과목리스트

    # 사용자의 과목 리스트와 사용자 전공의 필수과목 리스트와 비교해 이수과목, 미 이수과목 체크
    for subject in necessary_subject_list:
        if subject.title in user_subject_list:
            completed_list.append(subject) # 이수한 과목
        else:
            not_completed_list.append(subject) # 미 이수 과목

    context = {
        'completed_list' : completed_list,
        'not_completed_list' : not_completed_list,
    }

    return render(request, 'webcrawler/necessary_list.html', context)

## 전공과목 리스트 뷰
def major_list(request):
    
     # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')

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
        major_list = subject_fn.get_major_subject(request.session['data'][0])
        count_grade = subject_fn.get_count_grade_point(major_list)
        count_type = subject_fn.get_count_type(major_list)
        major_list_count = len(major_list.keys()) # 전공과목 개수
        major_list_point_count = int(sum([float(i[2]) for i in major_list.values() ])) # 전공과목 학점 총점
    else:
        major_list = None

    context = {
        'major_list': major_list,
        'major_list_count': major_list_count,
        'major_list_point_count': major_list_point_count,
        'certification_list_title': certification_list_title,
        'certification_list_info': certification_list_info,
        'certification_list_necessary': certification_list_necessary,
        'certification_major': certification_major,
        'count_grade': count_grade,
        'count_type': count_type,
    }

    return render(request, 'webcrawler/major_list.html', context)

## 교양과목 리스트 뷰
def culture_list(request):

     # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')

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
        culture_list = subject_fn.get_culture_subject(request.session['data'][0])
        count_grade = subject_fn.get_count_grade_point(culture_list)
        count_type = subject_fn.get_count_type(culture_list)
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

def chart(request):

     # 로그인 체크
    if not (request.session.get('intranet_id', False) and request.session.get('intranet_pw', False)):
        return redirect('accounts:login')
        
    if request.session.get('average_point_info', False):
        average_point_info = request.session['average_point_info']

    return render(request, 'webcrawler/chart.html', {'average_point_info': average_point_info})

