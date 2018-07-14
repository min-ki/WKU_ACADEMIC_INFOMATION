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
            data = parsed_subject(intranet_id, intranet_pw)
        except NameError:
            print("NameError 발생")

        if data:
            point_culture_subject = check_sum_of_list(data[0]) # 교필, 교선 일때의 점수의 합
            subject_list = data[0] # 과목 리스트
            total_point = data[1]['sum_of_grade_point']  # 전체 학점            
        else:
            # 로그인 에러 출력
            messages.error(request, '로그인에 실패했습니다.')
            return redirect('accounts:login')

    context = {'point_culture_subject': point_culture_subject, 'subject_list': subject_list,
            'total_point': total_point}  # data를 분할해서 여러개의 context로 넘기기

    return render(request, 'webcrawler/index.html', context)







