from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mysql_app.models import Instance, QueryData
from .fetch import fetchLogs
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, password=password, username=username)

            if user is not None:
                login(request,user)
                return redirect('dashboard')

            else:
                messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'mysql_app/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    context = {}
    return render(request, 'mysql_app/dashboard.html', context)

@login_required(login_url='login')
def view_instances(request):
    
    instances = Instance.objects.all()
    context = {'instances' : instances}
    return render(request, 'mysql_app/view_instances.html', context)

@login_required(login_url='login')
def view_logs(request, instance_id):
    instance = Instance.objects.filter(id=instance_id)
    if instance.exists():
        instance = instance[0]
        instance.status = True
        instance.save()
        create_flag = fetchLogs(instance)
    else:
        instance = ''
    query_data = QueryData.objects.filter(instance_id= instance_id).all()
    context = {'instance': instance, 'query_data' : query_data}
    return render(request, 'mysql_app/view_log.html', context)
