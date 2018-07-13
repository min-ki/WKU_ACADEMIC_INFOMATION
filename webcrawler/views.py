from django.shortcuts import render
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
        data = parsed_subject(intranet_id, intranet_pw)

        # 교필, 교선 일때의 점수의 합
    value = check_sum_of_list(data[0])

    context = {'data': data, 'value': value} # data를 분할해서 여러개의 context로 넘기기

    return render(request, 'webcrawler/index.html', context)



