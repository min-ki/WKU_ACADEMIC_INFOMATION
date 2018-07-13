from django.shortcuts import render, redirect


def login(request):
    
    if request.method == 'POST':
        request.session['intranet_id'] = request.POST['username']
        request.session['intranet_pw'] = request.POST['password']
        
        return redirect('home:index')
        
    return render(request, 'accounts/login.html', {})