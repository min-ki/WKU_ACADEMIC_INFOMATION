from django.shortcuts import render, redirect
from django.contrib import messages
from webcrawler.intranet import parser
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
# 웹 정보 서비스 로그인
def login(request):
    
    if request.method == 'POST':
        request.session['intranet_id'] = request.POST['username']
        request.session['intranet_pw'] = request.POST['password']
        
        if not request.session.get('data', False):
            while(True):
                try:
                    data = parser(request.POST['username'], request.POST['password'])
                except UnexpectedAlertPresentException:
                    continue
                except NoSuchElementException:
                    continue
                break

            if data == "login_fail":
                messages.error(request, '로그인에 실패하셨습니다.')
            else:
                request.session['data'] = data
                messages.success(request, '로그인에 성공하셨습니다.')
                return redirect('home:index')
        else:
            data = request.session['data']
            return redirect('home:index')
    else:
        request.session.flush()
    
    return render(request, 'accounts/login.html', {})

# 세션 로그아웃
def logout(request):

    request.session.flush() # 세션 데이터 초기화
    messages.success(request, '로그아웃이 성공적으로 되었습니다.')
    return redirect('accounts:login')
