from django.contrib import messages
from django.shortcuts import render, redirect
from .intranet import parser
from .models import Subject, Major
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
        data = parser(
            request.session['intranet_id'], request.session['intranet_pw'])

    if data:
        subject_list = data[0] # 과목 리스트
        subject_point = subject_fn.get_sum_of_subject(data[0]) # 전공학점, 교양학점
        total_point = int(data[1]['sum_of_grade_point'])  # 전체 학점
        user_info = data[2]  # 사용자 정보    
        scholar_ship = data[3] # 장학정보
        wpoint = data[4] # WPOINT  
        detail_wpoint = data[5] # WPOINT Detail
        average_point_info = data[6]
        graduated_point = subject_fn.get_graduated_point(user_info[1], user_info[4], user_info[6]) # 졸업학점
        major_point, basic_major_point = subject_fn.get_major_point(user_info[1], user_info[4], user_info[6]) # 기본전공, 전체 전공학점
        culture_point = subject_fn.get_culture_point(user_info[1]) # 교양학점 
        remain_graduated_point = int(graduated_point - total_point) # 남은학점
        
        graduated_point_percentage = int(subject_fn.get_percentage(total_point, graduated_point))  # 졸업학점 퍼센티지
        major_point_percentage = int(subject_fn.get_percentage(subject_point['major_subject_sum'], major_point))  # 전공학점 퍼센티지
        culture_point_percentage = int(subject_fn.get_percentage(subject_point['culture_subject_sum'], culture_point)) # 교양학점 퍼센티지

        ### 필수 학점
        graduated_culture_point = subject_fn.get_culutre_necessary_point(data[0])
        graduated_line_point = subject_fn.get_line_necessary_point(data[0])
        graduated_language_point = subject_fn.get_language_necessary_point(data[0])
        graduated_english_point = subject_fn.get_english_necessary_point(data[0])
        graduated_sw_point = subject_fn.get_sw_necessary_point(data[0])
        graduated_culture_choice_point = subject_fn.get_culture_choice_point(data[0])
        graduated_founded_subject_point = subject_fn.get_founded_subject_necessary_point(data[0])
        graduated_creative_point = subject_fn.get_creative_necessary_point(data[0])

        ### 복수전공, 교직이수 
        plural_major = subject_fn.check_plural_major(data[0]) 
        teach_major = subject_fn.check_teach_major(data[0])

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
            'graduated_culture_point': graduated_culture_point,
            'graduated_line_point': graduated_line_point,
            'graduated_language_point': graduated_language_point,
            'graduated_english_point': graduated_english_point,
            'graduated_sw_point': graduated_sw_point,
            'graduated_culture_choice_point' : graduated_culture_choice_point,
            'graduated_founded_subject_point': graduated_founded_subject_point,
            'graduated_creative_point' : graduated_creative_point,
        }

    return render(request, 'webcrawler/index.html', context)


## 이수과목 리스트 뷰
def completed_list(request):
    
    # 로그인 체크
    if request.session.get('intranet_id', False) and request.session.get('intranet_pw', False):
        pass
    else:
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
        certification_list_title = [item.title for item in certification_list] # 공학인증 과목
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
    if request.session.get('intranet_id', False) and request.session.get('intranet_pw', False):
        pass
    else:
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

    return render(request, 'webcrawler/chart.html', {'average_point_info': average_point_info})
