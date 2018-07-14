from django.contrib import messages
from django.shortcuts import render, redirect
from .intranet import parsed_subject


def check_sum_of_list(data):
    '''
        전공 총 학점, 선택전공 총 학점, 기본전공 총 학점
        교양 필수 학점, 교양 선택학점, 계열 필수 학점
        item은 사전 형태로 전달 됨
        subject[title.text] = [kind.text, point.text, grade.text]
    '''
    sum = 0

    for title, arr in data.items():
        if arr[0] == "교필" or arr[0] == "교선" or arr[0] == "계필":
            sum = sum + float(arr[1])

    return sum

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
                point_culture_subject = check_sum_of_list(data[0]) # 교필, 교선 일때의 점수의 합
                subject_list = data[0] # 과목 리스트
                total_point = data[1]['sum_of_grade_point']  # 전체 학점            
            else:
                # 로그인 에러 출력
                messages.error(request, '로그인에 실패했습니다.')
                return redirect('accounts:login')
        except NameError:
            print("NameError 발생")

        

    context = {'point_culture_subject': point_culture_subject, 'subject_list': subject_list,
            'total_point': total_point}  # data를 분할해서 여러개의 context로 넘기기

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

def major_list(request):
    
    if request.session.get('data', False):
        major_list = select_major_subject(request.session['data'][0])
    else:
        major_list = None

    return render(request, 'webcrawler/major_list.html', {'major_list' : major_list})

def select_major_subject(subject):

    ''' subject는 dict '''

    major_subject = {}

    for title, item in subject.items():
        if item[0] == '기전' or item[0] == '선전':
            major_subject[title] =  item

    return major_subject
